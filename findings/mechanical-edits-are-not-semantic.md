---
id: F32
slug: mechanical-edits-are-not-semantic
kind: finding
status: settled
date: 2026-08-15
---
# Mechanical edits do not need Edit's guard

**Outcome protected.** A session spends its turns on work, not on round trips.

**Argument.** Renumbering a list from 6 to 9 was three separate `Edit` calls, each
incrementing one digit.
Use `Edit` for semantic changes, where the exact-match guard earns its keep.
Do not use it for pure mechanics.

**Evidence.** Measured on this repo's own work, 2026-08-15.

**Checks.** none.
