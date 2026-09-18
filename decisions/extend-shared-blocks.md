---
id: D49
slug: extend-shared-blocks
kind: decision
status: open
date: 2026-08-24
---
# Extend shared block coverage

**Rule.** Do not widen a shared block over prose that is only near-identical.

**Outcome protected.** A fix reaches both plugins, and neither plugin's own names get reworded away.

**Argument.** Sharing is cheap and mechanical for anything byte-identical.
The remaining blockers are real, not laziness.
Most remaining `SKILL.md` duplication is near-identical.
It differs by the plugin's own name and its workspace folder.
Closing that gap means designing those names out of the prose.
Some blocks differ by one token only.
`ns_marks_v1` against `pc_marks_v1` is one such pair.
The two log filenames are another.
See D58, canonical copy plus a check.

**Options.**

A. Leave coverage where it is. Cite this record when the percentage is questioned.

B. Design the per-plugin names out of the near-identical prose, then share it.

C. Parameterise the shared block mechanism so one token may differ per site.

**Recommendation.** A, until a defect crosses the gap it leaves.
Option B rewords correct prose to raise a number.
Option C is new machinery for a problem no defect has produced yet.

**Evidence.** Written 2026-08-24 at the end of the modularity work.
This record is not a commitment.
It records what was considered, deferred, and why.
Coverage today is `unmeasured` as a share of near-identical lines.
`F120`, six one-sided fixes, is the cost this
mechanism exists to stop.

**Checks.** `python3 scripts/shared_blocks.py --check`, run by `scripts/validate.py`.
