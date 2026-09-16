---
id: F99
slug: device-shots-first-run
kind: finding
status: observed
date: 2026-09-15
---
# Device shots first run

**Outcome protected.** The three widths and the two themes are measured, not assumed.

**Argument.**

The first capture run produced 18 files and `summary.txt`. No screen overflows its viewport at any of the three widths.

`scrollWidth` equals the viewport width in all 18 captures. Overflow is 0px everywhere.

The page height changes with the width, as expected. The Procore dashboard is 8,927px tall at 390px and 6,765px at 1200px and at 1600px.

A person then read the six captures at 390px. Nothing is clipped and nothing is unreadable.

The stat tiles stay three across at 390px. Two labels wrap onto a second line, so those numbers sit lower than their neighbours.

The dashboard execute bar is `position:sticky`. A full-page capture paints it once, over the rows near the bottom edge of the first viewport. That overlap is a capture artefact and not a layout defect. `summary.txt` says so.

One product defect was seen while looking. Both templates write the `.po` element without an empty guard, so a row with no context text renders an empty grey strip.

**Evidence.**

- Run 2026-09-15 with `node scripts/measure_float.js --shots .claude/shots`. Playwright 1.56.1 and the bundled Chromium.
- 18 captures. Captures with overflow: 0. `scrollWidth` 390, 1200 and 1600 against viewports 390, 1200 and 1600.
- Heights at 390px: Procore 8,927px, NetSuite 7,344px, onboarding 9,060px.
- Heights at 1200px and at 1600px: Procore 6,765px, NetSuite 5,960px, onboarding 5,892px.
- The label that wraps at 390px is `GATE UNKNOWN` on Procore. `IN QUEUE` wraps onto a second tile row on NetSuite.
- The onboarding sheet drops its contents rail at 390px. In the two-column table the code column breaks `/netsuite-approval-double-check` across four lines.
- `.po` carries a background and padding in both templates. Procore fills it from the item key `context`. NetSuite fills it from `poContext`.
- The capture fixtures leave both keys empty, so the strip is empty in all 18 captures. Whether a real item can arrive with no context text is `unmeasured`.
- The float measurements printed 42 identical lines before and after the capture pass was added, checked by `diff`.
- D81, device usability check, is the rule this run serves.

**Checks.** `NODE_PATH=$(npm root -g) node scripts/measure_float.js --shots .claude/shots`, by hand.
