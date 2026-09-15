---
id: F79
slug: netsuite-visual-read-thin
kind: finding
status: settled
date: 2026-08-26
---
# NetSuite visual read prose thin

**Outcome protected.** Procedure gets written from an observation, not from symmetry.

**Argument.** The 2026-08-26 parity audit noticed this and recorded it rather than acting on it.
Procore's `SKILL.md` says `image` 11 times and `scanned` 10 times.
NetSuite's says them 2 times and 3 times.
Both files name all six attachment outcomes.
So the doctrine holds formally.

It is left alone deliberately.
The `scanned` branch and the OCR cap are unfired on both sides.
No run has exercised either.
Writing more procedure for a path nobody has walked is what the hardcoded-packs rule prevents.
So the honest move is to note that NetSuite has less written down about the branch that never runs.
Fix it from a real observation when one arrives.
Do not fix it from symmetry.

**Evidence.** Mention counts measured 2026-08-26 across the two `SKILL.md` files.
Procore: `image` 11, `scanned` 10.
NetSuite: `image` 2, `scanned` 3.
G6, two branches still unfired, carries the unfired branches.
D65, write a pack from a role document, carries the rule invoked here.

**Checks.** `check_check_registry()` asserts both capability tables stay declared.
