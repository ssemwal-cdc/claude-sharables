---
id: D105
slug: no-folder-skip-blank-icr
kind: decision
status: settled
date: 2026-10-07
---
# No folder, no reads where nothing can tie

**Rule.** With no workspace folder connected, skip attachment reads on an item whose verdict is already fixed as `skipped`. The verdict is fixed before any read. Derive that set narrowly from the skill's verdict rules. The first case is an `icr` item with a blank accepted cost and a blank Cost Impact. An item an attachment could change is still read. Every skip names its outcome. D27, retry only an expired link.

**Outcome protected.** A folderless run does not spend its time re-reading files that cannot tie.

**Argument.**

Without a folder nothing persists. Every run re-reads every attachment.

An item with no figure on the record has nothing to tie to the support. Only check 3 could run.

Owner ruling, 2026-10-21, process-only: the skip is not limited to the `icr` case. Any item already certain to skip needs no read. If an attachment could change the verdict, the item is read.

The head says `support not read: no folder connected, nothing to tie`. Check 3 is named as not run.

**Holes, named.**

- The Procore skill names two certain-to-skip cases with no folder. Case (a): an `icr` with a blank accepted cost, a blank Cost Impact, and Vendor Proposed blank, absent or unmapped. Case (b): a `com` whose payload has no `grand_total`. An `inv` or a `cco` never qualifies.
- Owner ruling, 2026-10-21, process-only: keep skipping case (a). Check 3, `pc.icr-phase-sum` (the proposal's phase lines sum), could in principle flag from the attachment. That miss is unlikely. The read costs more.

**Evidence.**

- Owner ruling, 2026-10-07, from the 2026-10-07 field run.
- Owner ruling, 2026-10-21, widened the skip to every item certain to skip.

**Checks.** none yet. The rule lives in the skill prose.
