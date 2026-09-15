---
id: pending
slug: cco-multiple-holders-ungated
kind: decision
status: settled
date: 2026-08-14
---
# Several holders stay ungated

**Rule.** Dedupe the holder ids on a package. Report the ids and leave the item ungated when more than one remains.

**Outcome protected.** No live change order is logged as done because the wrong workflow was chosen.

**Argument.**

A package can span several commitment change orders, because the holder is per line rather than per package.

One id after deduplication is the answer.

Several ids mean there is no single workflow instance that the one queue row stands for.

Choosing one would be a guess with a silent failure mode. See F‹wrong-id-returns-200-empty›, a wrong id returns 200 empty.

**Evidence.**

- Recorded 2026-08-14 against the 5 packages in F‹cco-holder-id-route›, a CCO workflow hangs off holder.id.

**Checks.** none
