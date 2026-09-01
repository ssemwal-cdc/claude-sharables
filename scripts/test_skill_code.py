#!/usr/bin/env python3
"""Run the executable code that lives inside the skills.

`validate.py` checks the repo's shape. This checks the behaviour of the six
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
  5. Procore  `__sniff`  - attachment bytes are classified before parsing. A
                           workbook or an image must never sniff as `pdf`, and an
                           expired S3 body must be its own state - folding those
                           together is what left whole formats unread.
  6. Procore  `__sheets` - workbook reads are budgeted by whole sheets, include
                           hidden sheets, and drop long-digit rows without taking
                           the real row beside them.
  7. template version   - each publish script's TEMPLATE_VERSION matches the marker
                           in its sibling template, and a mismatch warns without
                           stopping the run.
  8. PO identity rules  - the NetSuite SKILL.md resolves a bill's PO from the
                           transaction linkage, not from the typed `custbody3`
                           reference. Guards the exact queries whose absence
                           produced false "coded to the wrong PO" flags.
  9. NetSuite `poLine`  - the dashboard keeps linked / unlinked / failed distinct,
                           so an unconfirmed PO cannot render as confirmed.
 10. Step 0 write states - the workspace write keeps kept / refused / not attempted
                           distinct, so a run cannot announce that state will not
                           persist without having tried to write it.
 12. Custom tool subtype - a GenericToolItem's record link and cost fields come from
                           its own custom tool, and an unmapped subtype gets no link and no
                           `clear` verdict rather than another tool's id.
 13. Large render       - a 62-item dashboard stays inside one default file read on both
                           axes: under 2,000 lines and no single very long line. Rendering
                           means reproducing the file through a tool call, so a file that
                           cannot be read cannot be rendered at all.
 11. Commitment kind    - a `com` item without a wfType is demoted to `ungated`
                           rather than defaulting to one of the two commitment
                           collections. Both are valid workflowable types, so the
                           wrong one with the right id returns an empty instance,
                           which the execute step reads as already-actioned.

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


# ------------------------------------------------------------- 5. byte sniffing
def test_sniff():
    body = js_block(os.path.join(PC, "SKILL.md"), "__sniff")
    harness = r"""
var window = {};
""" + body + r"""
const buf = a => new Uint8Array(a).buffer;
// pad past the 512-byte printable-ASCII probe so the magic number is what decides
const pad = a => buf(a.concat(Array(600).fill(0x41)));
const asc = s => buf([...Buffer.from(s)]);
const cases = [
  ['pdf',      pad([0x25,0x50,0x44,0x46,0x2D,0x31,0x2E,0x36]), 'pdf'],
  ['xlsx',     pad([0x50,0x4B,0x03,0x04,0x14,0x00,0x06,0x00]), 'zip'],
  ['xls',      pad([0xD0,0xCF,0x11,0xE0,0xA1,0xB1,0x1A,0xE1]), 'ole2'],
  ['png',      pad([0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A]), 'image'],
  ['jpeg',     pad([0xFF,0xD8,0xFF,0xE0,0x00,0x10,0x4A,0x46]), 'image'],
  ['gif',      pad([0x47,0x49,0x46,0x38,0x39,0x61,0x01,0x00]), 'image'],
  ['tiff-le',  pad([0x49,0x49,0x2A,0x00,0x08,0x00,0x00,0x00]), 'image'],
  ['tiff-be',  pad([0x4D,0x4D,0x00,0x2A,0x00,0x00,0x00,0x08]), 'image'],
  ['webp',     pad([0x52,0x49,0x46,0x46,0x24,0x00,0x00,0x00]), 'image'],
  ['s3-xml',   asc('<?xml version="1.0"?><Error><Code>AccessDenied</Code></Error>'), 's3error'],
  ['s3-bare',  asc('<Error><Code>ExpiredToken</Code></Error>'), 's3error'],
  ['csv',      asc('Description,Scheduled Value\nElectrical,10849586.00\n'), 'text'],
  ['binary',   buf([0x00,0x01,0x02,0x03,0xDE,0xAD,0xBE,0xEF,0x7F,0x80,0x91,0xA2]), 'unknown'],
];
const bad = cases.filter(([n,b,want]) => window.__sniff(b) !== want).map(([n]) => n);
console.log(JSON.stringify({
  bad: bad,
  total: cases.length,
  // the three that carry the safety property, called out separately
  xlsxNotPdf:   window.__sniff(cases[1][1]) !== 'pdf',
  imageNotPdf:  window.__sniff(cases[3][1]) !== 'pdf',
  expiredIsOwn: window.__sniff(cases[9][1]) === 's3error',
}));
"""
    rc, out, err = run_node(harness)
    if rc != 0:
        check("sniff runs", False, err.splitlines()[0] if err else "non-zero exit")
        return
    r = json.loads(out)
    check("sniff: all %d magic-number cases" % r["total"], not r["bad"],
          "wrong: %s" % ", ".join(r["bad"]))
    # These three are the bug this was written for: a workbook or an image fed to
    # pdf.js throws, and the old two-state rule read that throw as "expired, retry"
    # or as "a scanned image" - so whole formats went unread. They must never sniff
    # as `pdf`, and an expired link must be its own state rather than a non-PDF.
    check("sniff: a workbook is never `pdf`", r["xlsxNotPdf"])
    check("sniff: an image is never `pdf`", r["imageNotPdf"])
    check("sniff: an expired S3 body is `s3error`, not a non-PDF", r["expiredIsOwn"])


# ---------------------------------------------------------- 6. workbook reading
def test_sheets():
    body = js_block(os.path.join(PC, "SKILL.md"), "__sheets")
    # drop the CDN loader line - not runnable outside a browser, and node would
    # try to resolve the URL as a module specifier. XLSX is stubbed below instead.
    body = "\n".join(l for l in body.split("\n") if not l.startswith("await import("))
    harness = r"""
