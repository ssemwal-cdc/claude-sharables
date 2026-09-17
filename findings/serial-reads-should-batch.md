---
id: pending
slug: serial-reads-should-batch
kind: finding
status: settled
date: 2026-08-15
---
# Independent reads went out serially

**Outcome protected.** A session spends its turns on work, not on round trips.

**Argument.** Git state, the NetSuite step and the Procore recipe were independent
reads.
They went out as three separate messages instead of one.
Batched, the tools run concurrently and cost one inference pass instead of
three.

**Evidence.** Measured on this repo's own work, 2026-08-15.
Three independent reads went out as three messages.

**Checks.** none.
