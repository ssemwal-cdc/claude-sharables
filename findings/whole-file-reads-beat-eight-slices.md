---
id: F61
slug: whole-file-reads-beat-eight-slices
kind: finding
status: settled
date: 2026-08-15
---
# One read beats eight slices of one file

**Outcome protected.** A session spends its turns on work, not on round trips.

**Argument.** This came from a review of one session's own inefficiency.
It is generic technique rather than repo knowledge, kept because it was
measured on real work.
The dominant cost is the number of round trips, not the size of any response.
Each round trip is a full model inference pass, which takes seconds.
The `grep` itself returns in milliseconds.
Prompt caching discounts re-sent context, so trimming output matters far less
than removing turns.

A `SKILL.md` file was hit with eight separate `sed` and `grep` ranges instead
of one read.
Reading it once would have cost fewer tokens than the slices summed.
It would also have surfaced every stale reference in one pass.
Instead they were discovered one at a time, after editing had started.

The counter-rule: a whole-file read is right for a skill-sized file.
It is wrong for a large source file, because those tokens then sit in context
for every later turn.
The heuristic is file size, not a principle.
Slicing discipline appropriate to a big codebase backfired on files small
enough to just read.

**Evidence.** Measured on this repo's own work, 2026-08-15.
The file at the time was read in eight slices.
Checked again 2026-09-17, `plugins/netsuite-approval-review/skills/`
`netsuite-approval-double-check/SKILL.md` is 730 lines and
`plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md`
is 561 lines.
Both are well past the size a single read stops paying for itself. So
the counter-rule is the operative one for both today.
The token cost of the eight slices against one read is `unmeasured` in
absolute terms.

**Checks.** none.
