#!/usr/bin/env python3
"""Run the executable code that lives inside the skills.

`validate.py` checks the repo's shape. This checks the behaviour of the four
pieces of real logic the skills carry, and it extracts each one **from
`SKILL.md` itself** rather than from a copy - so what runs here is exactly what
an agent will paste into a page.

Covered:

  1. NetSuite `__page`   - PDF layout rebuilt from pdf.js geometry: columns line
                           up across rows, barcode and long-digit rows dropped.
  2. NetSuite `__pages`  - size-budgeted extraction: whole pages only, never
                           split, degrades to one-per-call on a big page.
  3. Procore  `__gate`   - the actionability fan-out returns three distinct
                           states. This is the safety property: a failed request
                           must never read as "no workflow instance", which the
                           execute step treats as already-actioned.
  4. publish_dashboard   - a CCO without a resolved wfId is demoted to `ungated`
                           with no response buttons, rather than falling back to
                           the package id.

Usage:  python3 scripts/test_skill_code.py
Needs node on PATH for 1-3; those are skipped with a notice if it is missing.
"""
import json, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = os.path.join(REPO, "plugins/netsuite-approval-review/skills/"
                        "netsuite-approval-double-check")
PC = os.path.join(REPO, "plugins/procore-open-items-review/skills/"
                        "procore-open-items-review")

failures = []


def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + (("  - " + detail) if detail and not ok else ""))
    if not ok:
        failures.append(name)


def js_block(path, needle):
    """Pull the ```javascript block containing `needle` out of a SKILL.md."""
    src = open(path, encoding="utf-8").read()
    blocks = [b for b in re.findall(r"```javascript\n(.*?)```", src, re.S) if needle in b]
    if not blocks:
        sys.exit("ABORT: no javascript block containing %r in %s. The test "
                 "extracts from SKILL.md on purpose - if the block moved or was "
                 "renamed, fix this test rather than duplicating the code." % (needle, path))
    return blocks[0]


def run_node(script):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(script)
        p = f.name
    try:
        r = subprocess.run(["node", p], capture_output=True, text=True, timeout=60)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    finally:
        os.unlink(p)


# ---------------------------------------------------------------- 1. extractor
def test_extractor():
    body = js_block(os.path.join(NS, "SKILL.md"), "__page")
    # drop the pdf.js import/worker lines - not runnable outside a browser
    body = "\n".join(l for l in body.split("\n") if not l.startswith(
        ("const m =", "window.__pj", "const wt", "m.GlobalWorkerOptions")))
    body = body.replace("'ready'", "")
    # feed items straight in instead of going through a real pdf.js page
    body = body.replace(
        "const c = await (await window.__doc.getPage(n)).getTextContent();",
        "const c = n;")
    harness = r"""
var window = {};
""" + body + r"""
const mk = (str,x,y) => ({str, width: str.length*3.42, transform:[0,0,0,0,x,y]});
const page = { items: [
  mk('Electricity Supply Charge', 40, 700), mk('11,739 kWh', 220, 700), mk('$737.99', 400, 700),
  mk('Capacity Charge',           40, 685), mk('6.57 kW X 10.11236', 220, 685), mk('$66.44', 400, 685),
  mk('0110110101101011011010',    40, 200),   // barcode - must drop
  mk('123456789012345678901234',  40, 180),   // remittance digits - must drop
  mk('   ',                       40, 160),   // whitespace only - must drop
]};
(async () => {
  const out = await window.__page(page);
  const rows = out.split('\n');
  console.log(JSON.stringify({
    rows: rows.length,
    barcodeGone: !out.includes('011011'),
    remitGone: !out.includes('123456789012'),
    amtAligned: rows[0].indexOf('$737.99') === rows[1].indexOf('$66.44'),
    basisAligned: rows[0].indexOf('11,739') === rows[1].indexOf('6.57'),
  }));
})();
"""
    rc, out, err = run_node(harness)
    if rc != 0:
        check("extractor runs", False, err.splitlines()[0] if err else "non-zero exit")
        return
    r = json.loads(out)
    check("extractor: two data rows survive the filter", r["rows"] == 2, "got %s" % r["rows"])
    check("extractor: barcode row dropped", r["barcodeGone"])
    check("extractor: long-digit row dropped", r["remitGone"])
    check("extractor: amount column aligns across rows", r["amtAligned"])
    check("extractor: basis column aligns across rows", r["basisAligned"])


# ------------------------------------------------------------- 2. page budget
def test_page_budget():
    body = js_block(os.path.join(NS, "SKILL.md"), "__pages")
    harness = r"""
var window = {};
""" + body + r"""
async function run(sizes){
  window.__doc = {numPages: sizes.length};
  window.__page = async n => 'x'.repeat(sizes[n-1]);
  let calls = 0, from = 1, per = [];
  while (from) {
    const r = await window.__pages(from);
    calls++; per.push((r.text.match(/--- page /g)||[]).length); from = r.next;
    if (calls > 20) return {runaway:true};
  }
  return {calls, per};
}
(async () => {
  console.log(JSON.stringify({
    small:     await run([800,900,850]),
    oversized: await run([9000]),
    mixed:     await run([9000,500,500]),
    medium:    await run([1500,1500,1500,1500,1500]),
  }));
})();
"""
    rc, out, err = run_node(harness)
    if rc != 0:
        check("page budget runs", False, err.splitlines()[0] if err else "non-zero exit")
        return
    r = json.loads(out)
    check("page budget: three small pages collapse to one call",
          r["small"]["calls"] == 1, "got %s calls" % r["small"]["calls"])
    check("page budget: an oversized page returns alone and uncut",
          r["oversized"]["calls"] == 1 and r["oversized"]["per"] == [1])
    check("page budget: never splits a page",
          all(p >= 1 for p in r["mixed"]["per"]) and not r["mixed"].get("runaway"))
    check("page budget: terminates", not r["medium"].get("runaway"))


