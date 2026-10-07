---
id: pending
slug: inv-waiver-span
kind: decision
status: settled
date: 2026-10-07
---
# A waiver spanning pay apps is context or a warning

**Rule.** Check `pc.inv-waiver-span` compares a lien waiver naming several pay apps to the sum of their payment due. It never flags and never causes a skip.

**Outcome protected.** A valid multi-period waiver does not read as a defect.

**Argument.**

One waiver can cover several pay apps. A single-app comparison calls that a mismatch.

All apps in the run and summing gives a context line. Anything else gives a warning with figures.

A named pay app outside the queue gives a warning naming it.

**Evidence.**

- Owner ruling, 2026-10-07, from the 2026-10-07 field run.
- Registered under D66, declare checks in a registry.

**Checks.** `check_check_registry()` in `scripts/shared_blocks.py`.
