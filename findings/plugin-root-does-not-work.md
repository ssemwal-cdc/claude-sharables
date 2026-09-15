---
id: pending
slug: plugin-root-does-not-work
kind: finding
status: observed
date: 2026-08-11
---
# pluginRoot does not work

**Outcome protected.** Nobody spends a round on a documented shortcut that fails at install.

**Argument.**

The Anthropic docs say that `pluginRoot` lets you shorten a source to a bare name. It does not.

That combination fails the same way a bare name fails on its own.

`pluginRoot` plus a relative name passes validation and then resolves the source from the repo root anyway. Install fails with `Source path does not exist`.

**Evidence.**

- Reproduced against Claude Code v2.1.227.
- The rule is D‹no-plugin-root›, never use pluginRoot.

**Checks.** `scripts/validate.py` rejects the file if `metadata.pluginRoot` reappears.
