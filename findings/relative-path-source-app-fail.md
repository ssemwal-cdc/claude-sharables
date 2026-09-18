---
id: F7
slug: relative-path-source-app-fail
kind: finding
status: observed
date: 2026-08-11
---
# Relative source fails in app

**Outcome protected.** A teammate installing from the desktop app gets the plugin.

**Argument.**

A relative-path source works perfectly in the terminal, so it looks correct.

It then fails in the desktop app plugin browser. The catalog lists both plugins, and clicking install returns `Plugin couldn't be installed. Try again.`

The cause is in the Anthropic docs for the equivalent URL case. A surface that holds `marketplace.json` without a clone of the repo has nothing for a relative path to point at.

The docs say that URL-based marketplaces download the manifest file alone. Relative paths then reference files that were not downloaded.

The CLI works only because `marketplace add` clones the whole repository.

This is the subtle one, because the terminal gives no hint.

**Evidence.**

- Reproduced against Claude Code v2.1.227.
- The fix is D4, use git-subdir sources.

**Checks.** `scripts/validate.py` rejects a relative-path source string.
