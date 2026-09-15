---
id: pending
slug: verdict-vocabulary-gate
kind: decision
status: settled
date: 2026-08-24
---
# Gate template verdicts against publish

**Rule.** Add a new verdict to the allowlist, the review step vocabulary and the template together.

**Outcome protected.** Every branch on a dashboard can actually render.

**Argument.**

`check_verdict_vocabulary()` asserts that every verdict a template branches on is one its own publish script can emit.

It exists because Procore carried an actioned bin filtered on a verdict that the allowlist rejected. The branch was unreachable and had never rendered in any run.

Meanwhile the carry-forward rule in the skill retained items to feed that bin.

Nothing else checks that a page branch is reachable.

A capability table is a second surface with the same risk. See F‹capability-verdicts-gate›, capability rows name emittable verdicts.

**Evidence.**

- Added 2026-08-24. The unreachable bin is F‹actioned-bin-never-rendered›, the actioned bin never rendered.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py`.
