// Measures the floating header in a real browser. NOT part of the build: it needs Chromium
// and Playwright, neither of which validate.py may assume. Run it by hand after touching
// dash-band-track, dash-float-css, dash-header-mirror or anything about the page's height:
//
//   NODE_PATH=$(npm root -g) node scripts/measure_float.js
//   CHROME_PATH=/path/to/chrome NODE_PATH=... node scripts/measure_float.js   # if the
//                                                                            # default fails
//
// It exists because everything this feature claims is positional, and position is the one
// thing the static checks in test_skill_code.py cannot see. The repo has twice shipped a
// pinned bar that was never pinned - #bar on .bar with zero travel, then #bar in a frame
// that turned out not to scroll - and both times the CSS read correctly. Only a measurement
// catches that, so this reproduces the host arrangement rather than describing it: the
// widget in a cross-origin iframe sized to its own content, with the parent doing the
// scrolling. Cross-origin matters - same-origin would let the frame read the parent, which
// it cannot do in the real host. The content-sized frame is what removes its scrollport and
// so what makes CSS sticky inert; suiteInternalScroll at the bottom measures the opposite
// arrangement too, because the band maths has to hold whichever side scrolls.
const http = require("http");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { execFileSync } = require("child_process");

const REPO = path.resolve(__dirname, "..");
const VH = 760;
const PLUGINS = [
  { label: "procore", file: "pc.html", log: "_procore_review_log.json",
    dir: "plugins/procore-open-items-review/skills/procore-open-items-review/assets" },
  { label: "netsuite", file: "ns.html", log: "_netsuite_review_log.json",
    dir: "plugins/netsuite-approval-review/skills/netsuite-approval-double-check/assets" },
];

let fails = 0;
const ck = (n, ok, d) => { if (!ok) fails++; console.log((ok ? "  ok  " : "  FAIL") + "  " + n + (d ? "   [" + d + "]" : "")); };

// ---- fixtures: enough items that the page is several viewports tall ---------------------
function fixtures(tmp) {
  const wide = n => ({
    head: "Ties to the cent against the signed support, and the split reconciles.",
    facts: ["Line one of the arithmetic for item " + n + ".",
            "Line two, naming the counterparty and the subsidiary.",
            "Line three, on fees and tax at order stage."],
    detail: "Detail line for item " + n + ".", verdict: n % 7 === 0 ? "flagged" : "clear",
  });
  const pc = {}, ns = {};
  for (let n = 0; n < 22; n++) pc["i" + n] = Object.assign({
    itemId: String(1000 + n), wfId: String(9000 + n), projectId: "9", commitmentId: "8",
    kind: "cco", type: "Purchase Order", docNo: "PO17" + String(n).padStart(3, "0"),
    project: "CAMPUS - Building " + (n % 5 + 1), counterparty: "Counterparty " + n,
    amount: 10000 + n * 137, step: "Review", dueDate: "9/" + (n % 28 + 1) + "/2026",
    responses: ["Approve", "With notes", "Reject"], supportRead: ["support.pdf"],
    poNote: "New commitment - this order is itself the commitment, no prior billings.",
  }, wide(n));
  for (let n = 0; n < 20; n++) ns[String(2500000 + n)] = Object.assign({
    type: "Bill", docNo: "B" + String(n).padStart(5, "0"), vendor: "Vendor " + n,
    amount: 20000 + n * 211, trandate: "8/" + (n % 28 + 1) + "/2026",
    attachmentFile: "support.pdf",
  }, wide(n));

  const serve = path.join(tmp, "serve");
  fs.mkdirSync(serve, { recursive: true });
  for (const p of PLUGINS) {
    const work = path.join(tmp, p.label);
    fs.mkdirSync(work, { recursive: true });
    for (const f of ["publish_dashboard.py", "dashboard_template.html"])
      fs.copyFileSync(path.join(REPO, p.dir, f), path.join(work, f));
    const items = p.label === "procore" ? pc : ns;
    const cfg = p.label === "procore" ? { company: "0", icrToolId: "0" }
                                      : { me: 42, account: "1", tool: "t" };
    fs.writeFileSync(path.join(work, p.log), JSON.stringify({
      lastCompletedRun: "2026-08-27", lastRunTime: "2026-08-27 13:25",
      suppressed: 10, config: cfg, items: items }));
    execFileSync("python3", [path.join(work, "publish_dashboard.py"),
                             path.join(serve, p.file)], { stdio: "pipe" });
  }
  return serve;
}

