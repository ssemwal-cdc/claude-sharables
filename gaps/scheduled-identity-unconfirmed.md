---
id: G11
slug: scheduled-identity-unconfirmed
kind: gap
status: unobserved
date: 2026-08-26
---
# Scheduled run identity unconfirmed

**Moot** since F165, the built-in-browser regression, on
2026-09-24. The maintainer turned scheduling off. When scheduling returns, this reopens.

**Outcome protected.** A review shows the queue of the person who owns it.

**Argument.** Step 0 must report the name it finds and ask the user to confirm it.
Step 0 must never pick an identity silently.
A scheduled run has nobody to ask.
Most of Step 0 is self-serviceable.
The account id is in the URL.
The connector tool name is readable from the session.
The employee id is a query on the user's own email.
One unambiguous active employee row makes proceeding reasonable.
Zero rows or several rows is the branch the rule stops.
An unattended run that picked anyway chose an identity in silence.
`config.me` then scopes the whole review to that identity.
Nobody has looked at which branch fired.
Do not assume the branch is safe.
Do not assume the branch is broken.

**Evidence.** Everything in this record is guessed, not observed.
It is tested against mocks or fixtures and shipped.
Nobody has watched it work on real data.
`python3 scripts/test_skill_code.py` covers the logic against mocks only.
It cannot cover this gap, because this gap is about a real system.
2026-08-26: the maintainer reported a scheduled folderless run completing its own onboarding.
The run is the reason this question exists.
Which Step 0 branch it took is `unmeasured`.
Settle it by reading `config.meName` in a log a scheduled run wrote.
Confirm that name is the right person.
Watching one scheduled run also settles it.

**Checks.** none.