var window = {};
const SHEETS = {
  'Summary':   'Description,Amount\nElectrical labour,10849586\n,\nTotal,10849586\n',
  'Detail':    'Line,Value\n' + Array.from({length:400},(_,i)=>'L'+i+','+(i*1000)).join('\n') + '\n',
  'Hidden WS': 'Note,Val\nbarcode,000000000000000000000123456789012345\nReal,42\n'
};
global.XLSX = {
  read: () => ({SheetNames: Object.keys(SHEETS), Sheets: SHEETS}),
  utils: {sheet_to_csv: ws => ws}
};
""" + body + r"""
let n = 0, calls = 0, all = '', split = false;
do {
  const r = window.__sheets(new ArrayBuffer(8), n);
  calls++;
  // a call carrying part of a sheet without its header would mean a split
  if ((r.text.match(/--- sheet /g) || []).length === 0) split = true;
  all += r.text + '\n';
  n = r.next;
} while (n !== null && calls < 10);
console.log(JSON.stringify({
  calls: calls,
  neverSplit: !split,
  hiddenIncluded: /--- sheet 3: Hidden WS ---/.test(all),
  longDigitDropped: !/000000000000000000000123456789012345/.test(all),
  realRowKept: /Real,42/.test(all),
  blankRowDropped: !/\n,\n/.test(all),
  figuresIntact: /Electrical labour,10849586/.test(all),
}));
"""
    rc, out, err = run_node(harness)
    if rc != 0:
        check("sheets runs", False, err.splitlines()[0] if err else "non-zero exit")
        return
    r = json.loads(out)
    check("sheets: terminates", r["calls"] < 10, "ran %s calls" % r["calls"])
    check("sheets: budgets whole sheets, never splits one", r["neverSplit"])
    # A superseded figure is exactly the thing that gets hidden rather than deleted,
    # so taking sheet 1 and stopping would miss the case this check exists for.
    check("sheets: hidden sheets are read", r["hiddenIncluded"])
    check("sheets: long-digit row dropped", r["longDigitDropped"])
    check("sheets: the real row beside it survives", r["realRowKept"])
    check("sheets: blank rows dropped", r["blankRowDropped"])
    check("sheets: figures intact", r["figuresIntact"])


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


# ------------------------------------------------- 11. commitment kind (`com`)
def test_commitment_kind():
    """A commitment must carry the queue's item_type, and must not be guessed without it.

    `com` covers PurchaseOrderContract and WorkOrderContract. Both are valid workflowable
    types, so the wrong one carrying the right id comes back 200 with zero rows rather than
    a 400 - and Step 8 reads an empty instance as "already actioned elsewhere, skip it". A
    live contract would be logged as done with no click, which is the CCO wrong-id failure
    one type along. Hence: fail closed, and say so.
    """
    d = tempfile.mkdtemp()
    try:
        assets = os.path.join(PC, "assets")
        for f in ("publish_dashboard.py", "dashboard_template.html"):
            shutil.copy(os.path.join(assets, f), d)
        base = {"projectId": "9", "kind": "com", "project": "A - B", "counterparty": "X",
                "amount": 1000, "step": "Financial Analyst Review",
                "responses": ["Approve", "Revise and Resubmit"], "verdict": "clear",
                "head": "h", "facts": ["f"], "detail": "d"}
        log = {
            "lastCompletedRun": "2026-08-28", "lastRunTime": "2026-08-28 09:00",
            "suppressed": 0, "config": {"company": "0", "icrToolId": "0"},
            "items": {
                "po": dict(base, itemId="111", commitmentId="111", docNo="#PO-1",
                           wfType="PurchaseOrderContract"),
                "wo": dict(base, itemId="222", commitmentId="222", docNo="#WO-1",
                           wfType="WorkOrderContract"),
                "untyped": dict(base, itemId="333", commitmentId="333", docNo="#UN-1"),
            },
        }
        json.dump(log, open(os.path.join(d, "_procore_review_log.json"), "w"))
        out_html = os.path.join(d, "index.html")
        r = subprocess.run([sys.executable, os.path.join(d, "publish_dashboard.py"), out_html],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            check("publish script runs on commitments", False,
                  (r.stderr or r.stdout).strip().splitlines()[-1:] or "")
            return
        page = open(out_html, encoding="utf-8").read()
        blob = re.search(r"/\*__REVIEW_DATA__\*/(.*?)/\*__END__\*/", page, re.S).group(1)
        items = {i["doc"]: i for i in json.loads(blob)["items"]}
        po, wo, un = items["#PO-1"], items["#WO-1"], items["#UN-1"]
        check("com: a purchase order contract keeps its response buttons",
              po["verdict"] == "clear" and po["resp"], po["verdict"])
        check("com: the queue's item_type survives as the workflow type",
              po["wf"] == "PurchaseOrderContract" and wo["wf"] == "WorkOrderContract",
              "%s / %s" % (po["wf"], wo["wf"]))
        check("com: the workflow id is the record's own id, never a second lookup",
              po["wfId"] == po["id"] == "111", po["wfId"])
        check("com: no wfType is demoted to ungated", un["verdict"] == "ungated", un["verdict"])
        check("com: an untyped commitment offers no response buttons", un["resp"] == [])
        check("com: the demotion is announced, not silent", "wfType" in (r.stdout + r.stderr))
        # The link's collection is the same fork. Getting it from `wf` rather than from `kind`
        # is what makes one kind able to address two collections at all.
        check("com: the record link branches on the collection, not on kind alone",
              "work_order_contracts" in page and 'it.kind==="com"' in page)
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------- 7. template version
def _marker(path):
    m = re.search(r"layout template (v\d+)", open(path, encoding="utf-8").read())
    return m.group(1) if m else None


def test_template_version():
    """The marker exists to make a stale workspace copy legible. A marker nobody
    bumps is the state this replaced, so the agreement is enforced here."""
    for label, root in (("netsuite", NS), ("procore", PC)):
        assets = os.path.join(root, "assets")
        script = open(os.path.join(assets, "publish_dashboard.py"), encoding="utf-8").read()
        m = re.search(r'TEMPLATE_VERSION\s*=\s*"(v\d+)"', script)
        expect = m.group(1) if m else None
        found = _marker(os.path.join(assets, "dashboard_template.html"))
        check("%s: publish script declares TEMPLATE_VERSION" % label, expect is not None)
        check("%s: template carries a version marker" % label, found is not None)
        check("%s: script and template agree (%s)" % (label, expect),
              expect is not None and expect == found, "script=%s template=%s" % (expect, found))

    # Behaviour, not just agreement: a stale template must warn and still publish.
    # Aborting here would kill a Cowork run whose verdicts are fine and whose only
    # lag is the layout - which is the whole reason this warns instead of exiting.
    d = tempfile.mkdtemp()
    try:
        assets = os.path.join(NS, "assets")
        for f in ("publish_dashboard.py", "dashboard_template.html"):
            shutil.copy(os.path.join(assets, f), d)
        tpl_path = os.path.join(d, "dashboard_template.html")
        tpl = open(tpl_path, encoding="utf-8").read()
        open(tpl_path, "w", encoding="utf-8").write(
            re.sub(r"layout template v\d+", "layout template v0", tpl, count=1))
        json.dump({"lastCompletedRun": "2026-08-20", "lastRunTime": "2026-08-20 09:00",
                   "config": {"me": 42, "account": "1", "tool": "t"},
                   "items": {"1": {"type": "Bill", "docNo": "B1", "vendor": "V", "amount": 1,
                                   "trandate": "8/1/2026", "verdict": "clear", "head": "h",
                                   "facts": ["f"], "detail": "d"}}},
                  open(os.path.join(d, "_netsuite_review_log.json"), "w"))
        out = os.path.join(d, "index.html")
        r = subprocess.run([sys.executable, os.path.join(d, "publish_dashboard.py"), out],
                           capture_output=True, text=True, timeout=60)
        check("stale template warns", "WARNING" in (r.stdout + r.stderr) and
              "v0" in (r.stdout + r.stderr))
        check("stale template does NOT stop the run", r.returncode == 0, "exit %s" % r.returncode)
        check("stale template still publishes", os.path.exists(out))
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_step0_write_states():
    """A run declared that state would not persist because the workspace folder was
    OneDrive-synced, and went session-local without ever attempting the write
    (reported 2026-08-27). Every phrase in that message came from Step 0, which
    described the fallback without ever saying the failure has to be observed - and
    helpfully listed plausible causes a run can match against in advance. Same bug
    class as `empty` vs `failed` and `scanned` vs `unsupported`: two states collapsed,
    so the one that means "nobody looked" reports as the one that means "it failed".

    The rule that would have caught it existed only in CLAUDE.md, which the running
    skill never reads. These assertions live here so it cannot quietly leave the
    prompt again."""
    for label, root in (("netsuite", NS), ("procore", PC)):
        txt = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
        step0 = txt.split("## Step 0")[1].split("## Step 1")[0] if "## Step 0" in txt else ""
        check("%s: Step 0 is where the workspace write is specified" % label, bool(step0))

        # The three outcomes, each named. `not attempted` is the one that was missing.
        for state in ("kept", "refused", "not attempted"):
            check("%s: Step 0 names the `%s` outcome" % (label, state),
                  "`%s`" % state in step0)
        check("%s: the fallback is tied to `refused`, not to a failure in general" % label,
              "belongs to `refused` alone" in step0)

        # A write is proven by reading it back, not by having issued it.
        check("%s: the write is confirmed by reading it back" % label,
              "read it back" in step0)

        # The actual defect: reasoning from a property of the folder to a refused write.
        check("%s: inferring the outcome from the folder is forbidden" % label,
              "never infer the outcome from a property of" in step0)
        check("%s: the OneDrive reasoning is named as wrong, not left implicit" % label,
              "OneDrive" in step0)

        # "State will not persist" with no error named is the `unreadable` defect again.
        check("%s: a genuine fallback has to name what refused it" % label,
              "name what refused it" in step0)

        # A run left a 6 KB `log.gz.b64` in the workspace folder and could not delete it
        # (reported 2026-08-28) - the second improvisation into this gap after `_to_delete/`.
        # Both times the rule was present and listed *mechanisms* ("no temp file, no
        # write-then-move"), which a transfer encoding does not obviously match. The property
        # is what has to be stated, so these assert the property rather than the list.
        check("%s: the folder's permitted contents are an allowlist, not a list of bad habits"
              % label, "the only files that may exist in this folder" in step0)
        check("%s: staging a file to move bytes in or out is forbidden by name" % label,
              "never stage a file to move bytes into or out of this folder" in step0)
        check("%s: re-encoded copies are named, since that is the form it took" % label,
              all(w in step0 for w in ("base64-encoded", "chunked")))
        check("%s: the alternative is stated, not just the prohibition" % label,
              "Write the destination file itself" in step0)
        check("%s: an impossible write is `refused`, never a workaround that leaves a stray"
              % label, "not a workaround that leaves something behind" in step0)


# ------------------------------------------------------- 8. PO identity rules
def test_dashboard_view():
    """The toolbar had no coverage at all, and the default sort is the one setting every
    reader lands on without choosing it. Three things are guarded here, each of which has
    already failed once in some form: a default that cannot reach an existing user, a
    comparator that is not a valid comparator, and a sticky rule with no room to travel."""
    for label, root, key, oldkey in (("netsuite", NS, "ns_view_v2", "ns_view_v1"),
                                     ("procore",  PC, "pc_view_v3", "pc_view_v2")):
        tpl = open(os.path.join(root, "assets", "dashboard_template.html"), encoding="utf-8").read()

        m = re.search(r"var DEFV=\{sort:\"(\w+)\"", tpl)
        check("%s: default sort is newest" % label, bool(m) and m.group(1) == "newest",
              "found %s" % (m.group(1) if m else "no DEFV"))

        # A new default that ships under the old storage key reaches nobody who has ever
        # touched the toolbar - their stored view simply overrides it, for good.
        check("%s: view key was bumped with the default" % label, 'VKEY="%s"' % key in tpl)
        check("%s: the previous view key is migrated, not dropped" % label,
              'OLDVKEY="%s"' % oldkey in tpl and "delete sv.sort" in tpl)

        # Returning 1 for both orderings when both dates are absent is not a valid
        # comparator; an engine may produce any order from it.
        check("%s: the date comparator handles both-null" % label,
              "if(ad==null&&bd==null)return 0;" in tpl)

        # position:sticky resolves against the PARENT box. On .bar the parent is exactly as
        # tall as the bar, so it never travels - measured in a real browser, not assumed.
        # Asserts the mechanism, not the styling: pinning .bar's full declaration string
        # here made a pure restyle read as a sticky regression (2026-08-21).
        m_bar = re.search(r"\.bar\{[^}]*\}", tpl)
        check("%s: sticky sits on #bar, not .bar" % label,
              "#bar{position:sticky" in tpl and bool(m_bar) and "sticky" not in m_bar.group(0))
        check("%s: the sticky bar has a container to travel in" % label,
              'class="worksec"' in tpl and ".worksec{position:relative}" in tpl)

        # CLAUDE.md has asserted since 2026-08-19 that a test covers this. Until now it did
        # not. A marked item hidden behind a filter still has to execute, so narrowing the
        # bar to the filtered rows would silently discard decisions already made.
        bar = re.search(r"function renderBar\(\)\{(.*?)\n\}", tpl, re.S)
        check("%s: renderBar is present" % label, bool(bar))
        if bar:
            body = bar.group(1)
            check("%s: renderBar counts REVIEW.items, never the filtered rows" % label,
                  "REVIEW.items" in body and "applyView" not in body)

        # The execute affordance has to exist before anything is marked, or step 2 is
        # invisible until the reader has already worked out step 1 unaided.
        if bar:
            check("%s: the bar renders unconditionally, zero marks included" % label,
                  'getElementById("bar").innerHTML=\'<div class="bar">\'' in bar.group(1) and
                  'getElementById("bar").innerHTML=\'<p class="note"' not in bar.group(1))
        check("%s: the header mirror is wired" % label,
              'id="topexec"' in tpl and 'getElementById("topexec")' in tpl)

        # ---- the floating header ------------------------------------------------------
        # The frame is sized to its own content and the HOST scrolls, so nothing in CSS can
        # pin anything: measured in Chromium, window.innerHeight === document.scrollHeight
        # and window.scrollY stays 0. #floathdr is therefore placed from JavaScript against
        # a band read through IntersectionObserver, whose intersectionRect is clipped by
        # ancestor viewports across the cross-origin boundary. These assertions pin the
        # mechanism; the positions themselves need a browser (scripts/measure_float.js).
        check("%s: the floating header and its sentinel are in the markup" % label,
              'id="floathdr"' in tpl and 'id="bandsen"' in tpl)
        check("%s: the floating header has a containing block to be placed in" % label,
              ".wrap{position:relative}" in tpl and "#floathdr{position:absolute" in tpl)
        m_float = re.search(r"#floathdr\{[^}]*\}", tpl)
        check("%s: the floating header is NOT sticky - it has nowhere to travel" % label,
              bool(m_float) and "sticky" not in m_float.group(0) and "fixed" not in m_float.group(0))

        # A scroll listener is the obvious-looking way to do this and it is dead code here:
        # this document never scrolls, so the event never fires and the bar never moves.
        check("%s: the band is not tracked by a scroll event" % label,
              'addEventListener("scroll"' not in tpl and "onscroll" not in tpl)

        # One full-height sentinel is the trap. Thresholds are ratios, so a 700px viewport
        # over a 4,000px sentinel stays at 17% however far you scroll and no threshold is
        # ever crossed - observed at 4 callbacks for a whole page, with a stale band at
        # three of six offsets. Contiguous tiles are what make the top edge readable.
        check("%s: the sentinel is a tiled column, not one full-height element" % label,
              "BAND_TILE" in tpl and "bandBuild" in tpl and "sen.appendChild(t)" in tpl)
        check("%s: the observer gets a threshold list, not a single ratio" % label,
              "for(var i=0;i<=20;i++)th.push(i/20)" in tpl and "{threshold:th}" in tpl)

        # Filtering the queue changes the page height. Tiles that stopped short of the new
        # bottom read as "off screen" down there, and the bar would vanish mid-queue.
        check("%s: re-tiling is wired to the page's height, not to a render path" % label,
              "new ResizeObserver(function(){bandBuild()}).observe(" in tpl)

        # The bar duplicates controls that are already in the page, so it is out of the tab
        # order and hidden from screen readers rather than announced twice.
        check("%s: the floating bar is a visual duplicate only" % label,
              'id="floathdr" aria-hidden="true"' in tpl and 'tabindex="-1"' in tpl)


def test_po_identity_rules():
    """A bill's PO must come from the transaction linkage, never from the typed
    `custbody3` reference. Reading the typed field as the coding produced
    confident, false "coded to the wrong PO" flags on correctly coded bills
    (observed 2026-08-20 on five of five bills). These assertions guard the
    specific queries whose absence caused it - if someone reverts the SQL, this
    goes red rather than the next reviewer's queue going wrong."""
    src = open(os.path.join(NS, "SKILL.md"), encoding="utf-8").read()
    # Prose in this file gets re-wrapped, so match sentences against a
    # whitespace-flattened copy. A rewrap must not silently retire a guard.
    flat = re.sub(r"\s+", " ", src)

    sql = re.findall(r"```sql\n(.*?)```", src, re.S)
    link_q = [q for q in sql if "previoustransactionlinelink" in q]
    check("po: the linkage table is queried", len(link_q) >= 2,
          "found %d queries using it" % len(link_q))
    check("po: EVERY linkage query filters to the order-to-bill link",
          bool(link_q) and all("linktype = 'OrdBill'" in q for q in link_q),
          "%d of %d filter" % (sum("linktype = 'OrdBill'" in q for q in link_q), len(link_q)))
    check("po: ShipRcpt double-counting is called out", "ShipRcpt" in src)
    check("po: the per-line-pair fan-out is warned about",
          "one row per line pair" in flat)
    check("po: aggregates are deduplicated to distinct bills",
          "SELECT DISTINCT" in src and "distinct bill ids" in flat)

    check("po: the typed field is aliased as typed, not as the ref",
          "custbody3 AS po_typed" in src and "custbody3 AS po_ref" not in src)
    check("po: the PO pull keys on the linkage id, not a document-number string",
          "WHERE t.id IN (<po_id" in src and "WHERE t.tranid IN ('PO____')" not in src)

    for state in ("linked", "unlinked", "failed"):
        check("po: state %r is named" % state, "`%s`" % state in src)
    check("po: the three states are not collapsible",
          "Never collapse these three" in flat)

    check("po: a typed mismatch is a data-entry note, not a misallocation",
          "data-entry note" in flat)
    check("po: a typed mismatch never flags an item on its own",
          "never makes an item `flagged` on its own" in flat)
    check("po: a zero billed-to-date is not a finding",
          "A zero is not a finding" in flat)
    check("po: billed-to-date and pending are kept apart",
          "Do not fold pending into billed-to-date" in flat)
    check("po: the memo-derived poContext route is retired",
          "Never derive a `poContext` figure from a vendor-plus-memo search" in flat)


