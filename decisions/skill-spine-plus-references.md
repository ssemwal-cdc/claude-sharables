---
id: D62
slug: skill-spine-plus-references
kind: decision
status: settled
date: 2026-08-24
---
# Thin spine plus reference modules

**Rule.** Never move safety or policy prose into a file that loads on demand.

**Outcome protected.** Every run reads every rule that governs it.

**Argument.** About a third of each skill is dead weight on any given run.
NetSuite's Step 5 loads in browser mode, where it cannot run.
Step 8 loads on review-only runs.
`ofci-analysis-cip` on this machine is the in-house precedent.
That skill is a 158-line spine plus four reference files.
A reference file loads on demand.
A rule the model must choose to read is the silent-degradation class this repo has spent fifty commits removing.
Step 8 is the hard case, because it is large and almost entirely safety.
The only defensible handling for Step 8 is an explicit mandatory read.
Lazy loading Step 8 is not defensible.
`scripts/test_skill_code.py` reads `SKILL.md` by path with no fallback.
Re-point that script in the same commit as any split.
See D85, which mandate rules bind the two prompts.

**Options.**

A. Leave both prompts whole.

B. Split the non-safety steps into `references/` and keep safety prose in the spine.

C. Split everything and make every reference read mandatory.

**Recommendation.** B, in the deferred skill prose pass, not before it.
Option C keeps the token cost and adds the file count.
The saving in option B is real only if the safety prose stays put.

**Evidence.** Written 2026-08-24 at the end of the modularity work.
This record is not a commitment.
The dead-weight share is estimated at about a third and is `unmeasured`.
The spine size of the in-house precedent is 158 lines.

- Settled 2026-09-17 by commit `4a81d8c`. It split Step 8 and the lens sections into
  `references/` in both `SKILL.md` prompts. Step 8 got a mandatory-read pointer in each
  spine. `scripts/shared_blocks.py`'s route-table check now also reads `references/`, so
  `D75`, gate the two type lists, still holds. Option B, chosen as recommended.

**Checks.** `scripts/shared_blocks.py`'s `check_execute_type_coverage`, which now also reads a
skill's `references/` files. `scripts/test_skill_code.py`, confirmed unaffected because the
extracted code blocks sit in Steps 2-4, outside both moved ranges.
