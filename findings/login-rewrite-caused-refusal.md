---
id: pending
slug: login-rewrite-caused-refusal
kind: finding
status: settled
date: 2026-09-10
---
# A prose rewrite caused a login refusal

**Outcome protected.** An expired session gets a hand-off the user can act on, in the same
run.

**Argument.** A Procore run reached the sign-in screen and reviewed nothing.
It cited a hard constraint and said the next scheduled window would retry.
Nothing about the plugin's login behaviour had changed. The prose had changed.

The earlier rung was a plain instruction.
It said Procore login is email plus Continue, then SSO with no password.
It said to find the email field, set it, and click Continue.
It said anything beyond that is a hand-off to the user, not a retry.

The rewrite led with a bolded absolute not to touch the login form at all.
It appealed to the sheet's promise that the plugin never logs in for you, stated
at full generality.
It then demoted the permitted step to a clause beginning "The only case this
covers".
Same permission, opposite reading.
A run that reads top-down meets the prohibition first and the carve-out second.

The hard constraint the run cited appears nowhere in the file.
It is the shape of that sentence, quoted back as though it were a rule.

**Evidence.** Reported 2026-09-10, one run.
The prose changed in `6df1570`, the commit that rewrote the login rung as an
absolute.
See G13, three runs blaming the platform, the same shape.

**Checks.** `test_login_states()` in `scripts/test_skill_code.py`.
