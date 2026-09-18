---
id: F69
slug: contract-and-billed-off-unjoined-keys
kind: finding
status: settled
date: 2026-08-20
---
# Contract and billed totals used unjoined keys

**Outcome protected.** No correctly coded bill is flagged as miscoded.

**Argument.** The second of three compounding defects behind the phantom flag: contract
and billed-to-date were computed off two unjoined keys.
The contract came from a document-number string match.
The billed total came from a vendor and memo sum with no purchase order
predicate at all.

**Evidence.** Found by a teammate and confirmed against production 2026-08-20.
See `F71`, the bills this produced a false
flag on.

**Checks.** `scripts/test_skill_code.py` runs the code the cross-check step
carries.
