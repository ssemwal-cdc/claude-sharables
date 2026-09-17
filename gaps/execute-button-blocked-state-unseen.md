---
id: pending
slug: execute-button-blocked-state-unseen
kind: gap
status: unobserved
date: 2026-09-16
---
# Execute button blocked state unseen

**Outcome protected.** A blocked execute button reads as blocked, not as broken.

**Argument.** The dashboard template carries three button states.
Grey for idle. An amber outline with a full-contrast label for blocked. The solid dark primary when it can run.
F57, one disabled style two meanings, confirms the idle and the ready states directly.
The amber blocked state exists in the template but has never been seen rendered.

To clear it: mark an item blocked in the dashboard template and look at it.

**Evidence.** This claim is guessed, not proven.
Nobody has watched the amber blocked state render.
Do not cite it as established.
`test_dashboard_view` in `scripts/test_skill_code.py` covers the logic against mocks.
It cannot cover this gap, because this gap is about a real render.

**Checks.** none.
