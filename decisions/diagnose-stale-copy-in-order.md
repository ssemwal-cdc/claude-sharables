---
id: D47
slug: diagnose-stale-copy-in-order
kind: decision
status: settled
date: 2026-08-24
---
# Diagnose stale copies in order

**Rule.** Check the install version, then the workspace template version, then the render date on the widget.

**Outcome protected.** A maintainer fixes the copy that is actually stale.

**Argument.**

The stale-copy family has three members and three different fixes.

A stale install needs the two-command update and a restart. A stale workspace needs the sync to run. A stale dashboard needs a re-render.

The symptoms overlap almost completely, so the order matters.

Check the installed version against `main`. Then check the workspace `layout template vN` against the version Step 0 states, which is a direct check rather than an inference from a modification date. Then check the render date on the widget.

The template version marker catches a torn sync only, not a stale one. See
`F‹template-version-check-blind-to-lockstep›`, the marker misses a stale sync.

**Evidence.**

- Recorded 2026-08-24 after two wrong diagnoses in 2026-08.
- `scripts/test_skill_code.py` fails if script and template disagree. `scripts/validate.py` fails if either disagrees with the version `SKILL.md` states.
- An old chat replays an old dashboard. See F30, old chats replay old dashboards.
- The terminal list sees CLI installs only. See F49, plugin list sees CLI installs.
- A run set the version line wording. See F50, a run set version wording.

**Checks.** `scripts/validate.py` and `scripts/test_skill_code.py` pin the template version marker.
