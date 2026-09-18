---
id: D88
slug: skill-version-bump-enforced
kind: decision
status: settled
date: 2026-09-16
---
# The version bump is a check, not a habit

**Rule.** `scripts/validate.py` fails a push that changes a skill's files. The skill's version number must be higher than the version at the branch's merge-base with `main`.

**Outcome protected.** A teammate compares their installed version against the README table. That number actually moved when the skill changed.

**Argument.**

`D43`, four synced version sites, requires the four to agree. It says so itself: `scripts/validate.py` "can enforce the match, not the bump — bumping is the habit." `F102`, fetch tab navigated, and `D87`, a run closes every tab it opened, (2026-09-16) landed a real content change to both skills. Each gained a new Absolute rule and a Step 9. Neither skill's version line moved. `validate.py` was green the whole time, because the four sites still agreed with each other. They just had not moved.

The fix is `scripts/check_version_bump.py`. It diffs the branch against its merge-base with `main`. It groups changed files by `(plugin, skill)`, then reads each skill's version line at both ends of that range. A skill with changed files but no higher version fails the build. A skill absent from the merge-base is new, and is exempt. That matches the "new skill starts at version 1" rule in `D43`, four synced version sites.

This is a repo-side check, not a git hook, on purpose. `.github/workflows/validate.yml` already runs `validate.py` on every push. This rides the existing gate instead of adding a second enforcement path a teammate could skip locally.

**Evidence.**

- Observed 2026-09-16: PR #19 changed both `SKILL.md` files. The version line on each stayed at the number that shipped the day before. See `F103`, version line silently stale.
- `scripts/check_version_bump.py`, run against that same diff by hand, fails with the message this decision describes.

**Checks.** `python3 scripts/check_version_bump.py` standalone, or `python3 scripts/validate.py` as part of the build gate.
