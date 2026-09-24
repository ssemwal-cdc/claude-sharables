---
id: pending
slug: end-to-end-runs-routine
kind: finding
status: observed
date: 2026-09-24
---
# End-to-end runs confirmed routine

**Outcome protected.** A reviewer's verdicts come from a path somebody has watched work.

**Argument.** Full reviews now run end to end on both plugins, many times over.
Earlier partial runs already confirmed two pieces of this path.
A live Procore gate ran through the `CommitmentChangeOrder` join and gated two Align change orders.
A live NetSuite approval completed on record 2534442 by the Step 8.6 URL recovery.
F144, the once-unseen NetSuite notes page, is now read on the record.
The ordinary Approve With Notes route and the Procore execute walk are moot since D91, review-only plugins.

**Evidence.** Reported 2026-09-24 by the maintainer: end-to-end runs have happened thousands of times.
Which routes and item types those runs covered is not itemized.
The run count is `unmeasured`.
Partial observations dated 2026-08-15 stand: the Procore CCO gate and the NetSuite URL-recovery approval.
`python3 scripts/test_skill_code.py` covers the logic against mocks only.

**Checks.** `scripts/test_skill_code.py`, mocks only.
