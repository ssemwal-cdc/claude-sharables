---
id: D56
slug: prerequisite-bucket
kind: decision
status: settled
date: 2026-08-24
---
# Plugins are prerequisite buckets

**Rule.** By default, put a new skill in an existing plugin only when its external prerequisites match that plugin exactly.

**Outcome protected.** A teammate can switch off the work they cannot run, and keeps the work they can.

**Argument.**

A teammate can switch off one skill inside a plugin. See F154, one plugin skill can be switched off. That switch now protects the outcome.

So the prerequisite boundary is a default, not a wall. It keeps each install line, update line and README to one system.

List the external prerequisites of the new skill. These are MCP connectors, browser-authenticated sites, CLI binaries, credentials and tenant access.

Compare that set to each existing plugin, exactly. An identical set joins that plugin. A different set gets a new plugin by default.

A different set may join an existing plugin when grouping helps the teammates who install it. Say why in the commit.

Always a new plugin when the skill ships `.mcp.json`, `hooks/`, `bin/`, `monitors/` or `.lsp.json`. Also a new plugin when it ships a root `settings.json` that must not apply to the other skills. Those activate on plugin enable, not on skill invocation. A skill switch cannot stop them.

A different audience also points to a new plugin by default.

Four reasons to split are rejected. A different topic, a different department, a different data domain and a different dashboard. So is a feeling of being unrelated. So is a plugin then holding more than one skill. So is folder tidiness.

Do not rename an existing plugin to match its bucket. The name must match the folder and the marketplace entry, and teammates installed by name.

Name a future plugin after its prerequisite, such as `monday-tools`, not after its first task.

Adding a skill to an existing plugin does not touch `marketplace.json`. The `skills/` folder is discovered automatically.

**Evidence.**

- Recorded 2026-08-24. Both plugins hold one skill today. That is an accident of porting two skills with two prerequisites.
- Amended 2026-09-24. The old argument said a single plugin skill cannot be silenced. F154, one plugin skill can be switched off, measured that false, so the rule became a default. The outcome is unchanged.
- The documented standard layout allows several skills in one plugin. `scripts/validate.py` blocks it today. See G17, multi-skill plugin unbuilt.
- Past 4 plugins, publish a dependency-only bundle plugin with bare string dependencies. Do not build it at 2 plugins.
- Auto sync does not install a new plugin. It keeps installed plugins current. So each new plugin costs one announcement and one install per teammate.
- Both slash forms resolve to the plugin skill. See F8, both slash forms resolve.
- Both plugins run in Cowork. See F2, Cowork runs installed plugins.

**Checks.** `scripts/validate.py` requires a non-empty `skills/` folder in every plugin.
