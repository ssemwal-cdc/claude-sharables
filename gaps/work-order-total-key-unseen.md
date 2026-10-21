---
id: pending
slug: work-order-total-key-unseen
kind: gap
status: unobserved
date: 2026-10-21
---
# No folderless run has seen a work order payload

**Outcome protected.** A work order that can be read is read, not skipped on a guessed key.

**Argument.** With no folder connected, the Procore skill skips a `com` with no `grand_total`. D105, no folder and no reads where nothing can tie, sets that rule. No folderless run has seen a `WorkOrderContract` payload. If its total is not named `grand_total`, every folderless work order skips its reads.

**Evidence.** `unmeasured`. Likelihood is moderate until the first work order is observed. Do not cite the key as established.

**Checks.** none yet.
