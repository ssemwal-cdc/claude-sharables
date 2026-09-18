---
id: F24
slug: stale-install-reads-as-repo-bug
kind: finding
status: observed
date: 2026-08-14
---
# Stale install reads as bug

**Outcome protected.** A maintainer checks the install version before editing a file that is already right.

**Argument.**

A report said that `publish_dashboard.py` hardcoded the change order type that returns a 400. The repo had shipped the working type the day before. Both observations were correct.

Procore Step 0 copies plugin assets over the workspace copies on every run. So the workspace mirrors the installed plugin, not the repo.

An install that predates the fix keeps restoring the old file. The natural reading blames the repo and points at a file that is already correct.

The tell is that `SKILL.md` describes behaviour the assets do not have. Prose and assets ship in one commit, so they cannot disagree in the repo, only across an install boundary.

The fix is the two-command update and a restart. See F9, update needs the marketplace qualifier.

**Evidence.**

- Reported 2026-08-14.
- Corrected 2026-08-15 by a live Cowork run. See F28, the Cowork shell cannot see the plugin.

**Checks.** none
