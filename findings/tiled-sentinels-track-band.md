---
id: F84
slug: tiled-sentinels-track-band
kind: finding
status: observed
date: 2026-08-27
---
# Tiled sentinels track the band

**Outcome protected.** A reader mid-queue has the filter state and the commit button on screen.

**Argument.**

The question was whether the header can persist while scrolling. In CSS it cannot.

Reproduced in Chromium, the window height equals the document scroll height and the scroll offset never leaves zero. So a fixed position freezes at a document coordinate exactly as sticky does.

What does reach across the frame boundary is an intersection observer. Its intersection rectangle is clipped by every ancestor viewport, cross-origin ones included.

So from inside the widget it is possible to read which slice of the page the reader is looking at. The root bounds come back null. The clipped rectangle does not, and the clipped rectangle is all this needs.

The instrument has to be a column of contiguous tiles, and that is the whole trick.

Thresholds are ratios. A 700px viewport over a 4,000px sentinel is 17% of it and stays 17% however far you scroll, so nothing is ever crossed.

Tiled at 100px, the tile straddling the top edge of the band is clipped by that edge. So its rectangle top is the band top exactly, and its own visible ratio changes continuously, which keeps the callbacks coming.

Do not replace the tiles with one sentinel, and do not reach for a scroll listener. This document never scrolls, so the event never fires.

Re-tiling hangs off a resize observer on the wrapper, not off a render path. Filtering the queue and opening a detail both change the page height, and tiles that stop short of the new bottom read as off screen down there.

Observing the wrapper covers every cause including the first layout, so no render path has to remember. The sentinel column is absolutely positioned and adds no height, so it cannot feed itself.

The floating bar is a way back to the header, not a replacement for it. Its filter control scrolls the real toolbar into view, which does move the host scroller from inside a cross-origin frame.

What floats is only what is worth having in the second before a click. That is the filter state, one press back, and the commit button.

It is a visual duplicate, so it is hidden from assistive technology and removed from the tab order throughout. These are controls already in the page.

The count on it follows the filter and the execute mirror does not. That is the same split as D46, the execute bar ignores the filter.

**Evidence.**

- Closed 2026-08-27. One full-height sentinel with 401 thresholds gave 4 callbacks for a whole page of scrolling, and a stale band at 3 of 6 offsets.
- The tiled column measured 0.0px error at every offset, against a window-scrolling host and a div-scrolling host. It gave a distinct position for all 26 steps of an 8px-step scroll.
- The full header is about 380px. Reproducing it would cost half a 700px viewport.

**Checks.** `test_dashboard_view` pins the mechanism, mutation-tested. `scripts/measure_float.js` measures position by hand.
