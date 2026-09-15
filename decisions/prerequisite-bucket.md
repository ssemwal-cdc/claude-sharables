---
id: pending
slug: prerequisite-bucket
kind: decision
status: settled
date: 2026-08-24
---
# Plugins are prerequisite buckets

**Rule.** Put a new skill in an existing plugin only when its external prerequisites match that plugin exactly.

**Outcome protected.** A teammate can switch off the work they cannot run, and keeps the work they can.

**Argument.**

A plugin is the unit a teammate can switch off. A skill is not. Every enable, disable, uninstall and scope control takes a plugin name.

The one setting that can silence a single skill does not apply to plugin skills. So everyone who installs a plugin takes all of it.

That makes the boundary a prerequisite boundary. List the external prerequisites of the new skill. These are MCP connectors, browser-authenticated sites, CLI binaries, credentials and tenant access.

Compare that set to each existing plugin, exactly. An identical set joins that plugin. Any difference at all means a new plugin.

Always a new plugin when the skill ships `.mcp.json`, `hooks/`, `bin/`, `monitors/`, `.lsp.json`, or a root `settings.json` that must not apply to the other skills. Those activate on plugin enable, not on skill invocation.

Also a new plugin when a different subset of the team should have it. Audience counts on its own.

Four reasons to split are rejected. A different topic, a different department, a different data domain and a different dashboard. So is a feeling of being unrelated. So is a plugin then holding more than one skill. So is folder tidiness.

Do not rename an existing plugin to match its bucket. The name must match the folder and the marketplace entry, and teammates installed by name.

Name a future plugin after its prerequisite, such as `monday-tools`, not after its first task.

Adding a skill to an existing plugin does not touch `marketplace.json`. The `skills/` folder is discovered automatically.

**Evidence.**

- Recorded 2026-08-24. Both plugins hold one skill today. That is an accident of porting two skills with two prerequisites.
- The documented standard layout allows several skills in one plugin. `scripts/validate.py` blocks it today. See G‹multi-skill-plugin-unbuilt›, multi-skill plugin unbuilt.
- Past 4 plugins, publish a dependency-only bundle plugin with bare string dependencies. Do not build it at 2 plugins.
- Auto sync does not install a new plugin. It keeps installed plugins current. So each new plugin costs one announcement and one install per teammate.
- Both slash forms resolve to the plugin skill. See F‹skill-invocation-verified›, both slash forms resolve.
- Both plugins run in Cowork. See F‹cowork-runs-plugins›, Cowork runs installed plugins.

**Checks.** `scripts/validate.py` requires a non-empty `skills/` folder in every plugin.
