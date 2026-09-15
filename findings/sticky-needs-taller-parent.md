---
id: pending
slug: sticky-needs-taller-parent
kind: finding
status: observed
date: 2026-08-20
---
# Sticky resolves against its parent

**Outcome protected.** A pinned bar has somewhere to travel.

**Argument.**

A sticky position resolves against the parent box of the element.

The execute bar was first made sticky on an inner element whose parent is exactly as tall as it. That gives zero travel, with no error, and it looked done.

It was caught by measuring the viewport position of the bar at two scroll offsets in a real browser, not by reading the CSS.

It now sits on the outer element, inside a section that also holds the rows. That is what gives it a queue to float over.

The same measurement is the only honest way to check the next one.

**Evidence.**

- Measured 2026-08-20 in a real browser.
- The frame turned out not to scroll at all. See F‹widget-iframe-does-not-scroll›, the widget frame does not scroll.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
