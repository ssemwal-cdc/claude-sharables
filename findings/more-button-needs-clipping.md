---
id: F59
slug: more-button-needs-clipping
kind: finding
status: observed
date: 2026-08-24
---
# A clamp needs real clipping

**Outcome protected.** A control that is offered does something visible.

**Argument.**

Template v9 emitted the more button whenever the warning text was non-empty.

So a one-line warning offered a control that did nothing visible.

A trim pass now compares the scroll height against the client height after each render. It hides the button when nothing is cut.

**Evidence.**

- Verified with a deliberately short warning in the fixture. Two unclipped warnings hide the button and one clipped warning keeps it.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
