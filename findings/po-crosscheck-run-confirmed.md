---
id: F146
slug: po-crosscheck-run-confirmed
kind: finding
status: observed
date: 2026-09-16
---
# PO cross-check run confirmed

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

What is now reported: a full connector-mode run happened.
Both the duplicate check and the over-commitment check ran.
Step 5 runs only in connector mode.
The broader end-to-end gap is closed. See F‹end-to-end-runs-routine›, end-to-end runs confirmed.

**Evidence.** Corrected from guessed to proven, 2026-08-20.
Confirmed against production on five of five bills.
Bills `2325026-07` and `182743734-0004` are the known cases to re-use.
Guarded by `scripts/test_skill_code.py`, mutation-tested 10 of 10 caught.
Step 5 arrived in the root commit and its logic was never revised.
`git log -S` on `poContext`, `poWarning` and `custbody3` each return only that commit.
No commit message ever explained the design.
Step 5's own text once claimed its three checks "have found real issues".
That claim named no run, record or date, and is marked as designed in `SKILL.md`.
`python3 scripts/test_skill_code.py` covers the logic against mocks only.
Reported by the maintainer, date unrecorded.
A full connector-mode run happened, and both the duplicate check and the over-commitment check ran.
The run is unmeasured.

**Checks.** `scripts/test_skill_code.py`.
