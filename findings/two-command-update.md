---
id: pending
slug: two-command-update
kind: finding
status: observed
date: 2026-08-11
---
# Updating needs two commands

**Outcome protected.** A maintainer can see whether an update actually shipped.

**Argument.**

`claude plugin marketplace update` refreshes the catalog only. It does not touch an installed plugin, and it reports success as though it did.

The plugin needs a second command. That command requires the `@marketplace` qualifier, and the bare name fails with an error pointing at the wrong problem.

The sequence works from any directory, because plugins install at `user` scope. Restart the app afterwards, as the CLI says.

Prefer these commands over the `/plugin` flow. They are scriptable, they print the before and after versions, and they surface the qualifier error.

These commands update terminal installs only. See F‹app-store-separate-update-path›, the app has its own store.

**Evidence.**

- Verified 2026-08-11. `claude plugin marketplace update compass-claude-plugins` prints `Successfully updated marketplace` while the installed version does not move.
- `claude plugin update netsuite-approval-review` fails with `Plugin "netsuite-approval-review" not found`. The plugin is installed and `claude plugin list` shows it.
- A successful update prints a SHA pair, for example `9ea01d3a5df2 -> 5c242055c130`.
- This is the split in D‹marketplace-name-vs-repo›, marketplace name differs from repo, reached from a command the verification snippet never exercises.

**Checks.** none
