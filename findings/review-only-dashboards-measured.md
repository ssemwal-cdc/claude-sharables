---
id: pending
slug: review-only-dashboards-measured
kind: finding
status: observed
date: 2026-09-18
---
# Review-only dashboards measured

**Outcome protected.** A reviewer sees the whole queue, with no control they cannot use.

**Argument.**

D‹review-only-mode›, review-only plugins, step 9 asks for the float measurement after the cut.
Run on 2026-09-18 with `scripts/measure_float.js --shots`, after the execute assertions moved to `actionable-retired/`.

Every measurement passed for both dashboards. The float header still tracks every scroll offset. The Filters link still returns to the toolbar.

Eighteen captures, three widths, two schemes. No capture has a horizontal overflow.

Read by eye, three captures. NetSuite at 1200 light, Procore at 1200 dark, NetSuite at 390 dark.
Verdict per screen: PASS, PASS, PASS. No button, no bar, no mirror. Each row keeps its link and its detail toggle.

**Evidence.**

- Page heights fell. NetSuite at 1200 is 5471px. Procore at 1200 is 6162px. The bar's 153px, measured in D45, keep reference text out, is gone from each.
- The measurement script itself carried eight lines of execute assertions the record did not list. They were cut into `actionable-retired/scripts/measure_float.cut.js`, and the README map names them.

**Checks.** `NODE_PATH=$(npm root -g) node scripts/measure_float.js --shots .claude/shots`, by hand.
