---
id: pending
slug: run-self-banned-login
kind: finding
status: settled
date: 2026-09-10
---
# A run banned itself again

**Outcome protected.** An expired session gets a hand-off the user can act on, in the same run.

**Argument.** A Procore run reached the sign-in screen and reviewed nothing.
It cited a hard constraint and said the next scheduled window would retry.
Nothing about the plugin's login behaviour had changed.
The prose had changed.

The earlier rung was a plain instruction.
It said Procore login is email plus Continue, then SSO with no password.
It said to find the email field, set it, and click Continue.
It said anything beyond that is a hand-off to the user, not a retry.

The rewrite led with a bolded absolute not to touch the login form at all.
It appealed to the sheet's promise that the plugin never logs in for you, stated at full generality.
It then demoted the permitted step to a clause beginning "The only case this covers".
Same permission, opposite reading.
A run that reads top-down meets the prohibition first and the carve-out second.
The carve-out then reads as a grudging exception rather than as the instruction it is.
The hard constraint the run cited appears nowhere in the file.
It is the shape of that sentence, quoted back as though it were a rule.

**This is the Step 0 shape for the fourth time.** It is the third where the refusal came from this
repo's own words.
The workspace-write announcement was built from Step 0's own cause list.
The render refusals were built from the do-not-trust-this-tool note.
The invented 90 KB ceiling shipped in a `publish_dashboard.py` comment.
The rung is three named outcomes now: `authenticated`, `email-only` and `wall`.
They are decided on what is on screen.
The email step is stated as permitted, not as an exception.

**The second half is worth more, because it is not about wording.**
"A hand-off to the user, never a retry" named a category and never said what the action is.
That is a prohibition with no stated alternative.
So the run improvised, and picked the one recovery that cannot work.
An expired session does not heal on its own.
Every window until someone signs in fails identically.
A report promising a retry tells the user their queue is being handled when it is not.
That is worse than silence.
Step 0 now specifies the hand-off as an action.
Say it, name the field that made it a `wall`, ask them to sign in, then carry on in the same run.
It answers the unwatched case explicitly.
It forbids the retry sentence by name, with its reason attached.

**One thing the run may have got right, and the fix keeps it right.**
It described the screen as an email and password form.
If a password box really was on it, `wall` was the correct call.
Only the wording and the recovery were wrong.
So the table decides on the password box, not on whether an email field sits beside it.

**The two surfaces also disagreed, which gave the misreading something to cite.**
`docs/onboarding.html` promised that it never logs in for you.
`SKILL.md` permitted typing an email and pressing Continue.
Both were shipped, and a run resolving the contradiction picks the louder one.
The sheet now says what is true.
It never types your password, it fills an email-only SSO screen, and it stops at a password box.
It also stops at MFA or a CAPTCHA.
Where two files describe one behaviour to two audiences, a contradiction is a defect in both.

**Evidence.** Reported 2026-09-10, one run.
The prose changed in `6df1570`, the commit that rewrote the login rung as an absolute.
`test_login_states()` pins every clause and is mutation-tested three ways.
G‹write-never-attempted›, three runs blaming the platform, is the same shape.

**Checks.** `test_login_states()` in `scripts/test_skill_code.py`.
