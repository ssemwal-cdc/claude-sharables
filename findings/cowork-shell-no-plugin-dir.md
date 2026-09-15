---
id: pending
slug: cowork-shell-no-plugin-dir
kind: finding
status: observed
date: 2026-08-15
---
# Cowork shell cannot see plugins

**Outcome protected.** A stale workspace copy is visible instead of silent.

**Argument.**

The sandbox shell in Cowork cannot see the plugin directory at all. Only the connected workspace folder, outputs and uploads are mounted.

So on that surface the Step 0 copy never runs, and the workspace mirrors the last successful sync, which can lag the installed plugin.

The claim that the workspace always mirrors the installed plugin holds only where the shell can reach the plugin root.

This reopens the earlier diagnosis. A workspace stale because an old install kept restoring it, and one stale because nothing could restore anything, produce the same symptom. Only the first is fixed by updating the plugin.

Step 0 in both skills now carries a sync ladder. Rung 1 copies. Rung 2 reads and writes through the file tools. Rung 3 uses what is there and says so once.

**Evidence.**

- Observed in a live Cowork run 2026-08-15.
- The earlier reading is F‹stale-install-reads-as-repo-bug›, a stale install reads as a bug.

**Checks.** none
