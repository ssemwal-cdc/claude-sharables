---
id: F103
slug: version-line-silently-stale
kind: finding
status: observed
date: 2026-09-16
---
# A version line can silently miss its bump

**Outcome protected.** A teammate compares their installed version against the README table. That comparison means something, because the number moves when the skill does.

**Argument.**

PR #19 gave both skills a new Absolute rule and a Step 9 close-down. Neither skill's `**Skill version N — date.**` line changed. `scripts/validate.py` reported success. Its only check on the version lines is that the four sites agree with each other. That check is per `D43`, four synced version sites. It does not compare against what shipped before.

The result: a teammate ran `Check for updates`, then compared the version line to the README table. Both numbers agreed with each other and looked current. The skill underneath had already changed. The version display was not frozen by anything in the desktop app. The source never moved.

**Evidence.**

- Reported 2026-09-16, cross-checking `origin/main` at `50c281a` against the previous release.
- `plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md` and `plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md` both carried unchanged version lines across that commit's diff.

**Checks.** `python3 scripts/check_version_bump.py` now fails this case. See `D88`, the version bump is a check, not a habit.
