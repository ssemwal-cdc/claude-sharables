---
id: pending
slug: disjoint-host-bridges
kind: finding
status: observed
date: 2026-08-11
---
# Host bridges do not overlap

**Outcome protected.** A dashboard button starts a real turn instead of failing closed.

**Argument.**

The widget host and the artifact host expose disjoint bridges, with two different namespacing conventions.

On the widget host the origin is a framed content domain. `sendPrompt` and `openLink` are bare globals and are functions.

On the artifact host the origin is a local artifact scheme. `sendPrompt` and `openLink` are absent everywhere.

`callMcpTool`, `askClaude` and `runScheduledTask` sit on a `window.cowork` object on the artifact host and are absent on the widget host.

Zero overlap. So an artifact cannot send a message to chat, and a button that tries fails silently.

**Evidence.**

- Probed live from inside each surface 2026-08-11.
- The consequence is D‹widget-not-artifact›, render dashboards with show_widget.

**Checks.** none
