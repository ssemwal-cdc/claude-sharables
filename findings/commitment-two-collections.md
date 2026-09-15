---
id: F88
slug: commitment-two-collections
kind: finding
status: observed
date: 2026-08-28
---
# One kind covers two collections

**Outcome protected.** A commitment link and its gate query name the right collection.

**Argument.**

Purchase order contracts and work order contracts are separate Procore collections under one Commitments tool.

So the item kind cannot decide anything on its own.

The workflow type of the item, which is the queue item type verbatim, is what picks between them. It picks in the record link and at the workflow endpoint alike.

A commitment with no workflow type is demoted to ungated. That is the change order guard one type along.

Both strings are valid workflowable types. So the wrong one carrying the right id returns 200 with zero rows rather than a 400.

The execute step reads an empty instance as already actioned elsewhere, so a live contract would be logged as done with no click.

This is the seventh instance of the shape these records keep recording.

**Evidence.**

- Reported 2026-08-28.
- The guard is D30, demote a missing workflow id.

**Checks.** `test_commitment_kind` in `scripts/test_skill_code.py`, mutation-tested.
