---
id: G17
slug: multi-skill-plugin-unbuilt
kind: gap
status: unobserved
date: 2026-09-15
---
# Multi-skill plugins are unbuilt

**Outcome protected.** Nobody follows a documented standard that the build then rejects.

**Argument.**

D56, a plugin is a prerequisite bucket, tells a maintainer to put a second skill inside an existing plugin when the prerequisites match.

`scripts/validate.py` blocks that today. Its per-skill check asserts that the `plugin.json` description ends with `Skill version N — DATE.`.

A string can end with one tail only. So two skills at different versions can never both pass. The failure message in the script says as much.

The same file blocks the bundle plugin from the same decision. Its check requires a non-empty `skills/` folder, and a dependency-only manifest has neither a folder nor an entry.

So the check needs widening before either instruction can be followed. The bundle case needs a carve-out for a `dependencies` key.

Nobody has tried it. The failure would land on whoever tries, not on whoever wrote the advice.

**Evidence.**

- Never observed. No plugin in this repo holds a second skill, and no bundle plugin exists.
- Both walls are read from `scripts/validate.py` as of 2026-09-15. Neither has been triggered, so the exact failure text is `unmeasured`.

**Checks.** none. Widening `scripts/validate.py` is the work this gap names.
