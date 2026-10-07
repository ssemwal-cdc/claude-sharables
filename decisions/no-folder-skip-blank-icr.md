---
id: pending
slug: no-folder-skip-blank-icr
kind: decision
status: settled
date: 2026-10-07
---
# No folder, no reads where nothing can tie

**Rule.** With no workspace folder connected, skip attachment reads on one kind of `icr` item. That is an item with a blank accepted cost and a blank Cost Impact. The verdict stays `skipped`.

**Outcome protected.** A folderless run does not spend its time re-reading files that cannot tie.

**Argument.**

Without a folder nothing persists. Every run re-reads every attachment.

An item with no figure on the record has nothing to tie to the support. Only check 3 could run.

The head says `support not read: no folder connected, nothing to tie`. Check 3 is named as not run.

**Evidence.**

- Owner ruling, 2026-10-07, from the 2026-10-07 field run.

**Checks.** none yet. The rule lives in the skill prose.
