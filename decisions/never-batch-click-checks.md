---
id: D18
slug: never-batch-click-checks
kind: decision
status: superseded
date: 2026-08-13
---
# Never batch the click checks

**Superseded by** D‹review-only-mode›, review-only plugins, on 2026-09-18. Execute mode was retired. The rule returns with it, and the text lives on in `actionable-retired/`.

**Rule.** Run the pre-click re-verification and the post-click verification per item. Never sweep them.

**Outcome protected.** A wrong record state stops the batch before the next click lands.

**Argument.**

These two are what an optimisation pass reaches for next, so both skills now say so in place.

The entire value of the pre-click re-verification is running in the moment before that one click.

The post-click verification catches more than connector lag. It catches an unexpected record state, a response that routed wrongly and a frozen tab.

Sweeping once at the end means every remaining click has already landed before any of that is visible.

Both were costed as small savings. Neither is worth the trade.

**Evidence.**

- Recorded 2026-08-13. The saving was costed as small. The figure is `unmeasured`.
- The lag case is F10, verify the record not queue.

**Checks.** none
