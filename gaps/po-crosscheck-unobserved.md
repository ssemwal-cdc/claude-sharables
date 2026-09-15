---
id: pending
slug: po-crosscheck-unobserved
kind: gap
status: unobserved
date: 2026-08-20
---
# PO cross-check fixed, unobserved

**Outcome protected.** A correctly coded bill is never flagged as coded to the wrong purchase order.

**Argument.** This is the one gap that moved by being falsified, not confirmed.
Step 5 identified a bill's purchase order from `custbody3`, a typed reference.
It produced confident false "coded to the wrong PO" flags on correctly coded bills.
A teammate found it by noticing Related Records disagreed with System Information.

What is fixed: PO identity comes from `previoustransactionlinelink` with `linktype = 'OrdBill'`.
Three states stay distinct.
Billed-to-date is derived through the link and split from pending.
A zero is no longer readable as a finding.
A typed mismatch is demoted to a data-entry note.

What is still unobserved: the corrected Step 5 has never run inside an actual review.
The queries are live-verified, because every query in the fix was executed against production.
The skill following those queries end to end has not been watched.
Step 5 runs only in connector mode, so it inherits G‹no-end-to-end-run›, no watched run.

To clear it: run one connector-mode review over a queue with at least one disagreeing bill.
Required outcome: the item is not flagged for PO coding.
Required outcome: a `poWarning` names the disagreement.

**Evidence.** Corrected from guessed to proven, 2026-08-20.
Confirmed against production on five of five bills.
Bills `2325026-07` and `182743734-0004` are the known cases to re-use.
Guarded by `scripts/test_skill_code.py`, mutation-tested 10 of 10 caught.
Step 5 arrived in the root commit and its logic was never revised.
`git log -S` on `poContext`, `poWarning` and `custbody3` each return only that commit.
No commit message ever explained the design.
Step 5's own text claimed its three checks "have found real issues".
That claim named no run, record or date, and is now marked as designed in `SKILL.md`.
`python3 scripts/test_skill_code.py` covers the logic against mocks only.
It cannot cover this gap, because this gap is about a real system.

**Checks.** `scripts/test_skill_code.py`.
