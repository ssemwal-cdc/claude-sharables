---
id: pending
slug: waiter-loop-check-fires-on-defect
kind: finding
status: observed
date: 2026-09-16
---
# The waiter-loop check fires on a real defect

**Outcome protected.** No sentence in this repo instructs an unbounded wait-and-retry.

**Argument.** `D82`, hooks and checks pass, turns prose rules into checks.
This closes one more: no waiter loop.

`check_waiter_loops()` reads `CLAUDE.md`, the three `README.md` files, every
record, both `SKILL.md` files and every shared block.
It fails on an unbounded wait-and-retry sentence.

**Evidence.** Measured 2026-09-16, on this branch, with a `.bak` copy as the
undo.
Inserted one unbounded wait-and-retry sentence into a record.
The check went red, and named the file, the line and the sentence.
Restored the record. The check went green.

**Checks.** `python3 scripts/validate.py`.
