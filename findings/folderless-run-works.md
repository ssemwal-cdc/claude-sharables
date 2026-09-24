---
id: F76
slug: folderless-run-works
kind: finding
status: observed
date: 2026-08-26
---
# Folderless run works

**Outcome protected.** A teammate with no workspace folder can still review their queue.

**Argument.** Either plugin runs with no workspace folder connected.
The run interviews from scratch first, so it takes noticeably longer.
The run completes.
A caveat written the same day said the opposite, and that caveat is withdrawn.
The withdrawn chain was sound and its conclusion was wrong.
It argued that no folder makes every run a first run.
It argued that Step 0 rung 3 is therefore never available.
It argued that rung 1 fails on Cowork and rung 2 has never been observed.
It concluded that the skill must stop before Step 7.
Something in the ladder carries the run.
Rung 2 is the likely carrier.
A surface where rung 1 works is the other candidate.
Which rung carried it is unknown.
State what was observed, never what was derived.
A workspace folder is recommended, not required.
Cite this finding before calling the folder a hard requirement.

**Evidence.** 2026-08-26, reported by the maintainer, one run.
Which rung carried the run is `unmeasured`.
The plugin READMEs called the folder a hard requirement before this finding.
See F158, end-to-end runs confirmed, for the standing of run reports.

**Checks.** none.
