---
id: pending
slug: permission-mode-unreadable-by-agent
kind: finding
status: settled
date: 2026-08-15
---
# An agent cannot read its own permission mode

**Outcome protected.** A permission question converges in one round instead of four.

**Argument.** A `javascript_tool` call was reported blocked.
Four rounds of probes followed, with two wrong versions of a maintainer note
and an onboarding section written then deleted unshipped.
The actual answer: the run had been in skip-all rather than auto.
Nothing was ever wrong.

The mode was reported from memory, and no tool can check it.
No tool returns an agent's own permission mode, so the single fact the whole
investigation turned on was unverifiable by the agent.
Only the person at the keyboard could record it, in the moment, and it was
misremembered.
Capture the mode at the moment of the run.
Everything converged within one run of pinning it down, and nothing converged
before.

**Evidence.** Dated 2026-08-15.
Four rounds of probes, two wrong note versions, one deleted onboarding
section.
The permission mode of any past run is unrecordable after the fact.
`unmeasured`.

**Checks.** none.
