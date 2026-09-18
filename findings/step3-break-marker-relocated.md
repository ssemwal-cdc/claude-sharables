---
id: pending
slug: step3-break-marker-relocated
kind: finding
status: observed
date: 2026-08-24
---
# The onboarding break moved to step 3's end

**Outcome protected.** A reader can find the point where they may stop. That happens before they
have already started the step it lets them defer.

**Argument.** The posture paragraph had to be cut in half, because it outgrew the list
it introduces.
Two of its four sentences were third copies of facts a chip and a marker
already carried.

The break is marked at the end of step 3 now, and where it sits is the whole
point.
It existed before as a clause inside step four.
So the only reader who could find it had already started the step it lets
them defer.

It reuses the existing note class rather than adding one.
The sheet had just been through a brevity pass. A bespoke class for one
element is the accretion that pass was removing.
The placement guard is anchored to the element after the section anchor, not
to a phrase.
The phrase is the part that keeps getting rewritten.

The chip class stays, because the step 1 and step 2 headings use it.
A future check should assert the header row is empty, not that the class is
unused.

Step 4 keeps a warning of its own and no longer repeats either point.
The timeout is the one fact true of that step and not of the others.

**Evidence.** Reworked 2026-08-24 in two passes.
The figure landed at about 45 minutes with a stop after step 3.

**Checks.** `check_onboarding_page()` in `scripts/shared_blocks.py` checks
structure only, not placement.
