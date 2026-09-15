---
id: pending
slug: registry-added-additively
kind: decision
status: settled
date: 2026-08-26
---
# Leave the check prose alone

**Rule.** Do not rewrite the existing check prose into the registry shape.

**Outcome protected.** The calibration decisions in the review steps stay settled.

**Argument.**

The registry was added purely additively, and that was the whole design.

Not one line of existing check prose was moved, reworded or removed. The diff on both skills shows additions only, apart from the version lines.

That is a stronger behaviour-neutrality guarantee than restructuring and then verifying. It is why the phase shipped without a live run.

The obvious next move is to rewrite the checks underneath into the registry shape. Do not.

The check prose that stays put is what makes the registry free. A rewrite puts the review step calibration decisions back in play.

**Evidence.**

- Recorded 2026-08-26 alongside D‹check-registry-with-manifest›, declare every check in a registry.
- The behaviour neutrality rests on the diff, not on a run. It is `unmeasured` against live data.

**Checks.** none
