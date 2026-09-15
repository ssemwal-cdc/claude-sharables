---
id: D19
slug: return-rows-not-residuals
kind: decision
status: settled
date: 2026-08-13
---
# Return the rows, flattened

**Rule.** Compute the payment application identities in the page and return the residuals with the flattened rows.

**Outcome protected.** A review still catches the defect nobody specified a check for.

**Argument.**

Computing the six identities in the page and returning residuals is a tightening. Fixed arithmetic is more reliable in JavaScript than read off 50 KB of nested JSON.

Returning residuals alone was proposed and rejected.

A duplicated line, a zero-quantity line and a description that does not match the scope all survive a zero residual.

A reducer only finds what it was written to look for, and this review exists to catch what nobody specified.

So reduce the nesting, never the rows. The continuation sheet still comes back, flattened.

**Evidence.**

- Recorded 2026-08-13. The nested payload is about 50 KB. The reliability gain is `unmeasured`.

**Checks.** none
