---
id: F126
slug: template-version-check-blind-to-lockstep
kind: finding
status: settled
date: 2026-08-24
---
# The version check missed lockstep staleness

**Outcome protected.** A run tells the user when its workspace copies are old.

**Argument.** A question found this, not a failure.
The question was whether to write the dashboard copies every run instead of
caching them.

The copy cannot be removed, and that part of the design is right.
`publish_dashboard.py` resolves its log, its template and its output from
`__file__`.
The Cowork sandbox does not mount the plugin directory into the shell.
So code that must run in that shell has to live inside the workspace.
Step 0 already says to overwrite the workspace copies on every run.

The question landed on a real hole.
`check_template_version()` compared two workspace files, the template's marker
against the script's constant.
Step 0 copies those two files together.
So they disagree only when a sync tears halfway.
A workspace that is uniformly three versions old has both files agreeing, and
publishes in silence.
So the marker caught a torn sync and never a stale one.
The maintainer index claimed outright that a stale copy names itself.
It does not.
That line is corrected rather than left as a claim nobody had tested.

**Evidence.** Found 2026-08-24.
Reproduced: template `v4` plus script `v4` against a plugin shipping `v6`
produced no warning at all.

**Checks.** `scripts/validate.py` compares all three version sites.
`scripts/test_skill_code.py` compares script and template.
