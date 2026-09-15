---
id: pending
slug: ordbill-dedupe-line-pairs
kind: finding
status: observed
date: 2026-08-20
---
# Dedupe the link rows first

**Outcome protected.** A billed-to-date total is the truth, not a multiple of it.

**Argument.**

The bill link type filter is required, not optional. The same purchase order also emits receipt rows for the same bill.

The link table carries one row per line pair, not per document. A three-line bill returns three link rows.

So a naive sum across the join returns a multiple of the truth.

Deduplicate to distinct bill ids before aggregating, always.

**Evidence.**

- Observed 2026-08-20. A true 136,369.02 came back as 409,107.06, exactly three times.

**Checks.** `scripts/test_skill_code.py` runs the cross-check code.
