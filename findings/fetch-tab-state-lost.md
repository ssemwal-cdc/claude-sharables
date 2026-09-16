---
id: F102
slug: fetch-tab-state-lost
kind: finding
status: observed
date: 2026-09-16
---
# Fetch tab navigated, first pass lost

**Outcome protected.** A run fetches its data once, and leaves no tab parked on a dead link.

**Argument.**

On a Procore run, one tab held the Step 2 gate and the fetched record data as page state. Step 4 then navigated that same tab to an attachment, to capture its presigned link. The navigation wiped the page state. The first data pass was redone from the start.

The same run ended with a tab parked on a presigned S3 link. The link had expired within its 60-second window, so the tab showed an error page and served nothing.

Both cases come from the same gap. No tab had a name, and no step said which tab does what, or when a tab closes. `D87`, a run closes its tabs, names the tabs and the close triggers.

**Evidence.**

- Observed 2026-09-16, on a Procore run. The time lost to the redone pass is `unmeasured`.
- The number of tabs left open at the end of that run is `unmeasured`.

**Checks.** none
