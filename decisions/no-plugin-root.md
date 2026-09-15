---
id: pending
slug: no-plugin-root
kind: decision
status: settled
date: 2026-08-11
---
# Never use metadata.pluginRoot

**Rule.** Leave `metadata.pluginRoot` unset.

**Outcome protected.** Every registered plugin resolves at install.

**Argument.**

The key is documented and does not work. See F‹plugin-root-does-not-work›, pluginRoot does not work.

Use a self-contained `git-subdir` source instead. See D‹git-subdir-sources›, use git-subdir sources.

**Evidence.**

- Reproduced against Claude Code v2.1.227.

**Checks.** `scripts/validate.py` rejects the file if the key reappears.
