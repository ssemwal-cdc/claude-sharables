---
id: pending
slug: widget-sendprompt-works
kind: finding
status: observed
date: 2026-08-12
---
# sendPrompt posts to chat

**Outcome protected.** A reviewer executes a batch with one click and no clipboard.

**Argument.**

The widget port is confirmed working end to end.

The dashboard renders inline in the conversation. Pressing execute puts the instruction straight into chat as a new message.

So the widget host function takes a bare string and really does post.

The clipboard handoff in the template is now the artifact-host fallback alone. It should never be reached in normal use.

**Evidence.**

- Confirmed on NetSuite 2026-08-12.

**Checks.** none
