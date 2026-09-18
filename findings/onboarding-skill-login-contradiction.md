---
id: pending
slug: onboarding-skill-login-contradiction
kind: finding
status: settled
date: 2026-09-10
---
# Two files disagreed on login behaviour

**Outcome protected.** Two files describing one behaviour to two audiences never
contradict each other.

**Argument.** `docs/onboarding.html` promised that the plugin never logs in for you.
`SKILL.md` permitted typing an email and pressing Continue.
Both were shipped, and a run resolving the contradiction picked the louder one.

The sheet now says what is true.
It never types your password.
It fills an email-only SSO screen, and it stops at a password box.
It also stops at MFA or a CAPTCHA.

**Evidence.** Reported 2026-09-10, the same incident as
`F‹login-rewrite-caused-refusal›`, a prose rewrite caused the refusal.

**Checks.** `test_login_states()` in `scripts/test_skill_code.py`.
