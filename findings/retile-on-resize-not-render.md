---
id: F131
slug: retile-on-resize-not-render
kind: finding
status: observed
date: 2026-08-27
---
# Re-tiling hangs off a resize, not a render

**Outcome protected.** A reader mid-queue has the filter state and the commit button on
screen.

**Argument.** Re-tiling hangs off a resize observer on the wrapper, not off a render
path.
Filtering the queue and opening a detail both change the page height.
Tiles that stop short of the new bottom then read as off screen down there.

Observing the wrapper covers every cause, including the first layout, so no
render path has to remember.
The sentinel column is absolutely positioned and adds no height, so it cannot
feed itself.

**Evidence.** Closed 2026-08-27.

**Checks.** `test_dashboard_view` pins the mechanism, mutation-tested.
