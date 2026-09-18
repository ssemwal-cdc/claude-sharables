---
id: pending
slug: sticky-fails-cross-origin-iframe
kind: finding
status: observed
date: 2026-08-27
---
# CSS sticky cannot survive a cross-origin frame

**Outcome protected.** A reader mid-queue has the filter state and the commit button on
screen.

**Argument.** The question was whether the header can persist while scrolling.
In CSS it cannot.

Reproduced in Chromium, the window height equals the document scroll height
and the scroll offset never leaves zero.
So a fixed position freezes at a document coordinate exactly as sticky does.

**Evidence.** Closed 2026-08-27.
One full-height sentinel with 401 thresholds gave 4 callbacks for a whole page
of scrolling. It also gave a stale band at 3 of 6 offsets.

**Checks.** `test_dashboard_view` pins the mechanism, mutation-tested.