# --------------------------------------------------------------- 3. gate states
def test_gate_states():
    body = js_block(os.path.join(PC, "SKILL.md"), "__gate")
    harness = r"""
var window = {};
""" + body + r"""
const EQ = String.fromCharCode(61), AMP = String.fromCharCode(38);
global.fetch = async function(u){
  const id = u.split('object_id]'+EQ)[1].split(AMP)[0];
  if (id === '2') return {ok:false, status:429};          // rate limited
  if (id === '3') return {ok:true, json: async()=>[]};    // genuinely no instance
  if (id === '4') throw new Error('network down');
  return {ok:true, json: async()=>[{
    user_permissions:{can_respond: id === '1'},
    current_step_occurrence:{name:'FA Review', due_at:'2026-08-20',
                             available_responses:['Approve']}}]};
};
(async () => {
  const rows = [1,2,3,4,5].map(n => ({key:'k'+n, pid:'999', id:String(n), type:'GenericToolItem'}));
  const out = await window.__gate(rows, 3);
  const by = k => out.find(r => r.key === k);
  console.log(JSON.stringify({
    total: out.length,
    rateLimitIsFailed: by('k2') && by('k2').state === 'failed',
    throwIsFailed:     by('k4') && by('k4').state === 'failed',
    emptyIsEmpty:      by('k3') && by('k3').state === 'empty',
    canRespondHonoured: by('k1').can === true && by('k5').can === false,
  }));
})();
"""
    rc, out, err = run_node(harness)
    if rc != 0:
        check("gate fan-out runs", False, err.splitlines()[0] if err else "non-zero exit")
        return
    r = json.loads(out)
    check("gate: every item accounted for", r["total"] == 5, "got %s" % r["total"])
    check("gate: a 429 is `failed`, never `empty`", r["rateLimitIsFailed"])
    check("gate: a thrown request is `failed`", r["throwIsFailed"])
    check("gate: a genuine no-instance is `empty`", r["emptyIsEmpty"])
    check("gate: can_respond is read correctly", r["canRespondHonoured"])


# ------------------------------------------------------ 4. CCO ungated demotion
def test_cco_demotion():
    d = tempfile.mkdtemp()
    try:
        assets = os.path.join(PC, "assets")
        for f in ("publish_dashboard.py", "dashboard_template.html"):
            shutil.copy(os.path.join(assets, f), d)
        log = {
            "lastCompletedRun": "2026-08-13", "lastRunTime": "2026-08-13 11:00",
            "suppressed": 0, "config": {"company": "0", "icrToolId": "0"},
            "items": {
                "resolved": {"itemId": "111", "wfId": "999", "projectId": "9", "commitmentId": "8",
                             "kind": "cco", "type": "CCO", "docNo": "#002", "project": "A - B",
                             "counterparty": "X", "amount": 1000, "step": "FA Review",
                             "responses": ["Approve"], "verdict": "clear",
                             "head": "h", "facts": ["f"], "detail": "d"},
                "unresolved": {"itemId": "222", "projectId": "9", "commitmentId": "8",
                               "kind": "cco", "type": "CCO", "docNo": "#010", "project": "A - B",
                               "counterparty": "X", "amount": 2000, "step": "FA Review",
                               "responses": ["Approve"], "verdict": "clear",
                               "head": "h", "facts": ["f"], "detail": "d"},
            },
        }
        json.dump(log, open(os.path.join(d, "_procore_review_log.json"), "w"))
        out_html = os.path.join(d, "index.html")
        r = subprocess.run([sys.executable, os.path.join(d, "publish_dashboard.py"), out_html],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            check("publish script runs", False, (r.stderr or r.stdout).strip().splitlines()[-1:] or "")
            return
        blob = re.search(r"/\*__REVIEW_DATA__\*/(.*?)/\*__END__\*/",
                         open(out_html, encoding="utf-8").read(), re.S).group(1)
        items = {i["doc"]: i for i in json.loads(blob)["items"]}
        ok = items["#002"]
        bad = items["#010"]
        check("cco: resolved wfId keeps its response buttons",
              ok["verdict"] == "clear" and ok["resp"] and ok["wfId"] == "999")
        check("cco: resolved wfId is distinct from the record id", ok["wfId"] != ok["id"])
        check("cco: workflow type is CommitmentChangeOrder, not the queue's item_type",
              ok["wf"] == "CommitmentChangeOrder", ok["wf"])
        check("cco: unresolved wfId is demoted to ungated", bad["verdict"] == "ungated", bad["verdict"])
        check("cco: unresolved wfId offers no response buttons", bad["resp"] == [])
        check("cco: demotion is announced, not silent", "wfId" in (r.stdout + r.stderr))
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    print("Skill code checks\n")
    if shutil.which("node"):
        test_extractor()
        test_page_budget()
        test_gate_states()
    else:
        print("  SKIP  node not on PATH - extractor, page budget and gate states not run")
    test_cco_demotion()
    print()
    if failures:
        print("FAILED: " + "; ".join(failures))
        sys.exit(1)
    print("OK: all skill code checks passed")


if __name__ == "__main__":
    main()
