---
id: pending
slug: netsuite-po-execute-gap
kind: finding
status: observed
date: 2026-09-01
---
# NetSuite could not click POs

**Outcome protected.** Every reviewed type can be actioned.

**Argument.**

Five purchase orders were reviewed, all came back clear, and all were refused at the click.

The execute step record-type rule named bills and change orders only.

The run behaved correctly. It re-verified all five, clicked nothing and reported the gap.

It was still a defect, because the review step has read purchase orders since the day the skill shipped.

This is the Procore fourth-type problem one skill along, with the split inside a skill rather than at its edge. The review half knew a type the execute half did not, and nothing compared the two lists.

**Evidence.**

- Reported 2026-09-01. Two batches stopped at the same gate before it was called a defect.
- The route is D‹po-takes-bill-route›, purchase orders take the bill route.
- The gate is D‹execute-type-coverage-gate›, gate the two type lists.
- The route has never fired. See G‹po-execute-route-unfired›, the purchase order route is unfired.

**Checks.** `check_execute_type_coverage()` in `scripts/shared_blocks.py`.
