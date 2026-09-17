---
id: D50
slug: generated-bespoke-skill
kind: decision
status: abandoned
date: 2026-08-24
---
# Skill that generates skills

**Rule.** Never ship a skill that generates another skill for a user.

**Outcome protected.** Every approval runs on text a maintainer vetted and a push can fix.

**Argument.** The proposal was a skill that interviews the user and then generates a bespoke skill.
The interview half is solvable today.
The connector-probe half is solvable today.

**Reason abandoned.** The generation half is the wrong bet, for structural reasons.
A generated skill starts at zero on everything these notes paid for.
That includes three-state reads, verify the record not the queue, and the output-filter redactions.
It re-earns each lesson in production.
It does so on systems where the failure mode is a silent wrong approval.
It also forks the distribution model.
Push to `main` is the release, and that works because everyone runs the same artifact.
A per-user generated skill has no shared version and receives no fixes.
It is invisible to `validate.py`.
The Step 5 PO fix reached every installed copy in one push.
It would have reached zero generated copies.
It inverts the house safety convention as well.
Neither plugin acts on its own judgement, and that rule is load-bearing.
A skill that designed itself is judgment all the way down.
It leaves no reviewable text a maintainer ever vetted.

**Evidence.** Declined 2026-08-24.
F‹po-crosscheck-run-confirmed›, the Step 5 fix, is the push that reached every installed copy.
D9, version resolves from the commit SHA, is why one push ships.
The count of generated copies a fix would reach is zero, by construction.

**Checks.** none.
