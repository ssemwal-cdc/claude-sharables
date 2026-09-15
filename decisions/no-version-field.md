---
id: D9
slug: no-version-field
kind: decision
status: settled
date: 2026-08-11
---
# No version field anywhere

**Rule.** Never add a `version` field to `plugin.json` or to a marketplace entry.

**Outcome protected.** Every push to `main` reaches everyone who has the plugin.

**Argument.**

With no `version` field the version resolves from the git commit SHA. Every push to `main` is a new version.

A `version` string needs a bump. A forgotten bump leaves everyone on their cached copy, so the fix never ships.

The rule bans the machine fields only. The human marker is required. See D43, four synced version sites.

**Evidence.**

- Confirmed 2026-08-11. `claude plugin list` prints a commit SHA prefix as the version, for example `7ca6a2ea2c70`.
- `claude plugin validate` warns `No version specified`. That warning is expected here. See D83, expected validator warning.

**Checks.** `scripts/validate.py` rejects a `version` field in `plugin.json` and in `marketplace.json`.
