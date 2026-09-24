---
id: F154
slug: plugin-skill-switch-off
kind: finding
status: observed
date: 2026-09-24
---
# One plugin skill can be switched off

**Outcome protected.** A teammate can switch off the work they cannot run, and keeps the work they can.

**Argument.**

A permission deny rule on the Skill tool silences one skill inside an installed plugin. The other skills in that plugin stay available.

The rule takes the skill name in the short form or the namespaced form. Both forms block the skill.

The desktop app also has a per-skill toggle inside a plugin. The maintainer observed it there.

So the plugin is no longer the smallest thing a teammate can switch off. D56, plugins are prerequisite buckets, rested on that claim.

A skill toggle does not reach what activates on plugin enable. D56, plugins are prerequisite buckets, names those files. They still force a new plugin.

**Evidence.**

- Measured 2026-09-24 on Claude Code 2.1.281. The NetSuite plugin loaded through `--plugin-dir`, in auto mode.
- With no rule, the skill loaded and quoted its version line.
- With `Skill(netsuite-approval-double-check)` denied, the Skill tool returned "Skill execution blocked by permission rules".
- With `Skill(netsuite-approval-review:netsuite-approval-double-check)` denied, the Skill tool returned the same text.
- The desktop toggle is a maintainer observation. Its menu path is not recorded.
- Whether a denied skill still costs context through its listing is `unmeasured`.
- Cowork is `unmeasured`.

**Checks.** none
