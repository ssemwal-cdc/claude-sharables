---
id: pending
slug: tied-verdict-for-verified-blanks
kind: decision
status: settled
date: 2026-09-23
---
# Add a fifth verdict for a verified blank

**Rule.** A verified figure with one blank field earns its own verdict, `tied`, never folded into `skipped`.

**Outcome protected.** An item whose figures were verified reaches the reviewer. It is never buried beside items where nothing was verified.

**Argument.**

`skipped` folded two different things into one word. Nothing was verified. Or everything checkable agreed and one field is blank in Procore.

The second case is genuinely approvable. It sat inside a fifty-row `skipped` block, beside items with no evidence at all.

D41, three states never a boolean, made the same argument once for a read that failed.

D63, gate verdicts against publish, requires the new verdict in the allowlist, the review step vocabulary and the template together.

D6, never act without an instruction, sets the new verdict's name. It states the evidence, never the action.

**Evidence.**

- Added 2026-09-23. The folded verdict is F115, the actioned bin never rendered, a related case where one verdict hid two meanings.

**Checks.** `check_verdict_vocabulary()` and `check_capability_verdicts()` in `scripts/shared_blocks.py`. `scripts/test_skill_code.py`, the tied-verdict cases.
