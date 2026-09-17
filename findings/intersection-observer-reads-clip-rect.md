---
id: pending
slug: intersection-observer-reads-clip-rect
kind: finding
status: observed
date: 2026-08-27
---
# An observer reads scroll position across a frame

**Outcome protected.** A reader mid-queue has the filter state and the commit button on
screen.

**Argument.** What does reach across the frame boundary is an intersection observer.
Its intersection rectangle is clipped by every ancestor viewport, cross-origin
ones included.

So from inside the widget it is possible to read which slice of the page the
reader is looking at.
The root bounds come back null.
The clipped rectangle does not, and the clipped rectangle is all this needs.

**Evidence.** Closed 2026-08-27.
The tiled column measured 0.0px error at every offset, against a
window-scrolling host and a div-scrolling host.
It gave a distinct position for all 26 steps of an 8px-step scroll.

**Checks.** `test_dashboard_view` pins the mechanism, mutation-tested.
