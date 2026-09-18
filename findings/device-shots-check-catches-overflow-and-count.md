---
id: F143
slug: device-shots-check-catches-overflow-and-count
kind: finding
status: observed
date: 2026-09-16
---
# The device-shots check has three outcomes

**Outcome protected.** Every screen is measured at three widths and both themes, or the
gap is a stated note.

**Argument.** `D82`, hooks and checks pass, turns prose rules into checks.
This closes one more: every screen measured.

`check_device_shots()` reads `.claude/shots/summary.txt`.
It fails on any capture overflow, or on fewer than 18 rows.
Read against `scripts/check_records.py`'s `check_device_shots()` on
2026-09-17. It has a third branch: when the summary file is missing
entirely, it returns no problems at all.
That absence is a note from `device_shots_note()`, not a failure. So an
environment that never captured shots still passes this check silently.

A new `shots` CI job runs the capture and this check together.
`D81`, device usability check, names the check.

**Evidence.** Measured 2026-09-16, on this branch, with a `.bak` copy as the
undo.
Edited one capture's overflow to 12 in `summary.txt`.
The check went red, and named the file and the overflow count.
Restored the file.
The check went green with 18 rows and zero overflow.
Playwright 1.56.1 captured 18 files in `.claude/shots`, with zero overflow.

**Checks.** `python3 scripts/validate.py`.
