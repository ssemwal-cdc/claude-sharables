---
id: F138
slug: password-box-correctly-triggers-wall
kind: finding
status: observed
date: 2026-09-10
---
# A password box correctly triggers wall

**Outcome protected.** The login table decides on the password box, not on whether an
email field sits beside it.

**Argument.** One part of the refused run was right, and the fix keeps it right.
It described the screen as an email and password form.
If a password box really was on it, `wall` was the correct call.
Only the wording and the recovery were wrong, not the read of the screen.

**Evidence.** Reported 2026-09-10, the same run as
`F135`, a prose rewrite caused the refusal.

**Checks.** `test_login_states()` in `scripts/test_skill_code.py`.
