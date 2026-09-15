---
id: D4
slug: git-subdir-sources
kind: decision
status: settled
date: 2026-08-11
---
# Use git-subdir marketplace sources

**Rule.** Give every marketplace entry a `git-subdir` source with its own `url` and a bare repo-relative `path`.

**Outcome protected.** A teammate can install from the desktop app, from the CLI, and through org sync.

**Argument.**

A `git-subdir` entry is self-contained. It carries its own `url` and `path`, so it resolves with or without a local clone.

Do not pin `sha` or `version`. Leaving the source unpinned is what makes every push ship.

A relative-path source installs from the CLI and fails everywhere else. See F7, relative path fails in the app.

A bare folder name is invalid outright. See F1, bare folder name rejected.

Leave `metadata.pluginRoot` unset. See D7, pluginRoot does not work.

A full git URL needs the `.git` suffix. See F4, dot-git suffix required.

**Evidence.**

- Verified against Claude Code v2.1.227 by reproducing each failure.
- The CLI works with a relative path only because `marketplace add` clones the whole repository.

**Checks.** `scripts/validate.py` rejects a relative-path source string and rejects `metadata.pluginRoot`.
