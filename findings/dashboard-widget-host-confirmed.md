---
id: F157
slug: dashboard-widget-host-confirmed
kind: finding
status: observed
date: 2026-09-24
---
# Dashboard bar confirmed in widget host

**Outcome protected.** The reader can see the item count and reach Filters wherever they are in
the queue.

**Argument.** `position:sticky` does nothing on the widget host.
The widget frame auto-sizes while the conversation scrolls, so a sticky bar degrades silently to
an ordinary block.
That is why the header mirror exists and must not be deleted as redundant.
The header mirror is the half that works on either host.
A floating bar replaced the sticky one.
It reads the visible band with `IntersectionObserver` across the frame boundary.
`scripts/measure_float.js` measures that bar from fixtures and is reproducible.
The bar itself never worked as a plain sticky element.
The float mechanism is why it works now.

**Evidence.** Reported 2026-09-24 by the maintainer: scrolling halfway down a real dashboard
shows a thin bar pinned at the top.
It carries the item count and Filters.
Measured: 0.0px band error at every offset, and a distinct position for 26 steps of an 8px
scroll, from fixtures.
The bar measures 153px on both dashboards.
The full header is about 380px against a 700px viewport.
The real-queue-size overlay behavior was not asked.
At 43 or 73 items, not the 6-8 item fixtures, it stays `unmeasured`.

**Checks.** `test_dashboard_view` pins the mechanism.
`scripts/measure_float.js` measures position by hand.
