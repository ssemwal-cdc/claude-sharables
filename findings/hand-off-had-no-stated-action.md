---
id: pending
slug: hand-off-had-no-stated-action
kind: finding
status: settled
date: 2026-09-10
---
# A hand-off rule named no action

**Outcome protected.** A rule that forbids a retry also states the one action that
replaces it.

**Argument.** "A hand-off to the user, never a retry" named a category and never said
what the action is.
That is a prohibition with no stated alternative.
So the run improvised, and picked the one recovery that cannot work.

An expired session does not heal on its own.
Every window until someone signs in fails identically.
A report promising a retry tells the user their queue is being handled when it
is not.
That is worse than silence.

Step 0 now specifies the hand-off as an action.
Say it, and name the field that made it a `wall`. Ask them to sign in,
then carry on in the same run.
It answers the unwatched case explicitly, and forbids the retry sentence by
name, with its reason attached.

**Evidence.** Reported 2026-09-10, one run, the same incident as
`F‹login-rewrite-caused-refusal›`, a prose rewrite caused the refusal.

**Checks.** `test_login_states()` in `scripts/test_skill_code.py`.
