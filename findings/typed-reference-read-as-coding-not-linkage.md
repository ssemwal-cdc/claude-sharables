---
id: pending
slug: typed-reference-read-as-coding-not-linkage
kind: finding
status: settled
date: 2026-08-20
---
# A typed reference was read as the coding

**Outcome protected.** No correctly coded bill is flagged as miscoded.

**Argument.** The first of three compounding defects behind the phantom flag: a typed
reference was read as the coding.
The linkage fields and the Related Records panel appeared zero times in the
whole repo.
The query step already read the right table and never asked it for the link.
All three defects are now fixed in the cross-check step.

**Evidence.** Found by a teammate and confirmed against production 2026-08-20.
See `F‹phantom-po-miscoding-flag-was-wrong›`, the bills this produced a false
flag on.

**Checks.** `scripts/test_skill_code.py` runs the code the cross-check step
carries.
