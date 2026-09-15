---
id: F5
slug: no-duplicate-copy-warning
kind: finding
status: observed
date: 2026-08-11
---
# No duplicate-copy warning

**Outcome protected.** A teammate is not sent hunting for a shadow copy that does not exist.

**Argument.**

An earlier version of these notes claimed the short slash name meant a stale personal skill was shadowing the plugin.

That was wrong. Checked against a live run, the short name loads the plugin skill, with its own description and assets.

Do not warn users about duplicate standalone copies.

**Evidence.**

- Checked against a live run 2026-08-11.

**Checks.** none
