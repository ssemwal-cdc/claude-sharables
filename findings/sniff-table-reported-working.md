---
id: pending
slug: sniff-table-reported-working
kind: finding
status: observed
date: 2026-08-20
---
# The sniff table is working

**Outcome protected.** Nobody redesigns a working type check, and nobody cites an unfired branch.

**Argument.**

The sniff table was designed from a failure report rather than a reproduction.

It is now reported working. Real workbooks are read and real images are looked at.

That is a user report rather than a transcript, so it is weaker evidence than a record id. It is no longer a guess.

Two branches under it are still unfired and are not covered by that confirmation.

The first is the scanned branch, which rasterises a PDF that parsed and yielded almost nothing. That is not the same as an image attachment Chrome renders directly.

The second is the OCR fallback, along with the rule that an OCR figure never earns a clear verdict.

Do not cite either as established.

**Evidence.**

- Confirmed 2026-08-20 by the person running the plugins.
- The design is F‹attachment-sniff-six-outcomes›, six attachment outcomes.
- The unfired branches are `unmeasured`.

**Checks.** none
