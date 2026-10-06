---
id: D97
slug: login-email-stored
kind: decision
status: settled
date: 2026-10-06
---
# The sign-in email comes from config

**Rule.** On Procore's email-only screen, a run types `config.loginEmail`. When it is absent, the run asks the user once and stores the answer. A run never takes the address from the session context.

**Outcome protected.** Once the address is stored, an idle Procore session resumes without a hand-off.

**Argument.**

The email-only step was allowed, but it named no value. A run had to choose between the session email and its own rule against sending that email to other services. It handed off. An address the user typed for this purpose is their own request, so no rule conflicts with it.

**Evidence.**

- Reported 2026-10-06: a run reached the email-only screen, typed nothing, and asked the user to sign in.
- That a stored address clears the screen with no hand-off is `unmeasured`. The next run that meets the screen measures it.

**Checks.** `test_login_states()` in `scripts/test_skill_code.py` pins `config.loginEmail` in Step 0.
