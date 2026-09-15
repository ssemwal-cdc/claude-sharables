---
id: F29
slug: fewer-larger-tool-calls
kind: finding
status: settled
date: 2026-08-15
---
# Fewer, larger tool calls

**Outcome protected.** A session spends its turns on work, not on round trips.

**Argument.** This came from a review of one session's own inefficiency.
It is generic technique rather than repo knowledge.
It is kept because it was measured on real work.
The dominant cost is the number of round trips, not the size of any response.
Each round trip is a full model inference pass, which takes seconds.
The `grep` itself returns in milliseconds.
Prompt caching discounts re-sent context.
So trimming output matters far less than removing turns.

What went wrong, in rough order of cost.

- **Reading one file in eight slices.** `SKILL.md` is about 450 lines.
  It was hit with eight separate `sed` and `grep` ranges.
  Reading it once would have cost fewer tokens than the slices summed.
  It would also have surfaced every stale reference in one pass.
  Instead they were discovered one at a time, after editing had started.
- **Serial independent reads.** Git state, the NetSuite step and the Procore recipe were independent.
  They went out as three messages.
  Batched, the tools run concurrently and cost one inference pass.
- **Running before reading.** A fixture run failed because `publish_dashboard.py` resolves paths from
  `__file__` and ignored the flags passed to it.
  Five lines read first would have prevented two wasted turns.
  The same applies to `node --check` against a process substitution.
- **Mechanical edits as separate calls.** Renumbering a list from 6 to 9 was three `Edit` calls.
  Each incremented one digit.
  Use `Edit` for semantic changes, where the exact-match guard earns its keep.
  Do not use it for pure mechanics.

**The counter-rule.** A whole-file read is right for a 450-line skill.
It is wrong for a large source file, because those tokens then sit in context for every later turn.
The heuristic is file size, not a principle.
Slicing discipline appropriate to a big codebase backfired on files small enough to just read.

**Evidence.** Measured on this repo's own work, 2026-08-15.
`SKILL.md` is about 450 lines and was read in eight slices.
Three independent reads went out as three messages.
Two turns were wasted by running before reading.
The token cost of the eight slices against one read is `unmeasured` in absolute terms.

**Checks.** none.
