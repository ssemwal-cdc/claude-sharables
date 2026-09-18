---
id: F48
slug: app-store-separate-update-path
kind: finding
status: observed
date: 2026-08-21
---
# App installs update in-app

**Outcome protected.** A teammate can force an update and read which release they run.

**Argument.**

App-installed plugins live in the account-synced store of the app, not in `~/.claude/plugins`.

The force-update path is profile, then Settings, then Plugins, then Browse, then the Personal tab. Then it is the `claude-sharables` chip beside Local uploads, then the overflow menu, then Check for updates.

That menu also carries the Sync automatically toggle and shows Synced commit. Synced commit is the installed release and is directly comparable to the tip of `main`.

Two display traps sit nearby. The app labels the marketplace by repo name, not by marketplace name.

The Last updated column tracks the last commit to `marketplace.json`, not plugin content. So an old date there is not staleness.

Removing the marketplace from that menu uninstalls its plugins, and a re-add lands on current. That is the reliable last resort.

**Evidence.**

- Verified with screenshots 2026-08-21. The Last updated column read 2026-08-12 for a long stretch.
- The repo-name label is the split in D5, marketplace name differs from repo, surfacing in reverse.

**Checks.** none
