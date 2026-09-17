---
id: F8
slug: skill-invocation-verified
kind: finding
status: observed
date: 2026-08-11
---
# Both slash forms resolve

**Outcome protected.** A teammate can invoke a plugin skill by the short name.

**Argument.**

The short slash name resolves to the plugin skill while it is unambiguous.

The namespaced form, plugin name then colon then skill name, always works. Both are fine.

Assets travel with the plugin and are visible in the skill panel. The plugin root variable resolves them at run time.

**Retraction.** An earlier note claimed the short slash name meant a stale personal skill was shadowing the plugin.

Checked against this live run, that was false. The short name loads the plugin skill, with its own description and assets.

Do not warn a teammate about a duplicate standalone copy.

**Evidence.**

- Verified 2026-08-11 with `/netsuite-approval-double-check`, which ran the plugin copy.

**Checks.** none
