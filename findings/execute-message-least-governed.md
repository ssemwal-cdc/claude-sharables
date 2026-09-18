---
id: pending
slug: execute-message-least-governed
kind: finding
status: settled
date: 2026-08-24
---
# Execute message was least governed

**Outcome protected.** The text closest to a real approve click is governed text.

**Argument.** A nine-agent prose audit found a place nobody had looked, the composed execute
message.
It is the text closest to a real approve click.
It was the least-governed text in either plugin, a JavaScript string inside an HTML
template. No shared block covered it, and no test read it.

Both copies had independently drifted into carrying procedure, and both got it wrong in
the same week.
NetSuite's told the run to click the named button only.
That is the button rule Approve With Notes exists to override.
It then told the run to re-query the pending queue, the retired verification.
That verification invites a re-run that would approve twice.

Procore's carried its whole five-step ladder and omitted `per_page=100`.
Procore's own Step 2 records that omission converting a live workflow into an empty
response.
Step 8 then reads that response as already actioned, and skips the item.

**Evidence.** Audit dated 2026-08-24.
`grep per_page plugins/` returned three hits, all in `SKILL.md`, none in the template.

**Checks.** `check_execute_prompt_purity()` in `scripts/shared_blocks.py`.
