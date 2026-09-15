---
id: F11
slug: shared-state-filename-collision
kind: finding
status: observed
date: 2026-08-12
---
# A shared filename crossed records

**Outcome protected.** Each skill log holds its own records only.

**Argument.**

The two skills used to share a state filename, differing only by parent folder, with both folders under the same workspace parent.

An agent running both in one session resolved the bare name against the wrong folder.

It wrote NetSuite records into the Procore log.

So the filenames are distinct now, and each publish script migrates the old name in place.

**Evidence.**

- Observed 2026-08-12. One session, real cross-contamination.
- The rule is D15, one state file per skill.

**Checks.** none
