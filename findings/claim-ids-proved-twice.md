---
id: F141
slug: claim-ids-proved-twice
kind: finding
status: observed
date: 2026-09-15
---
# The id claim ran clean twice

**Outcome protected.** Claiming ids never moves an existing id, and always rewrites the
citations it can.

**Argument.** The id claim was proved twice.
On this tree the dry run reports nothing pending.
On a scratch copy with two pending records, it assigned the next free number
per kind.
It rewrote one slug citation, converted one supersedes slug and regenerated
the three indexes.
No existing id moved.

**Evidence.** Measured on 2026-09-15, on this branch over `3a63144`, using a
scratch copy for the two-pending-record case.

**Checks.** `python3 scripts/check_records.py --claim-ids --apply`.
