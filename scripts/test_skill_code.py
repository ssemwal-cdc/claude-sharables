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


# ------------------------------------------------------- 8. PO identity rules
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
    test_template_version()
    test_po_identity_rules()
    print()
    if failures:
        print("FAILED: " + "; ".join(failures))
        sys.exit(1)
    print("OK: all skill code checks passed")


if __name__ == "__main__":
    main()