// A host page that only does what the real one does: hold the widget in a scrolling column.
const HOST = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>host</title>
<style>body{margin:0;font:14px sans-serif}#sc{height:100vh;overflow-y:auto;background:#e8e8e6}
.sp{padding:40px 20px}iframe{display:block;width:920px;border:0;margin:0 auto}</style></head>
<body><div id="sc"><div class="sp" style="height:320px">turn above</div>
<iframe id="w" scrolling="no" height="600"></iframe>
<div class="sp" style="height:700px">turn below</div></div>
<script>var q=new URLSearchParams(location.search),w=document.getElementById('w');
if(q.get('fixed')){w.setAttribute('scrolling','yes');w.setAttribute('height',760);
  document.getElementById('sc').style.height='auto'}
w.src='http://127.0.0.1:8092/'+q.get('d');</script></body></html>`;

function servers(serve) {
  const host = http.createServer((q, r) => { r.writeHead(200, { "Content-Type": "text/html; charset=utf-8" }); r.end(HOST); });
  const kid = http.createServer((q, r) => {
    const f = path.join(serve, path.basename(decodeURIComponent(q.url.split("?")[0])));
    if (!fs.existsSync(f)) { r.writeHead(404); return r.end("no"); }
    r.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    r.end(fs.readFileSync(f));
  });
  host.listen(8091, "127.0.0.1");
  kid.listen(8092, "127.0.0.1");
  return () => { host.close(); kid.close(); };
}

async function suite(page, p) {
  console.log("\n=== " + p.label + " ===");
  await page.goto("http://127.0.0.1:8091/?d=" + p.file);
  await page.waitForTimeout(700);
  // Match on the origin, not the filename: the host's own URL carries the filename in its
  // query string and matching that picks the parent frame, which has no #floathdr in it.
  const fr = page.frames().find(f => f.url().startsWith("http://127.0.0.1:8092/"));
  if (!fr) return ck(p.label + ": widget frame loaded", false);

  // The host sizes the frame to the widget's content. That is what removes its scrollport.
  const ch = await fr.evaluate(() => document.documentElement.scrollHeight);
  await page.evaluate(h => document.getElementById("w").setAttribute("height", h), ch);
  await page.waitForTimeout(500);

  const inner = await fr.evaluate(() => ({ ih: innerHeight, sh: document.documentElement.scrollHeight, sy: scrollY }));
  ck("the frame has no scrollport of its own", inner.ih === inner.sh && inner.sy === 0, JSON.stringify(inner));
  ck("the page is several viewports tall (" + ch + "px vs " + VH + ")", ch > VH * 2);

  const sc = y => page.evaluate(o => document.getElementById("sc").scrollTop = o, y);
  const disp = () => fr.evaluate(() => getComputedStyle(document.getElementById("floathdr")).display);
  const box = async s => { const h = await fr.$(s); return h ? await h.boundingBox() : null; };

  await sc(0); await page.waitForTimeout(300);
  ck("no floating bar while the real header is on screen", (await disp()) === "none");
  const tiles = await fr.evaluate(() => document.querySelectorAll("#bandsen i").length);
  ck("sentinel tiled to the whole page (" + tiles + " tiles)", tiles >= Math.floor(ch / 100));

  let worst = -1; const spots = new Set();
  for (const y of [1200, 1900, 2600, 3400, 4100]) {
    await sc(y); await page.waitForTimeout(320);
    const b = await box("#floathdr .floatbar");
    if ((await disp()) === "none" || !b) { ck("host at " + y + ": bar is shown", false); continue; }
    spots.add(Math.round(b.y * 100) / 100 + "@" + y);
    worst = Math.max(worst, b.y);
    ck("host at " + y + ": bar fully on screen at viewport y=" + Math.round(b.y),
       b.y >= -1 && b.y + b.height <= VH + 1, "y=" + b.y.toFixed(1) + " h=" + b.height.toFixed(0));
  }
  ck("the bar tracked every offset rather than sticking at one", spots.size >= 4, spots.size + " of 5");
  ck("the bar rides the top edge (worst y=" + worst.toFixed(0) + ")", worst >= 0 && worst < 40);

  await sc(3400); await page.waitForTimeout(300);
  await (await fr.$("#floathdr button")).click();
  await page.waitForTimeout(500);
  const tb = await box(".toolbar");
  ck("Filters ↑ scrolls the host back to the real toolbar", !!tb && tb.y >= -1 && tb.y < VH,
     "toolbar y=" + (tb ? tb.y.toFixed(0) : "off screen"));
  ck("and the bar stands down once the real header is back", (await disp()) === "none");

  await sc(0); await page.waitForTimeout(200);
  await (await fr.$("#rows .row .acts button")).click();
  await page.waitForTimeout(250);
  await sc(2600); await page.waitForTimeout(320);
  ck("a marked item puts Execute on the bar, out of the tab order",
     await fr.evaluate(() => { const e = document.getElementById("floathdr");
       return /Execute/.test(e.textContent) && e.querySelectorAll('button[tabindex="-1"]').length >= 2; }));
  const eb = await box("#floathdr .go.big");
  ck("that Execute button is itself reachable on screen",
     !!eb && eb.y >= 0 && eb.y + eb.height <= VH, eb ? "y=" + eb.y.toFixed(0) : "off screen");
  await fr.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
}

// The other host arrangement: a frame with a scrollport of its own, which is what the
// 2026-08-26 report says this host is NOT - but the report is a report, and the band maths
// has to hold either way or the feature rests on it. It does hold, because intersectionRect
// and .wrap's own rect are read in the same client coordinate space, so subtracting one from
// the other gives the right offset whichever side did the scrolling.
async function suiteInternalScroll(page, p) {
  console.log("\n=== " + p.label + ", frame scrolling itself ===");
  await page.goto("http://127.0.0.1:8091/?d=" + p.file + "&fixed=1");
  await page.waitForTimeout(700);
  const fr = page.frames().find(f => f.url().startsWith("http://127.0.0.1:8092/"));
  const inner = await fr.evaluate(() => ({ ih: innerHeight, sh: document.documentElement.scrollHeight }));
  ck("the frame does have its own scrollport here", inner.ih < inner.sh, JSON.stringify(inner));
  for (const y of [900, 1800, 3000]) {
    await fr.evaluate(o => window.scrollTo(0, o), y);
    await page.waitForTimeout(350);
    const h = await fr.$("#floathdr .floatbar");
    const b = h ? await h.boundingBox() : null;
    ck("frame scrolled to " + y + ": bar on screen at y=" + (b ? Math.round(b.y) : "-"),
       !!b && b.y >= -1 && b.y + b.height <= VH + 1);
  }
}

(async () => {
  let chromium;
  try { ({ chromium } = require("playwright")); }
  catch (e) { console.error("needs playwright: NODE_PATH=$(npm root -g) node scripts/measure_float.js"); process.exit(2); }
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "floatmeasure-"));
  const stop = servers(fixtures(tmp));
  const opts = { args: ["--no-sandbox"] };
  if (process.env.CHROME_PATH) opts.executablePath = process.env.CHROME_PATH;
  const browser = await chromium.launch(opts);
  const page = await browser.newPage({ viewport: { width: 1000, height: VH } });
  page.on("pageerror", e => { console.log("  PAGE ERROR: " + e.message); fails++; });
  try {
    for (const p of PLUGINS) await suite(page, p);
    await suiteInternalScroll(page, PLUGINS[0]);
  }
  finally {
    await browser.close(); stop();
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  console.log("\n" + (fails ? fails + " FAILURE(S)" : "all measurements passed"));
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error("ERR", e); process.exit(1); });
