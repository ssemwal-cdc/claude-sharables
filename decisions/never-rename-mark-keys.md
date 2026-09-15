---
id: D38
slug: never-rename-mark-keys
kind: decision
status: settled
date: 2026-08-20
---
# Never rename a marks key

**Rule.** Never rename a per-item marks key. Give a new control a new key.

**Outcome protected.** A decision the user marked survives a re-render.

**Argument.**

Per-item marks live in browser local storage, alongside the view state. They are the only user state that survives a re-render.

Renaming a marks key for tidiness silently discards decisions the user marked but has not executed.

The two kinds of state are not equivalent. Losing a view costs a scroll. Losing a mark discards work.

So a new control gets a new key rather than widening a marks key.

The rule is about whatever the current keys are, not about a particular name.

**Evidence.**

- Recorded 2026-08-20. The current keys are one marks key and one view key per plugin.
- The view keys have been bumped on purpose. See D39, a new default needs a new key.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
