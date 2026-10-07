---
id: pending
slug: gate-timeout-is-failed
kind: decision
status: settled
date: 2026-10-07
---
# A gate timeout is failed

**Rule.** Each gate fetch aborts after 20 seconds. A timeout is `failed`, never `empty`. Each Chrome call stays near 20 rows of one endpoint family.

**Outcome protected.** A hung call never reads as a queue with no live instance.

**Argument.**

Two larger fan-out calls hung four minutes each in the field run.

An empty answer says that the API returned no instance. A hang proves nothing about the API.

D34, a failed call is unknown, made the same argument for NetSuite.

**Evidence.**

- Owner ruling, 2026-10-07, from the 2026-10-07 field run.

**Checks.** none. The gate code runs in a live browser tab only.
