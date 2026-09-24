---
id: F155
slug: commitment-payload-unread
kind: finding
status: observed
date: 2026-09-24
---
# Commitment payload reported closed

**Outcome protected.** A commitment's figures come from fields the payload really has.

**Argument.** The queue's fourth type, the commitment, shipped as PC v24.
Step 3's field names were borrowed from the `change_order_packages` read.
Against a real purchase order contract, `grand_total`, `line_items` and `retainage_percent` held.
The counterparty's display string is `vendor.company`, not `vendor.name`.
`WorkOrderContract` is a separate collection under the same `com` type string.
No answer ever said a work order contract reached the queue.

**Evidence.** Reported 2026-09-24 by the maintainer: pretty sure this is closed.
The maintainer is not certain, so do not call this measured.
`WorkOrderContract` is still unread. That half stays `unmeasured`.
`test_commitment_kind` in `scripts/test_skill_code.py` pins the demotion and is mutation-tested.

**Checks.** `test_commitment_kind` in `scripts/test_skill_code.py`.
