---
id: pending
slug: demote-missing-wfid-ungated
kind: decision
status: settled
date: 2026-08-15
---
# Demote a missing workflow id

**Rule.** Demote an item with no workflow instance id to `ungated` and print a warning. Never fall back to another id.

**Outcome protected.** An unresolved gate cannot reach the execute list.

**Argument.**

The dangerous part is the failure mode, not the 400.

The execute instruction treats a lookup that returns no instance as already actioned elsewhere and skips the item.

So a wrong id raises no error. It silently logs a live item as done.

The publish script therefore demotes such an item rather than falling back to the package id.

An ungated item renders a resolve-the-gate control instead of response buttons, so an unresolved id cannot reach the execute list.

Keep that guard if the lookup is ever changed.

The workflow type is per item now, with the instance id beside it. The queue item type and the workflow endpoint type are not the same thing, and the old constant assumed they were.

**Evidence.**

- Recorded 2026-08-15 from F‹wrong-id-returns-200-empty›, a wrong id returns 200 empty.
- Applied to commitments too. See F‹commitment-two-collections›, one kind covers two collections.

**Checks.** `scripts/test_skill_code.py` runs the ungated demotion, mutation-tested.
