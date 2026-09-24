---
id: D43
slug: skill-version-lines
kind: decision
status: settled
date: 2026-08-21
---
# Four synced version sites

**Rule.** Bump the skill version number, the date, the two descriptions and the README cell in one commit.

**Outcome protected.** A teammate can read which version of a skill they run, on the surface they are looking at.

**Argument.**

An installed skill is a snapshot. The desktop app shows its commit only deep in a menu, as Synced commit. See F48, app installs update in-app. No surface that shows a skill shows a commit.

So the version lives in four sites, one per surface that shows it. The start of the skill frontmatter description carries `vN`. The end of the `plugin.json` description carries `Skill version N — date.`. A plugin with several skills ends it with one `<skill> skill version N — date.` per skill, in skill-folder order. Its README cell carries `<skill> vN` per skill. The `SKILL.md` body line carries the same. The README table carries `vN`.

The body line reads `**Skill version N — YYYY-MM-DD.**` as the first line under the title.

The marketplace descriptions carry no version on purpose. A stale catalog could show a number that matches neither the installed copy nor `main`.

The line names GitHub as the only comparison point. A `git-subdir` install ships the plugin folder alone, so a local README lookup finds nothing.

A new skill starts at version 1. An installed copy with no version line predates 2026-08-21.

**Evidence.**

- Settled by screenshot 2026-08-21. The plugin detail page renders the `plugin.json` description in full and the skill description truncated to one line.
- A first live run reported its line correctly, then looked for the README table locally and found nothing. It proposed a `plugin.json` version field, the field D9, no version field bans.
- An app restart is not enough to see an update. See F66, restart the computer.

**Checks.** `scripts/validate.py` asserts every site exists and all four agree. It cannot enforce the bump.
