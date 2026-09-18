---
id: F45
slug: retraction-not-applied-to-sheet
kind: finding
status: observed
date: 2026-08-20
---
# A retraction reached one surface

**Outcome protected.** No session cites a claim this repo already withdrew.

**Argument.**

The onboarding sheet tells the reader to set permissions to auto and not to use skip-all. That is the one permissions instruction it carries.

It is a setup instruction, not troubleshooting. The onboarding section warned against elsewhere was troubleshooting for a hang that never existed.

It rests on one settled fact. Skip-all is ruled out on the Anthropic documentation grounds for a browser holding live approval authority.

The maintainer notes used to cite a second fact, that every operation either plugin performs had run clean in auto. The auto-mode record retracts precisely that.

The retraction was applied in one place and not the other. So the notes asserted a claim they had already withdrawn 600 lines earlier.

Nothing shipped wrong. The sheet itself never carried the over-claim. A later session reading only the second copy would have cited it as established.

The sheet gives the reason rather than only the prohibition. A rule with no reason is the one people talk themselves out of.

**Evidence.**

- The instruction was added 2026-08-20. The split was found in the 2026-09-15 prose pass.
- The retraction is in D29, auto mode never skip-all.

**Checks.** none
