---
id: D29
slug: auto-mode-not-skip-all
kind: decision
status: settled
date: 2026-08-15
---
# Auto mode, never skip-all

**Rule.** Run both plugins in auto permission mode. Never use skip-all, and add no permission configuration.

**Outcome protected.** A browser holding live approval authority keeps its permission prompts.

**Argument.**

The single denial that started the permissions detour was environmental. The run was in skip-all, not auto.

Nothing about the code, the hosts or the configuration was involved.

Re-running the exact snippet in auto passed with no prompt. That is one operation, not all of them, and the earlier claim that every operation had run clean in auto is withdrawn.

So the instruction rests on its other leg. Skip-all is ruled out on the Anthropic documentation grounds, which say to use that mode only in isolated environments where Claude Code cannot cause damage.

A browser signed into Procore and NetSuite with live approval authority is the exact opposite of that.

An auto-mode environment configuration block is not recommended. It is configuration with no demonstrated purpose, and unused configuration rots. The block is in the git history if something is ever genuinely blocked.

An onboarding section was written for a scheduled-run hang that turned out not to exist, and removed unshipped. Do not add one without a reproduction.

**Evidence.**

- Settled 2026-08-15 by re-running byte-identical code in auto mode with no configuration block.
- Coverage of auto mode across every operation is `unmeasured`.
- The onboarding sheet carries the skip-all reason and never the withdrawn claim. See F45, a retraction reached one surface.
- The denial that started it is F22, the classifier can deny everything.
- The mode cannot be read back. See F32, permission mode is unreadable.
- A returned promise can serialise empty. See F34, a returned promise serialises empty.

**Checks.** none
