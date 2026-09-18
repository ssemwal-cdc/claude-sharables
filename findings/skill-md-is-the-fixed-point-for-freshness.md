---
id: F122
slug: skill-md-is-the-fixed-point-for-freshness
kind: finding
status: settled
date: 2026-08-24
---
# SKILL.md is the fixed point for freshness

**Outcome protected.** A run tells the user when its workspace copies are old.

**Argument.** Any check comparing two workspace files is blind, because staleness
moves both files in lockstep.
`SKILL.md` is the only fixed point, because it ships with the plugin.
It is current by construction even where the plugin directory cannot be
reached.

Step 0 now states the expected `layout template vN` and reads the workspace
copy back.
It reports a mismatch once and carries on.
That is the same fail-open posture as rung 3, because a stale layout still
renders correct verdicts.
That makes a third site for the template version per plugin.
`validate.py` now fails if `SKILL.md`, the template marker and the script
constant disagree.
Adding a synced site without adding its enforcement is the mistake this pass
cleaned up twice.

**Evidence.** Found 2026-08-24, the fix for
`F126`, the version check blind to
lockstep.

**Checks.** `scripts/validate.py` compares all three version sites.
