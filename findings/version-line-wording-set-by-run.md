---
id: pending
slug: version-line-wording-set-by-run
kind: finding
status: observed
date: 2026-08-21
---
# A run set version wording

**Outcome protected.** A teammate asking a skill its version gets an answer they can act on.

**Argument.**

Asked which version it ran, the installed skill reported its line correctly.

It then looked for the README table locally and found nothing, because a `git-subdir` install ships the plugin folder and never the repo root.

It reported the staleness check as unrunnable and proposed adding a `version` field to `plugin.json`. That is the field D‹no-version-field›, no version field, bans.

So the line now names GitHub as the only comparison point and rules the field out in place. Each plugin README carries the same note.

Anything the line asks a reader to do must work from the plugin folder alone.

**Evidence.**

- Observed on the first live run after 2026-08-21.

**Checks.** `scripts/validate.py` asserts the four version sites agree.
