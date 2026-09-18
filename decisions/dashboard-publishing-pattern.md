---
id: D80
slug: dashboard-publishing-pattern
kind: decision
status: settled
date: 2026-09-15
---
# Publish through the widget

**Rule.** Ship a dashboard template and a publish script as assets. Copy them into the workspace, and render the output through the widget.

**Outcome protected.** A reviewer gets a one-click dashboard from either plugin, built the same way.

**Argument.**

Both plugins carry a template and a publish script under the skill assets folder.

The first run copies them into a workspace state folder.

The output renders through the widget host and never to chat. See D16, render dashboards with show_widget.

Match this shape when porting. If a new skill deviates, say so rather than normalising it quietly.

**Evidence.**

- The house-convention wording said the output is published to an artifact. That contradicted the widget decision, which is settled and later.
- Corrected 2026-09-15 in the prose pass. Both plugins have rendered through the widget since 2026-08-12.

**Checks.** `scripts/validate.py` asserts both assets exist and are referenced through the plugin root variable.
