---
id: F56
slug: dashboard-drift-six-defects
kind: finding
status: settled
date: 2026-08-24
---
# Six defects from dashboard drift

**Outcome protected.** A fix that reaches one plugin reaches the other one.

**Argument.** An audit compared the two plugins' assets against each other.
A question about making them more modular prompted it.
The finding worth keeping is the shape, not any single bug.
Every one of these is a case where one copy learned something and the other never did.

Six defects were fixed in one commit, on the NetSuite side unless noted.

1. Browser mode could not publish, so a complete review died at Step 7.
2. There was no verdict allowlist, so a typo'd verdict fell through the pill logic to "Clear".
   That is fail-open on the field that decides what gets approved.
   Procore has aborted on this since it shipped.
3. `var live=null` was never assigned, so about 45 lines were unreachable.
   Those lines held the gone and changed states, `newRow`, the bin and a permanently zero card.
4. Marks were never pruned, so a mark for an approved bill stayed in `ns_marks_v1` forever.
   It would reappear if NetSuite reused the id.
   Procore sweeps them.
5. The money card had no rollover, so a 2.7m dollar queue rendered as `$2702k`.
6. The abort message named `_review_log.json`, the pre-migration name, in both copies.
   So the rename fix reached neither string.

Defect 1 and the unused-config-keys defect share one root cause, an over-broad `required` list.
That is why this is six defects and not seven.
`me` and `tool` were injected and read by the page and never used.
Only `account` is used.

**The drift check came out of this.** See D58, canonical copy plus a check.
What is established by construction and by test: adding the markers changed no content.
The check catches a one-sided edit, a reworded comment, a missing canonical file and an orphaned one.
Each failure names the file and the differing line.
Editing one canonical file and running `--sync` reaches both plugins.
Both dashboards still render in headless Chromium, in both themes, with markers embedded.
What is not established: nobody has yet fixed a real shared bug by editing the canonical file mid-review.

**The honest limit.** The `SKILL.md` duplication is mostly near-identical rather than identical.
It is the same paragraph with the plugin's own name and workspace folder substituted.
So the block mechanism can never cover most of that surface as written.
See D49, do not widen a block over near-identical prose.

**What made this findable is the repo's own device.** Two independent sources said different things.
Neither copy could detect its own miss.
The difference here is that the second source was the other plugin, in the same repo the whole time.

**Evidence.** Audit dated 2026-08-24.
`dashboard_template.html`: 528 lines against 603, with 308 identical, 54.5% Dice.
`publish_dashboard.py`: 148 lines against 238, with 106 identical.
The CSS blocks alone were 92.5% identical.
Across the two `SKILL.md` files, 250 to 300 of 1,495 lines were duplicated or near-duplicated.
10 of the 22 commits that ever touched a `SKILL.md` touched both in the same commit.
Every one of those ten was a mechanics or convention change, not a change to a financial check.
The marker diff was 36 marker lines with zero deletions, verified by grepping every changed line.
Coverage on 2026-08-24 was 13 blocks across 26 sites.
That is 9 blocks in the assets over 90 lines and 4 in the two `SKILL.md` files over 34 lines.
Do not trust that figure once it is old.
`python3 scripts/shared_blocks.py --check` prints the live count, which cannot be stale.
Only 72 of about 1,500 lines sit in contiguous byte-identical runs.
Only about 34 of those have clean paragraph boundaries.
Mutation-tested at every step, including a one-sided pdf.js bump and a reworded Step 0 paragraph.

**Checks.** `python3 scripts/shared_blocks.py --check`, run by `scripts/validate.py`.
