---
id: D80
slug: dashboard-publishing-pattern
kind: decision
status: settled
date: 2026-09-15
---
# Publish through the widget

**Rule.** Ship a dashboard shell, its `dashboard.css` and `dashboard.js`, and a publish script as assets. Copy all of them into the workspace, and render the output through the widget.

**Outcome protected.** A reviewer gets a one-click dashboard from either plugin, built the same way.

**Argument.**

Both plugins carry a shell, its stylesheet and script, and a publish script under the skill assets folder.

Step 0 copies all of them into a workspace state folder.

The output renders through the widget host and never to chat. See D16, render dashboards with show_widget.

Match this shape when porting. If a new skill deviates, say so rather than normalising it quietly.

**Evidence.**

- The house-convention wording said the output is published to an artifact. That contradicted the widget decision, which is settled and later.
- Corrected 2026-09-15 in the prose pass. Both plugins have rendered through the widget since 2026-08-12.
- The shell split into `dashboard.css` and `dashboard.js` is on branch `claude/cdn-split`, 2026-11-11. Not on main.

**Checks.** `scripts/validate.py` fails a `SKILL.md` that names a missing `${CLAUDE_PLUGIN_ROOT}` path, and fails a bare relative asset path. An asset that no `SKILL.md` names is a note, not a failure.

Kind: process
Home: scripts/validate.py