# ----------------------------------------------------------- 9. NetSuite poLine
def test_po_line():
    """The dashboard must keep the three PO states distinct. Rendering an
    `unlinked` or `failed` PO the same way as a `linked` one would present an
    unconfirmed PO as confirmed - the same misfile the skill just removed."""
    tpl = open(os.path.join(NS, "assets", "dashboard_template.html"), encoding="utf-8").read()
    m = re.search(r"(function poLine\(it\)\{.*?\n\})", tpl, re.S)
    if not m:
        sys.exit("ABORT: poLine() not found in the NetSuite dashboard template. This "
                 "test extracts it from the template on purpose - if it moved, fix "
                 "this test rather than duplicating the function.")
    script = ("function esc(s){return String(s==null?'':s)}\n" + m.group(1) + """
var out = {
  linked:   poLine({poRef:"PO16093", poLink:"linked"}),
  unlinked: poLine({poRef:"PO16093", poLink:"unlinked"}),
  failed:   poLine({poRef:"PO16093", poLink:"failed"}),
  empty:    poLine({})
};
console.log(JSON.stringify(out));
""")
    code, out, err = run_node(script)
    if code != 0:
        check("poLine runs", False, (err.splitlines() or ["non-zero exit"])[0])
        return
    r = json.loads(out)
    warn = "var(--warn-fg)"
    check("poLine: linked names the applied PO", "PO16093" in r["linked"] and "Applied to" in r["linked"])
    check("poLine: linked is not warn-coloured", warn not in r["linked"])
    check("poLine: unlinked says no PO is applied", "No PO applied" in r["unlinked"])
    check("poLine: unlinked is visibly unconfirmed", warn in r["unlinked"])
    check("poLine: unlinked still names what the record claims", "PO16093" in r["unlinked"])
    check("poLine: failed says the linkage was not read", "could not be read" in r["failed"])
    check("poLine: failed is NOT rendered as unlinked",
          "No PO applied" not in r["failed"] and warn in r["failed"])
    check("poLine: the three states are mutually distinct",
          len({r["linked"], r["unlinked"], r["failed"]}) == 3)
    check("poLine: an older payload renders nothing rather than guessing", r["empty"] == "")


