---
id: F84
slug: zero-billed-evidence-was-inverted
kind: finding
status: settled
date: 2026-08-20
---
# Zero billed was read as corroboration

**Outcome protected.** No correctly coded bill is flagged as miscoded.

**Argument.** The third of three compounding defects behind the phantom flag: the
zero-evidence was inverted.
A first draw and any pending bill both show no billed amount on the purchase
order.
That reading is expected, not corroboration.
The history query selected the approval status, and no rule ever spent it.

**Evidence.** Found by a teammate and confirmed against production 2026-08-20.
See `F71`, the bills this produced a false
flag on.

**Checks.** `scripts/test_skill_code.py` runs the code the cross-check step
carries.
