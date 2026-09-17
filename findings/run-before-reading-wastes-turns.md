---
id: pending
slug: run-before-reading-wastes-turns
kind: finding
status: settled
date: 2026-08-15
---
# Running before reading wasted two turns

**Outcome protected.** A session spends its turns on work, not on round trips.

**Argument.** A fixture run failed because `publish_dashboard.py` resolves paths from
`__file__` and ignored the flags passed to it.
Five lines read first would have prevented two wasted turns.
The same applies to `node --check` against a process substitution.

**Evidence.** Measured on this repo's own work, 2026-08-15.
Two turns were wasted by running before reading.

**Checks.** none.
