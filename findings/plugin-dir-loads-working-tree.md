---
id: pending
slug: plugin-dir-loads-working-tree
kind: finding
status: observed
date: 2026-08-26
---
# plugin-dir loads the working tree

**Outcome protected.** A maintainer can prove a change installs before pushing it.

**Argument.**

`claude --plugin-dir ./plugins/<name>` loads the working tree. It reported the uncommitted new version where the marketplace install reported the old one.

It is also what the CLI suggests when a plugin is not installed.

It takes the plugin directory, not the repo root.

Schema-valid and installable are different things. Run `claude plugin validate` and this, both.

**Evidence.**

- Confirmed 2026-08-26, the same day as F‹marketplace-add-tests-published-tree›, marketplace add tests the release.
- The CLI text is `pass --plugin-dir <path> to load one from disk`.

**Checks.** none. This is a manual pre-push check.
