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
A mention count is a snapshot, not a durable fact, and it has already drifted once.
See Evidence for the count as of this record's last check.
Both files name all six attachment outcomes.
So the doctrine holds formally.

It is left alone deliberately.
The `scanned` branch and the OCR cap are unfired on both sides.
No run has exercised either.
Writing more procedure for a path nobody has walked is what the hardcoded-packs rule prevents.
So the honest move is to note that NetSuite has less written down about the branch that never runs.
Fix it from a real observation when one arrives.
Do not fix it from symmetry.

**Evidence.** Mention counts are a snapshot from the command in Checks below, not a durable fact.
No script holds them current, so re-run the command before citing a figure.
Measured 2026-08-26: Procore `image` 11 times, `scanned` 10 times, NetSuite `image` 2 times, `scanned` 3 times.
Re-measured 2026-09-24: Procore `image` 12 times, `scanned` 11 times, NetSuite `image` 2 times, `scanned` 4 times.
The `scanned` counts drift on a wording change alone, not on a run.
G6, two branches still unfired, carries the unfired branches.
D65, write a pack from a role document, carries the rule invoked here.

**Checks.** `check_check_registry()` asserts both capability tables stay declared.
`check_visual_read_mentions()` in `scripts/check_records.py` counts image and
scanned mentions in every `SKILL.md` and fails on drift from the Evidence figures.
