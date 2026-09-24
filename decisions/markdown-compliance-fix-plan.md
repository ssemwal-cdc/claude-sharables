---
id: D89
slug: markdown-compliance-fix-plan
kind: decision
status: settled
date: 2026-09-16
---
# Markdown compliance fix plan

**Rule.** Execute the 16 rulings below. Never widen them without a new interview.

**Outcome protected.** Every markdown file states what somebody observed, and a check holds it.

**Argument.** A four-lane review read all 218 markdown files on 2026-09-16.
The repo checks were green through the whole review.
So every defect it found was unchecked.
The review found 176 Simplified Technical English errors.
It found 8 teammate claims that no run supports.
It found 37 published numbers and paths with no script reader.
The maintainer was interviewed on each open decision.
These rulings are that interview.

**Rulings.**

| # | Item | Ruling |
|---|---|---|
| 1 | Sentence ceiling | `MAX_SENTENCE_WORDS` becomes 20. Fix every sentence that goes red |
| 2 | Fix scope | Text and checks land together. Each fix ships with the check that holds it |
| 3 | Published numbers and paths | All 37 get a reader. A missing `docs/onboarding.html` fails the build |
| 4 | Skill size | Move Step 8 and the lens sections to `references/`. Step 8 gets a mandatory read |
| 5 | PO cross-check unobserved, formerly a gap | Closed. Moved to F146, PO cross-check run confirmed. A full connector-mode run pulled the order and the history, and both checks ran. Still depends on ruling 7 |
| 6 | Notes page unseen, formerly a gap | Closed. Moved to F144, the note read on the record |
| 7 | F158, end-to-end runs confirmed | Closed 2026-09-24. The maintainer reports thousands of end-to-end runs. The ordinary approval path and the Procore execute walk are moot since D91, review-only plugins |
| 8 | F157, widget host bar confirmed | Closed 2026-09-24. The maintainer reports a thin bar with the item count and Filters stays pinned at the top on a real dashboard |
| 9 | Procore scheduled prompt unfired, formerly a gap | Closed. Moved to F147, missed window ran nothing later |
| 10 | procore `README.md:15` | Drop the two figures. Describe the narrowing without numbers |
| 11 | `F40`, the NetSuite toolbar port, with `F52`, amber was the real finding, `F62`, nothing runs without Chrome, and `F64`, two plugin commands exist | Keep the observed status. Write the reported observation into each Evidence line |
| 12 | `F57`, one disabled style two meanings | Two states reported. A new gap, `gaps/execute-button-blocked-state-unseen.md`, records the amber blocked state as unseen |
| 13 | Cowork storage leads, formerly a finding | Moved to G3, a gap for the unverified leads. Every citation rewritten |
| 14 | No duplicate-copy warning, and both slash forms resolve | Merged into `F8`, both slash forms resolve. It holds the run, both conclusions and the retraction. The old no-duplicate-copy-warning record is deleted |
| 15 | 15 findings over 45 lines | Split each into one observation per record |
| 16 | `docs/onboarding.html:192` | Keep the 45-minute figure. A finding marks it `unmeasured` |

**Evidence wording.** A maintainer report is not a measurement.
Every Evidence line from this interview reads as a report.
Use this form: `Reported by the maintainer, date unrecorded. The run is unmeasured.`

**Also in scope.** Fix all 176 linter errors in the 218 markdown files.
Fix the 14 errors in the 5 prose blocks under `plugins/_shared/`.
Fix the marker break at netsuite `SKILL.md:581`, per `D61`, markers on paragraph boundaries.
Replace the real vendor in the example at netsuite `SKILL.md:530`, per `D60`, shipped examples use placeholders.
Correct `README.md:126`, which names two version sites where four are enforced.
Correct `README.md:177`, which counts seven checks and omits the record checks.
Restate the coverage claim in `decisions/library-pins-checked-not-shared.md:24`.
A new library in one plugin passes the pin check today.
Restate the stale argument in `decisions/execute-bar-always-rendered.md:24`.
`F82`, the widget frame never scrolls, settled that question.
Point the drifted counts in `findings/netsuite-visual-read-thin.md` at a script.
Correct the 450-line figure in `findings/fewer-larger-tool-calls.md`.
The two files hold 730 and 561 lines today.
Add the silent-pass branch to `findings/mandate-gaps-closed.md:21`.

**Checks.** The pass widens `scripts/check_records.py` and `scripts/validate.py`.
Run the linter at error severity over every markdown file and every shared block.
Scan both `SKILL.md` files for sentence length and citation form.
Close the backticked slug hole in the citation check.
Close the `once` hole in the waiter-loop guard.
Refuse a record status that does not match its folder.
Re-point `scripts/test_skill_code.py` at any code block that moves.
Prove each new guard red on the defect it guards before the pass lands.

**Left open.** A record line ceiling is recommended and not ruled.
Ruling 15 splits 15 records today, and nothing stops the next one growing.

**Deferred records to close.** `D62`, never move safety prose into an on-demand file, is settled by ruling four.
`D85`, skill prose pass, is settled by rulings 1, 2 and 4.