# ------------------------------------------- 12. custom tool subtypes (`icr`)
def test_custom_tool_subtype():
    """A GenericToolItem's record link and cost fields come from its own custom tool.

    One queue carried two custom tools - Internal Change Risk and Customer Change Request,
    the second one 37 of 62 items - and the config had only ever been told about one. Every
    one of those 37 got a link built with the other tool's id, which resolves to a real page
    in the wrong tool rather than 404ing, and cost fields read through a mapping that does not
    describe them. Fail closed on both: no link rather than a wrong one, and an item whose
    cost checks could not run is not `clear`.
    """
    d = tempfile.mkdtemp()
    try:
        assets = os.path.join(PC, "assets")
        for f in ("publish_dashboard.py", "dashboard_template.html"):
            shutil.copy(os.path.join(assets, f), d)
        base = {"projectId": "9", "kind": "icr", "project": "A - B", "counterparty": "X",
                "amount": 1000, "step": "Cost Gate", "responses": ["Yes", "Reject"],
                "verdict": "clear", "head": "h", "facts": ["f"], "detail": "d"}
        cfg = {"company": "0", "customTools": {
            "Internal Change Risk (88)": {"toolId": "88", "costFields": {
                "vendorProposed": "custom_field_1", "compassAccepted": "custom_field_2"}},
            "Customer Change Request (77)": {"toolId": "77", "costFields": {
                "romCost": "custom_field_3"}}}}
        log = {"lastCompletedRun": "2026-09-01", "lastRunTime": "2026-09-01 09:00",
               "suppressed": 0, "config": cfg, "items": {
                   "icr": dict(base, itemId="111", docNo="#ICR-1",
                               subtype="Internal Change Risk (88)"),
                   "ccr": dict(base, itemId="222", docNo="#CCR-1",
                               subtype="Customer Change Request (77)"),
                   "unmapped": dict(base, itemId="333", docNo="#NEW-1",
                                    subtype="Some Other Tool (99)"),
                   "nosubtype": dict(base, itemId="444", docNo="#OLD-1", verdict="flagged")}}
        json.dump(log, open(os.path.join(d, "_procore_review_log.json"), "w"))
        out_html = os.path.join(d, "index.html")
        r = subprocess.run([sys.executable, "-B", os.path.join(d, "publish_dashboard.py"),
                            out_html], capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            check("publish script runs (subtypes)", False,
                  (r.stderr or r.stdout).strip().splitlines()[-1:] or "")
            return
        blob = re.search(r"/\*__REVIEW_DATA__\*/(.*?)/\*__END__\*/",
                         open(out_html, encoding="utf-8").read(), re.S).group(1)
        items = {i["doc"]: i for i in json.loads(blob)["items"]}
        check("subtype: each tool keeps its own tool id",
              items["#ICR-1"]["toolId"] == "88" and items["#CCR-1"]["toolId"] == "77",
              "%s / %s" % (items["#ICR-1"]["toolId"], items["#CCR-1"]["toolId"]))
        check("subtype: an unmapped subtype gets no tool id rather than another tool's",
              items["#NEW-1"]["toolId"] == "", items["#NEW-1"]["toolId"])
        check("subtype: an unmapped subtype cannot stay clear",
              items["#NEW-1"]["verdict"] == "skipped", items["#NEW-1"]["verdict"])
        check("subtype: it keeps its response buttons - the gate is unaffected",
              items["#NEW-1"]["resp"] == ["Yes", "Reject"])
        check("subtype: an item with no subtype recorded is not guessed either",
              items["#OLD-1"]["toolId"] == "")
        check("subtype: a flagged item stays flagged - a flag found is still a flag",
              items["#OLD-1"]["verdict"] == "flagged", items["#OLD-1"]["verdict"])
        check("subtype: the demotion is announced, not silent",
              "Some Other Tool (99)" in (r.stdout + r.stderr))

        # A config predating customTools describes exactly one tool, and must keep working.
        log["config"] = {"company": "0", "icrToolId": "88"}
        json.dump(log, open(os.path.join(d, "_procore_review_log.json"), "w"))
        r2 = subprocess.run([sys.executable, "-B", os.path.join(d, "publish_dashboard.py"),
                             out_html], capture_output=True, text=True, timeout=60)
        blob = re.search(r"/\*__REVIEW_DATA__\*/(.*?)/\*__END__\*/",
                         open(out_html, encoding="utf-8").read(), re.S).group(1)
        items = {i["doc"]: i for i in json.loads(blob)["items"]}
        check("subtype: a pre-customTools config still links every row",
              r2.returncode == 0 and all(items[k]["toolId"] == "88" for k in items),
              {k: items[k]["toolId"] for k in items})

        # The template must read the item's tool id, not only the config-level floor.
        tpl = open(os.path.join(d, "dashboard_template.html"), encoding="utf-8").read()
        rec = tpl[tpl.index("function recUrl"):]
        rec = rec[:rec.index("\n}")]
        check("subtype: recUrl prefers the item's own tool id", "it.toolId" in rec)
        check("subtype: recUrl returns no link rather than a wrong one",
              "if(!tid) return " in rec)
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------ 13. a large render survives a read
def test_render_fits_one_read():
    """The rendered dashboard has to be readable before it can be handed to show_widget.

    A widget takes its HTML inline, so rendering means reproducing the file through a tool
    call - which means reading it first. On 2026-09-01 a 62-item Procore queue published to
    2,834 lines, past a default file read, and the run declined to render it. serialise()
    emits one compact line per item for that reason. This pins both axes: the line count a
    default read has to cover, and no single line long enough to be truncated on its own.

    Bounds, not thresholds: they are properties of the read, and the point is that a real
    queue stays well inside them. 62 items is the largest queue observed.
    """
    for name, root, log in (("procore", PC, _big_procore_log()),
                            ("netsuite", NS, _big_netsuite_log())):
        d = tempfile.mkdtemp()
        try:
            assets = os.path.join(root, "assets")
            for f in ("publish_dashboard.py", "dashboard_template.html"):
                shutil.copy(os.path.join(assets, f), d)
            stem = "_procore_review_log.json" if name == "procore" else "_netsuite_review_log.json"
            json.dump(log, open(os.path.join(d, stem), "w"))
            out_html = os.path.join(d, "index.html")
            r = subprocess.run([sys.executable, "-B", os.path.join(d, "publish_dashboard.py"),
                                out_html], capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                check("%s: publish script runs (large queue)" % name, False,
                      (r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout)
                      else "non-zero exit")
                continue
            text = open(out_html, encoding="utf-8").read()
            lines = text.split("\n")
            check("%s: a 62-item render fits one default file read" % name,
                  len(lines) < 2000, "%d lines" % len(lines))
            check("%s: no single line is long enough to truncate on its own" % name,
                  max(len(l) for l in lines) < 8000,
                  "longest %d chars" % max(len(l) for l in lines))
            blob = re.search(r"/\*__REVIEW_DATA__\*/(.*?)/\*__END__\*/", text, re.S).group(1)
            payload = json.loads(blob)
            check("%s: the compact payload still parses" % name,
                  len(payload["items"]) == 62, len(payload.get("items", [])))
            check("%s: one line per item, not one line for all of them" % name,
                  blob.count("\n") >= 62, blob.count("\n"))
        finally:
            shutil.rmtree(d, ignore_errors=True)


def _filler():
    """Field lengths in the range a real write-up produces - the byte count is the test."""
    return {"head": "Arithmetic ties; the accepted cost matches the attached proposal total.",
            "facts": ["Cost Impact $412,880.00 = accepted $412,880.00 (status yes_known).",
                      "Proposal total $412,880.00 located verbatim on page 2 of the support.",
                      "Phase lines sum to $412,880.00; proposed $451,200.00, accepted lower."],
            "detail": ("Cost Impact is recorded as yes_known at $412,880.00 and the accepted "
                       "cost carries the same figure, so check 1 ties. The attached proposal "
                       "parsed as text and its total appears verbatim on page 2, so check 2 "
                       "ties to accepted rather than to proposed. The phase lines sum to the "
                       "same total. No placeholder value is present. Two narrative fields are "
                       "blank and neither prevents judging the cost." * 2),
            "context": "Commitment 4488213 · 6.08% complete · balance to finish $9,412,004.00",
            "warning": ("The proposal is dated eleven days after the change risk was raised "
                        "and its entitlement narrative names no RFI.")}


def _big_procore_log():
    items = {}
    for n in range(62):
        items["GenericToolItem:%d" % (900000 + n)] = dict(
            _filler(), itemId=str(900000 + n), projectId=str(4400 + n % 9),
            commitmentId=str(4488000 + n), supportRead=["PCI %d — proposal.pdf" % n],
            kind="icr", subtype="Internal Change Risk (88)", type="Internal Change Risk",
            docNo="ICR-%04d · CR-%03d" % (n, n),
            project="Campus %d - Building %d" % (n % 3 + 1, n % 6 + 1),
            counterparty="Example Mechanical Contractors of the Midwest LLC",
            amount=412880 + n * 1013, dueDate="2026-09-%02d" % (n % 28 + 1),
            step="Financial Analyst Review", responses=["Approve", "Revise and Resubmit"],
            verdict=("clear", "flagged")[n % 2], reviewedOn="2026-09-01",
            attachments=["Proposal-%04d-Final.pdf" % n])
    return {"lastCompletedRun": "2026-09-01", "lastRunTime": "2026-09-01 09:12",
            "suppressed": 41,
            "config": {"company": "0", "customTools": {
                "Internal Change Risk (88)": {"toolId": "88", "costFields": {}}}},
            "items": items}


def _big_netsuite_log():
    """Keyed by record id, and poContext/poWarning where Procore has context/warning."""
    items = {}
    for n in range(62):
        f = _filler()
        items[str(2530000 + n)] = {
            "type": "Bill", "docNo": "BILL-%05d" % n,
            "vendor": "Example Mechanical Contractors of the Midwest LLC",
            "amount": 412880 + n * 1013, "trandate": "2026-08-%02d" % (n % 28 + 1),
            "verdict": ("clear", "flagged")[n % 2], "reviewedOn": "2026-09-01",
            "head": f["head"], "facts": f["facts"], "detail": f["detail"],
            "poContext": f["context"], "poWarning": f["warning"],
            "poRef": "PO16093", "poLink": "linked",
            "attachmentFile": "Invoice-%05d.pdf" % n}
    return {"lastCompletedRun": "2026-09-01", "lastRunTime": "2026-09-01 09:12",
            "config": {"me": "0", "tool": "0", "account": "0"}, "items": items}


def main():
    print("Skill code checks\n")
    if shutil.which("node"):
        test_extractor()
        test_page_budget()
        test_gate_states()
        test_sniff()
        test_sheets()
        test_po_line()
    else:
        print("  SKIP  node not on PATH - extractor, page budget, gate states, "
              "sniff, sheets and poLine not run")
    test_cco_demotion()
    test_commitment_kind()
    test_custom_tool_subtype()
    test_render_fits_one_read()
    test_template_version()
    test_step0_write_states()
    test_dashboard_view()
    test_po_identity_rules()
    print()
    if failures:
        print("FAILED: " + "; ".join(failures))
        sys.exit(1)
    print("OK: all skill code checks passed")


if __name__ == "__main__":
    main()
