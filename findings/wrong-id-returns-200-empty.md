---
id: F36
slug: wrong-id-returns-200-empty
kind: finding
status: observed
date: 2026-08-15
---
# A wrong id returns empty

**Outcome protected.** A live item is never logged as actioned by someone else.

**Argument.**

Two different failures exist here and only one is loud.

A wrong workflowable type returns a 400, which is unmissable.

The right type with the wrong id returns 200 with zero rows. That is indistinguishable from no workflow instance existing.

The execute step reads no instance as already actioned elsewhere. So the package id produces a clean success that logs a live item as done.

That is what made change orders look ungated to begin with.

An earlier note said the wrong id returns a 400. That note was wrong.

**Evidence.**

- Corrected from a live run 2026-08-15.
- The guard is D30, demote a missing wfId.

**Checks.** `scripts/test_skill_code.py` pins the ungated demotion.
