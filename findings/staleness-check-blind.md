---
id: pending
slug: staleness-check-blind
kind: finding
status: settled
date: 2026-08-24
---
# Staleness check was blind

**Outcome protected.** A run tells the user when its workspace copies are old.

**Argument.** A question found this, not a failure.
The question was whether to write the dashboard copies every run instead of caching them.

**The copy cannot be removed, and that part of the design is right.**
`publish_dashboard.py` resolves its log, its template and its output from `__file__`.
The Cowork sandbox does not mount the plugin directory into the shell.
So code that must run in that shell has to live inside the workspace.
The every-run overwrite the question was reaching for already exists.
Step 0 says to do this on every run and that it overwrites the workspace copies deliberately.

**The question landed on a real hole.** `check_template_version()` compared two workspace files.
It compared the template's marker to the script's constant.
Step 0 copies those two files together.
So they disagree only when a sync tears halfway.
A workspace that is uniformly three versions old has both files agreeing, and publishes in silence.
So the marker caught a torn sync and never a stale one.
The maintainer index claimed outright that a stale copy names itself.
It does not.
That line is corrected rather than left as a claim nobody had tested.

**The fix has to live somewhere that always ships.** Any check comparing two workspace files is blind here.
Staleness moves both files in lockstep.
`SKILL.md` is the only fixed point, because it ships with the plugin.
It is current by construction even where the plugin directory cannot be reached.
Step 0 now states the expected `layout template vN` and reads the workspace copy back.
It reports a mismatch once and carries on.
That is the same fail-open posture as rung 3, because a stale layout still renders correct verdicts.
That makes a third site for the template version per plugin.
`validate.py` now fails if `SKILL.md`, the template marker and the script constant disagree.
Adding a synced site without adding its enforcement is the mistake this pass cleaned up twice.

**The general shape has appeared often enough to name.**
A check whose two inputs fail together cannot detect that failure.
Any freshness check needs one input that cannot go stale.
Same family as the connector-lag rule: verify the record, not the queue, because the queue lags with it.
Same family as the CCO wrong-id case, where a 200-empty response looks like no instance.

**Evidence.** Found 2026-08-24.
Reproduced: template `v4` plus script `v4` against a plugin shipping `v6` produced no warning at all.

**Checks.** `scripts/validate.py` compares all three version sites. `scripts/test_skill_code.py` compares script and template.
