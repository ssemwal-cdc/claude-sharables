---
id: F133
slug: tiled-sentinels-beat-single-sentinel
kind: finding
status: observed
date: 2026-08-27
---
# Tiled sentinels track the band, one big one does not

**Outcome protected.** A reader mid-queue has the filter state and the commit button on
screen.

**Argument.** The instrument has to be a column of contiguous tiles, and that is the
whole trick.
Thresholds are ratios.
A 700px viewport over a 4,000px sentinel is 17% of it, and stays 17%
however far you scroll. So nothing is ever crossed.

Tiled at 100px, the tile straddling the top edge of the band is clipped by
that edge.
So its rectangle top is the band top exactly. Its own visible ratio
changes continuously, which keeps the callbacks coming.

Do not replace the tiles with one sentinel, and do not reach for a scroll
listener.
This document never scrolls, so the event never fires.

**Evidence.** Closed 2026-08-27.
One full-height sentinel with 401 thresholds gave 4 callbacks for a whole page
of scrolling. It also gave a stale band at 3 of 6 offsets.

**Checks.** `test_dashboard_view` pins the mechanism, mutation-tested.
