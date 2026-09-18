// Cut from `scripts/measure_float.js` by review-only-mode. Verbatim; do not edit.

// ===== scripts/measure_float.js lines 174-183 =====
// The marked-item and Execute-button assertions of suite(). The localStorage.clear that
// followed them stays live because the run still leaves the frame clean.
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
