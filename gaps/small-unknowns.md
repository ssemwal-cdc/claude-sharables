---
id: G5
slug: small-unknowns
kind: gap
status: unobserved
date: 2026-08-15
---
# Four small unknowns

**Outcome protected.** A small unknown stays named instead of becoming an assumption.

**Argument.** Four unknowns are small enough to share one record.

- **The desktop app's version display.** Nobody knows whether the app's plugin list shows a
  commit-hash version.
  The onboarding sheet says both plugins appear in the installed list, which is definitely visible.
  The hash check is documented for the CLI only.
- **The Cowork connector toggle.** Nobody knows whether Cowork sessions need the
  per-conversation connector toggle under plus, then Connectors.
  Anthropic's documentation says connectors are per-conversation.
  The step was removed from the sheet as not matching observed behaviour.
- **Rung 2 of the Step 0 sync ladder.** Nobody knows whether the file tools can read
  `${CLAUDE_PLUGIN_ROOT}` from a Cowork sandbox.
  Observed so far: the shell cannot see it there.
  Read is expected to work, because assets resolve at run time and the skill panel lists them.
  Nobody has walked that rung.
  If read fails too, rung 3 keeps runs alive.
  Cowork workspaces would then refresh only from a surface whose shell mounts the plugin directory.
- **Approve With Notes and the handler shape.** Nobody knows whether it shares plain Approve's
  shape of an async script load, then `win.open`.
  If it does, its failure presents as the documented "notes page never arrives" case.
  The same page-read gate catches that case.
  Nobody has read that button's handler.
  There is no note-carrying equivalent of the URL recovery.

**Evidence.** Every claim here is guessed, not proven.
Each is tested against mocks or fixtures, or against documentation, and shipped.
Nobody has watched any of them on real data.
Do not cite any of them as established.
`python3 scripts/test_skill_code.py` covers the logic against mocks.
It cannot cover these gaps, because they are about real systems.
The shell's inability to see `${CLAUDE_PLUGIN_ROOT}` was observed 2026-08-15 in a Cowork run.
F‹netsuite-approval-note-confirmed›, the notes page now seen once, carries the fourth unknown's consequence.
One clean read does not confirm the button's handler for every case.

**Checks.** none.
