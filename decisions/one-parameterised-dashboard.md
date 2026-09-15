---
id: pending
slug: one-parameterised-dashboard
kind: decision
status: open
date: 2026-08-24
---
# One parameterised dashboard

**Rule.** Keep two dashboard templates until a third lens needs a dashboard.

**Outcome protected.** A defect in one dashboard cannot reach the other one silently.

**Argument.** Merging the two templates is the largest change on the deferred list.
It has the least user-visible benefit.
It removes the independent verification that two copies give.
The drift check already solves the problem that made merging tempting.
See D‹shared-blocks›, canonical copy plus a check.

**Options.**

A. Keep two templates. Rely on the drift check.

B. Merge into one parameterised template now.

**Recommendation.** A. Revisit only when a third lens needs its own dashboard.

**Evidence.** Written 2026-08-24 at the end of the modularity work.
This record is not a commitment.
The two templates were 54.5% line-identical as of 2026-08-24.
The two publish scripts were 54.9% line-identical on the same date.

**Checks.** `python3 scripts/shared_blocks.py --check`, run by `scripts/validate.py`.
