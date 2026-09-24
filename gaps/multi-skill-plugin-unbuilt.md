---
id: G17
slug: multi-skill-plugin-unbuilt
kind: gap
status: unobserved
date: 2026-09-15
---
# Bundle plugins are unbuilt

**Outcome protected.** Nobody follows a documented standard that the build then rejects.

**Argument.**

D56, plugins are prerequisite buckets, names two layouts the build used to reject. The first is several skills in one plugin. The second is a dependency-only bundle plugin.

The first wall fell on 2026-09-24. `scripts/validate.py` now reads one version tail per skill in a multi-skill `plugin.json`. See D43, four synced version sites.

The bundle wall stands. A dependency-only manifest has no `skills/` folder, and `scripts/validate.py` requires a non-empty one. The bundle case needs a carve-out for a `dependencies` key.

D56, plugins are prerequisite buckets, defers the bundle until past 4 plugins. So this gap stays open on purpose.

**Evidence.**

- Never observed. No bundle plugin exists.
- The bundle wall is read from `scripts/validate.py` as of 2026-09-24. It has not been triggered, so the exact failure text is `unmeasured`.
- The multi-skill wall was measured before it fell. A two-skill fixture failed the old check and passes the new one. `scripts/test_validate_versions.py` holds that proof.
- Deferred 2026-09-24 by the maintainer. Revisit G17 after the current gap work lands. Start from the maintainer's second marketplace, `ssemwal-cdc/glen-tools`, which copies this repo's scripts.

**Checks.** `scripts/test_validate_versions.py` for the fallen wall. none for the bundle wall.
