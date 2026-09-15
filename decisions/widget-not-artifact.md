---
id: pending
slug: widget-not-artifact
kind: decision
status: settled
date: 2026-08-12
---
# Render dashboards with show_widget

**Rule.** Render both dashboards with `show_widget`. Never render them as an artifact.

**Outcome protected.** One click on a dashboard button puts the execute instruction into chat.

**Argument.**

The widget host and the artifact host expose disjoint bridges. See F‹disjoint-host-bridges›, no bridge overlap.

An artifact cannot send a message to chat. A button that hands an instruction back to the conversation is inert there and fails closed, with no throw and no console output.

`askClaude` is not a substitute. It runs a small model in the page and returns to the page, so it cannot start a turn with real tool access.

The cost is that `callMcpTool` is unavailable, so the page cannot re-query its own data. The NetSuite dashboard used to do that on open.

That check now lives in the execute turn, which is strictly better. An on-open query is already stale when execute is pressed. A check in the moment before the click has no window at all.

Do not restore the artifact path for persistence. A shareable URL was considered and rejected, because NetSuite and Procore are the systems of record.

**Evidence.**

- Probed live from inside each surface 2026-08-11. `sendPrompt` and `openLink` are bare globals on the widget host and absent on the artifact host.
- `callMcpTool`, `askClaude` and `runScheduledTask` sit on `window.cowork` on the artifact host and are absent on the widget host.
- Confirmed end to end on NetSuite 2026-08-12. See F‹widget-sendprompt-works›, sendPrompt posts to chat.

**Checks.** none
