---
id: pending
slug: asset-paths-plugin-root
kind: decision
status: settled
date: 2026-08-11
---
# Reference assets through CLAUDE_PLUGIN_ROOT

**Rule.** Write every asset path as `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/assets/<file>`.

**Outcome protected.** A skill finds its own assets after it is installed.

**Argument.**

A bare relative asset path works in the repo and breaks once installed.

At run time the working directory is the user workspace, not the plugin folder.

So a path that resolves during development resolves to nothing for a teammate.

**Evidence.**

- Reproduced against Claude Code v2.1.227. Both skills reference assets through the variable.

**Checks.** `scripts/validate.py` rejects a bare `assets/` path and asserts every referenced asset exists.
