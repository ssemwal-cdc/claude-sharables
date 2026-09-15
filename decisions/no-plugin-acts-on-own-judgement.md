---
id: D6
slug: no-plugin-acts-on-own-judgement
kind: decision
status: settled
date: 2026-08-11
---
# Never act without an instruction

**Rule.** Approve or respond only on an explicit per-item instruction from the user.

**Outcome protected.** No approval carries a decision the user did not make.

**Argument.**

Neither plugin acts on its own judgement.

Both only approve or respond on an explicit per-item instruction.

Preserve that in anything ported in.

The instruction arrives through the composed execute message. See D48, the message authorises only.

**Evidence.**

- Both shipped plugins follow this rule.

**Checks.** `check_execute_prompt_purity()` in `scripts/shared_blocks.py` keeps the authority in the message.
