---
id: F159
slug: execute-button-blocked-state-confirmed
kind: finding
status: observed
date: 2026-09-24
---
# Execute button blocked state confirmed

**Outcome protected.** A blocked execute button reads as blocked, not as broken.

**Argument.** The dashboard template carried three button states.
Grey for idle. An amber outline with a full-contrast label for blocked. The solid dark
primary when it can run.
F57, one disabled style two meanings, already confirmed the idle and the ready states.
This finding confirms the amber blocked state was seen too.
It was already moot since D91, review-only plugins, on 2026-09-18, because execute mode was
removed before this was seen. The state lives on only in `actionable-retired/`.

**Evidence.** Reported 2026-09-24 by the maintainer: the amber blocked state was seen.
Which record or item triggered it is not recorded. That detail is `unmeasured`.
`test_dashboard_view` in `scripts/test_skill_code.py` covers the logic against mocks.

**Checks.** none.
