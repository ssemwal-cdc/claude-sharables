---
id: F109
slug: mechanism-replaces-second-screen-phrase
kind: finding
status: observed
date: 2026-08-24
---
# A hardware phrase became a mechanism claim

**Outcome protected.** A prerequisite reads as a thing you must have, not as a
description of the wait.

**Argument.** The onboarding sheet's phrase about a second screen was cut, while its
meaning was kept.
In a sheet whose second section is a prerequisites list, it read as a hardware
requirement.

What replaced it names the mechanism instead.
Most of the elapsed time is a download, an install and a restart. The rest
is a run that pauses and waits for you.
That is a claim about the work, and it is checkable.

It sits above the prerequisites list, not in it.
That list is things you must have, and this is not one of them.
It is deliberately not inside a collapsed block.
A reassurance nobody opens is not a reassurance.

The first wording over-corrected and was caught the same day.
Saying that none of this needs your full attention invites starting it and
leaving, and the run cannot survive that.

The landed line leads with the two facts a reader decides from: how long
and where they can stop. The posture follows as explanation.
Stating the consequence beat issuing a rule.
The consequence is what makes someone stay.

**Evidence.** Reworked 2026-08-24 in two passes.

**Checks.** `check_onboarding_page()` in `scripts/shared_blocks.py` checks
structure only, not placement.
