---
id: pending
slug: drift-check-built-from-six-defects
kind: finding
status: observed
date: 2026-08-24
---
# The drift check came out of six defects

**Outcome protected.** A one-sided edit, a reworded comment, a missing canonical file and
an orphaned one all fail the build.

**Argument.** The six one-sided defects led to the shared-block drift check.
See D58, canonical copy plus a check.

What is established by construction and by test: adding the markers changed no
content.
The check catches a one-sided edit, a reworded comment, a missing canonical
file and an orphaned one.
Each failure names the file and the differing line.
Editing one canonical file and running `--sync` reaches both plugins.
Both dashboards still render in headless Chromium, in both themes, with
markers embedded.

What is not established: nobody has yet fixed a real shared bug by editing the
canonical file mid-review.

**Evidence.** Audit dated 2026-08-24.
10 of the 22 commits that ever touched a `SKILL.md` touched both in the same
commit.
Every one of those ten was a mechanics or convention change, not a change to a
financial check.
The marker diff was 36 marker lines with zero deletions, verified by grepping
every changed line.
Coverage on 2026-08-24 was 13 blocks across 26 sites.
That is 9 blocks in the assets over 90 lines and 4 in the two `SKILL.md` files
over 34 lines.
Do not trust that figure once it is old.
`python3 scripts/shared_blocks.py --check` prints the live count, which cannot
be stale.
Mutation-tested at every step, including a one-sided pdf.js bump and a
reworded Step 0 paragraph.

**Checks.** `python3 scripts/shared_blocks.py --check`, run by
`scripts/validate.py`.
