---
id: pending
slug: po-execute-route-unfired
kind: gap
status: unobserved
date: 2026-09-01
---
# Purchase order route unfired

**Outcome protected.** A reviewed purchase order can be actioned, and only as the reviewer instructed.

**Argument.** The route shipped as NS v23 and nothing has been clicked through it.
A maintainer's run put five purchase orders through the review, all `clear`.
Step 8 refused every one, because its record-type rule named bills and change orders only.

**What is observed is precise.** The run re-verified all five records.
Each carries `approvalstatus`, `custbody_sna_cdc_next_approver`, `custbody_sna_cdc_previous_approver`
and `custbody_sna_cdc_app_count`.
Each was still pending and still assigned to the user.
Those four fields are exactly what the pre-click gate and the post-click verification read.
That is the whole basis for putting purchase orders on the bill route, and it is a good one.

**What is not observed, and must not be cited as though it were.**

- **The buttons.** Nobody has read a purchase order's approval buttons.
  Whether it offers Approve With Notes at all is unknown.
  Step 4 has a branch for that button being absent, and that branch is itself unfired.
  Report the button labels verbatim if a run ever hits it.
- **The note.** Every approval this skill has made carried `Approved by Claude` through Approve With Notes.
  A purchase order approved without a note has never happened.
  So the log line naming a record type with no notes button has never been written.
- **The plain-Approve no-op.** The dropped `win.open` failure was pinned on a bill, record 2534442.
  Whether a purchase order's button behaves the same way is untested.
  The recovery is written to apply, and applying is not the same as working.
- **The gate in browser mode.** NS v23 states that with no connector the buttons are the gate for every type.
  That was always implied and never written down.
  It has not been run either.

**What is now impossible rather than merely unlikely: the same gap reopening quietly.**
`check_execute_type_coverage()` compares three lists.
Those are the schema's type vocabulary, the execute step's route table and `ITEM_TYPE_MANIFEST`.
It fails the build on any disagreement.
It says nothing about whether a route is correct.
It says only that a route exists for every type the queue can hold.
Everything unobserved above is the part a build gate cannot reach.

**Evidence.** Evidence class: a maintainer's report of a run, not a transcript.
Reported 2026-09-01: five purchase orders reviewed, five refused at the click.
The run behaved correctly. It re-verified all five, clicked nothing and reported the gap.
Record 2534442 is the bill where the URL recovery was pinned.
`check_execute_type_coverage()` is mutation-tested five ways.
Those mutations are dropping the row, shrinking the schema, inventing a fourth type, renaming the
heading and blanking a gate cell.

**Checks.** `check_execute_type_coverage()` in `scripts/shared_blocks.py`.
