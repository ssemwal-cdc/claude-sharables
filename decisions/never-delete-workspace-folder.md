---
id: pending
slug: never-delete-workspace-folder
kind: decision
status: settled
date: 2026-08-24
---
# Never delete the workspace folder

**Rule.** Never delete the workspace folder or its asset copies to fix a stale copy.

**Outcome protected.** A run with a broken sync still has the last good assets and the state file.

**Argument.**

The copies are stale because the write failed. Deleting the destination does not make the plugin root reachable.

The next run fails the same way, and rung 3 of the sync ladder then has nothing to fall back on. Delete-then-write converts a fail-open into a fail-closed.

It also destroys the state file in that folder. That file holds `config`, the review history and `lastCompletedRun`. Publish then aborts rather than guessing an identity.

The narrow version, deleting the two asset files and keeping the log, only helps where the sync can already run.

**Evidence.**

- Recorded 2026-08-24.
- The reachability limit is F‹cowork-shell-no-plugin-dir›, the Cowork shell cannot see the plugin.

**Checks.** none
