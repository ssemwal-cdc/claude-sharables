---
id: pending
slug: device-usability-check
kind: decision
status: open
date: 2026-09-15
---
# Device usability check

**Rule.** Check every screen at three widths and in both themes.

**Outcome protected.** The page works on the device the reader actually holds.

**Argument.** This is a usability check across devices.
It is not a documentation exception.
Three screens exist: the two dashboards and the onboarding sheet.
`scripts/measure_float.js` already reproduces the widget host and measures the floating bar.
It runs by hand, because `validate.py` may not assume a browser.
Extending it is cheap, because the harness already publishes both dashboards from fixtures.
The onboarding sheet was measured once at three widths and in both schemes.
That measurement was a one-off and no command repeats it.
A metric is not appearance.
A person still has to look at typography, spacing and hierarchy.

**Options.**

A. Leave the check as it is. Measure by hand when something looks wrong.

B. Extend `scripts/measure_float.js` to capture 390px, 1200px and 1600px in light and dark.
   Cover both dashboards and the onboarding sheet. Run it by hand and do not commit the images.

C. Do B and commit the images as a baseline.

**Recommendation.** B.
Run it by hand, because the check needs a browser.
Do not commit the images, because a binary baseline rots and nothing reads it.

**Evidence.** Deferred at the interview on 2026-09-15.
`scripts/measure_float.js` covers one arrangement per dashboard today.
Widths covered by a repeatable command today: zero.
The onboarding sheet measured 5,926px tall on desktop and 9,191px on mobile, once, on 2026-08-28.
F‹onboarding-copy-buttons›, measured at three widths in both schemes, is that one-off.
G‹dashboard-widget-host-unseen›, fixtures never committed, is why a one-off measurement is not enough.

**Checks.** `scripts/measure_float.js`, by hand, not in CI.
