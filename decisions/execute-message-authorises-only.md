---
id: D48
slug: execute-message-authorises-only
kind: decision
status: settled
date: 2026-08-24
---
# The message authorises only

**Rule.** Let the execute message carry the authority, the item list, each verdict and any user comment. Keep the procedure in `SKILL.md`.

**Outcome protected.** The gates that govern a click live in the text a test reads.

**Argument.**

The string the execute button posts into chat carries the authority and nothing else.

It names no endpoint, no query parameter, no verification method and no button rule.

This was settled on two facts about how execute is used. It is always pressed in the same session that ran the review, so the skill is loaded and in context.

And the run is not watched. That is precisely why the gates belong in the governed text rather than in a JavaScript string no test reads.

Both prompts had independently drifted into carrying procedure and both had got it wrong. One contradicted the execute step, and the other omitted one of its gates.

The check also asserts the message still points at the execute step. An authorisation with no specification attached is the other way to break this.

**Evidence.**

- Settled with the maintainer 2026-08-24.

**Checks.** `check_execute_prompt_purity()` in `scripts/shared_blocks.py`.
