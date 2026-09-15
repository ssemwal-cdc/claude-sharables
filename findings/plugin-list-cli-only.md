---
id: pending
slug: plugin-list-cli-only
kind: finding
status: observed
date: 2026-08-21
---
# plugin list sees CLI installs

**Outcome protected.** An empty terminal list is not read as a missing install.

**Argument.**

`claude plugin list` returned empty on a machine where both plugins were installed and working through the desktop app.

The CLI and the app keep separate inventories. The CLI inventory is `~/.claude/plugins/installed_plugins.json`. The app keeps its own store.

So the terminal update commands touch the CLI copy only, and an empty list does not mean the app has no plugins.

Update app installs through the app. See F‹app-store-separate-update-path›, the app has its own store.

**Evidence.**

- Confirmed 2026-08-21 on a machine with working app installs.

**Checks.** none
