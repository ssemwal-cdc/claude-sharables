---
id: pending
slug: plugin-json-only-in-claude-plugin
kind: decision
status: settled
date: 2026-08-11
---
# Only plugin.json in claude-plugin

**Rule.** Put nothing except `plugin.json` inside `.claude-plugin/`.

**Outcome protected.** A plugin installs and its skills are discovered.

**Argument.**

`skills/` at the plugin root is discovered automatically, so `plugin.json` needs no `skills` key.

A `skills/`, `commands/`, `agents/` or `hooks/` folder inside `.claude-plugin/` is not found.

`plugin.json` itself is required. Without it the install fails.

**Evidence.**

- Verified against Claude Code v2.1.227 with the two shipped plugins.

**Checks.** `scripts/validate.py` requires `plugin.json` and a non-empty `skills/` folder.
