---
id: pending
slug: no-self-update-instruction
kind: decision
status: settled
date: 2026-08-11
---
# No self-update text in SKILL.md

**Rule.** Never put `/plugin marketplace update` in a `SKILL.md`. Point the reader at auto sync.

**Outcome protected.** A teammate follows an instruction that can actually run.

**Argument.**

`SKILL.md` is a prompt, not a script.

`/plugin` is a client command that Claude cannot invoke.

The file carrying the instruction is itself the stale copy, so the instruction can never be current.

Auto sync keeps an installed plugin current already. See F‹two-command-update›, update needs the marketplace qualifier, for the terminal route.

**Evidence.**

- Recorded 2026-08-11. No run has been observed following such an instruction, so the failure is `unmeasured`.

**Checks.** none
