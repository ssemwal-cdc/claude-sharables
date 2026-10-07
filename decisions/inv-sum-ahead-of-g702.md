---
id: pending
slug: inv-sum-ahead-of-g702
kind: decision
status: settled
date: 2026-10-07
---
# A contract sum ahead of the G702 warns only when explained

**Rule.** Procore `contract_sum_to_date` ahead of the G702 gives a warning. That holds only when payment due ties and the gap equals named approved change orders not yet on the G702. Otherwise FLAG.

**Outcome protected.** A timing gap does not hide an unexplained one.

**Argument.**

Approved change orders reach Procore before the next pay application. The G702 lags for a real reason.

A gap that no named change order explains has no such reason.

**Evidence.**

- Owner ruling, 2026-10-07, from the 2026-10-07 field run.

**Checks.** none yet. The rule lives in the skill prose.
