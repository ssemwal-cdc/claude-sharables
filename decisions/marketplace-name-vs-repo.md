---
id: pending
slug: marketplace-name-vs-repo
kind: decision
status: settled
date: 2026-08-11
---
# Marketplace name differs from repo

**Rule.** Pass the repo to `marketplace add` and the marketplace name to `install`. Never make the two agree.

**Outcome protected.** A teammate's install command works the first time.

**Argument.**

The repo is `ssemwal-cdc/claude-sharables`. The marketplace is `compass-claude-plugins`, from the `name` key in `marketplace.json`.

So `add` takes the repo and `install` takes the marketplace. This looks like a typo and is not.

The same split surfaces in the update commands. See F‹two-command-update›, update needs the marketplace qualifier.

It surfaces in reverse in the desktop app, which labels the marketplace by repo name. See F‹app-store-separate-update-path›, the app has its own store.

**Evidence.**

- Verified 2026-08-11. `/plugin marketplace add ssemwal-cdc/claude-sharables` then `/plugin install <plugin-name>@compass-claude-plugins`.
- The bare plugin name fails an update with `Plugin "netsuite-approval-review" not found` while the plugin is installed.

**Checks.** none
