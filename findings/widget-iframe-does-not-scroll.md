---
id: F82
slug: widget-iframe-does-not-scroll
kind: finding
status: observed
date: 2026-08-26
---
# The widget frame never scrolls

**Outcome protected.** No version is spent fixing a defect this host cannot produce.

**Argument.**

The maintainer had never seen the sticky bar work, and the reason is mechanical.

The page renders inside a frame sized to its own content, with the parent scrolling. So a sticky bottom offset has zero travel.

The bar sits near the bottom of a long document and is simply not on screen while you work the queue. The header mirror is far above the viewport in the same arrangement.

So the earlier claim that the header mirror is guaranteed to work is true of rendering and false of reachability. Mid-queue there is no execute control on screen at all.

The overlap defect a scrolling frame produces cannot occur in this host. Do not spend a version fixing it.

The sticky rule stays anyway. It costs nothing and it starts working the day a host scrolls the frame.

**Evidence.**

- Reported 2026-08-26 and reproduced mechanically the same day. The bar sat at a fixed 3,874px down a 4,114px document, and the header mirror was 1,621px above the viewport.
- The overlap defect measured 5 row buttons returning the bar from a point hit test, so it is genuinely unclickable where a frame does scroll.
- The fix is F84, tiled sentinels track the band.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py` and `scripts/measure_float.js` by hand.
