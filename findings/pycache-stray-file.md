---
id: F95
slug: pycache-stray-file
kind: finding
status: observed
date: 2026-09-01
---
# Python bytecode left a stray

**Outcome protected.** The workspace folder holds only files a step names.

**Argument.**

Running the publish script left a bytecode cache folder in a folder that refuses deletes.

It is the one file in that folder no step names and nobody chose.

So the fix is to never create it. Both skills now invoke Python with the flag that writes no bytecode.

This is the stray-file rule broken by the tooling rather than by a step.

**Evidence.**

- Observed 2026-09-01. The folder was a few kilobytes. Its exact size is `unmeasured`.

**Checks.** none
