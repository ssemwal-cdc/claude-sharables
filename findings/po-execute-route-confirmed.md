---
id: F163
slug: po-execute-route-confirmed
kind: finding
status: observed
date: 2026-09-24
---
# Purchase order route reported working

**Outcome protected.** A reviewed purchase order can be actioned, and only as the reviewer instructed.

**Argument.** The route shipped as NS v23 on the bill-route rule, D76, purchase orders take
bill route.
Five purchase orders once refused at the click, F94, NetSuite could not click POs, before
that rule shipped.
Four fields confirmed live on 2026-09-01: `approvalstatus`, `custbody_sna_cdc_next_approver`,
`custbody_sna_cdc_previous_approver` and `custbody_sna_cdc_app_count`.
Those are exactly what the pre-click gate and the post-click verification read.
The buttons, the note and the plain-Approve no-op were never confirmed live before this report.
The route is retired with execute mode since D91, review-only plugins. It returns with
execute mode.

**Evidence.** Reported 2026-09-24 by the maintainer: the route worked.
The maintainer is not certain, so do not call this measured.
Which purchase order, which button set and which run are not recorded.
`check_execute_type_coverage()` in `scripts/shared_blocks.py` guards only that a route exists
for every type.
It says nothing about whether a route is correct.

**Checks.** `check_execute_type_coverage()` in `scripts/shared_blocks.py`.
