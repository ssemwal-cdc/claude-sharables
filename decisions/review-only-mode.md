---
id: D91
slug: review-only-mode
kind: decision
status: settled
date: 2026-09-18
---
# Review-only plugins

**Rule.** Remove execute mode from both plugins. Move every removed line of prose and code into `actionable-retired/`, one file per source, named by its original path.
Do it in one pull request, from one branch, so one `git revert` of the merge commit also puts it back.
Keep every state key and every mark key as it is, so a reinstated execute mode reads old logs unchanged.

**Outcome protected.** A reviewer gets a dashboard with no decision controls. A future session can read what was removed, diff it against the live files, and put it back.

**Argument.**

The owner chose this on 2026-09-18, after weighing a second plugin and a stored mode key.
Both kept execute mode alive for somebody. Nobody needs it today.
Dead code that no user can reach is not built, so it goes.

Reinstatement has to stay cheap, and readable without git archaeology.
So the removed material lives in `actionable-retired/`, in the tree, where a session can open it and diff it.
Git gives the second path. When the removal is one merge commit, one revert restores everything together.
Splitting the removal across several pull requests would make that revert a hunt.

The folder sits at the repo root, outside `plugins/`, so nothing in it installs or ships. The validator skips it.

The three things a revert cannot fix are the reasons for the three guard rules below.

**Reinstatement recipe.** Two paths, and the folder README carries both.
By hand: open `actionable-retired/`, read its README map, and paste each file back at the path it names. Diff first, because the live file may have moved on.
By git: tag the last `main` commit before the merge as `execute-mode-last`. Run `git revert -m 1 4b0dff1` on a branch, resolve drift against the tag, and open a pull request.
The superseded records below return to `settled` in that same pull request.

**Guard rules for the removal.**

1. Never rename or delete a state file key. The `actions` array stays, empty on new runs, and is never read. D15, one state file per skill, and D74, adopt config from conflict copy, still apply.
2. Never rename a per-item marks key. D38, never rename a marks key, still applies, even with nothing writing them.
3. Never change what a verdict means. A `clear` stays a recommendation. D63, gate verdicts against publish, still applies.

**Plan, in order.**

1. Tag `main` at its current head as `execute-mode-last` and push the tag. Create `actionable-retired/` with a README. The README holds the reinstatement recipe and a two-column map: retired file, original path and lines.
2. In both `SKILL.md` files, cut the Two modes section, Step 8 and the execute-only Absolute rules. Save each cut as `actionable-retired/<plugin>/SKILL.md.cut.md`. Renumber Step 9 to Step 8. Keep the rule that never calls a write endpoint. Keep the rule that never approves on its own judgement.
3. Move both `references/step-8-execute.md` files into the folder under their plugin. Cut the execute paragraph from `references/lenses-delivery-design.md` into a `.cut.md` beside them.
4. In both `dashboard_template.html` files, cut the decision controls. That is the three buttons and the reject-reason input. It is the `mark` and `setText` functions. It is the `#bar` element, its renderer, and the marks read from local storage. Save the cut as `actionable-retired/<plugin>/dashboard_template.cut.html`, with a line comment at each cut site in the live file. Keep the row link, the details and the verdict pill. Keep every mark-key name in a comment naming this record.
5. Move `dash-header-mirror.block` into `actionable-retired/_shared/` and remove its marked sites. Cut the execute lines from `dash-band-track.block`, `dash-of-total.block`, `skill-artifact-host.block` and `skill-close-down.block` into `.cut` files beside it. Sync and check. D58, sync shared blocks from canonical.
6. In both `publish_dashboard.py` files, cut the execute payload fields into `publish_dashboard.cut.py`. Keep reading `actions` so an old log still loads.
7. In `scripts/shared_blocks.py`, move `check_execute_type_coverage` and `check_execute_prompt_purity` into `actionable-retired/scripts/`. Remove their two calls from `scripts/validate.py`. Add `actionable-retired/` to the validator's skip list. Keep the verdict checks.
8. In `scripts/test_skill_code.py`, move `test_gate_states` and the bar and mirror assertions of `test_dashboard_view` into `actionable-retired/scripts/`. Add one assertion that neither template contains `onclick="mark(` or an element with id `bar`. Break it once and watch it go red.
9. Run the float measurement by hand on both renders. D70, measure position in a browser. Record the queue rows visible in the first 700px as a finding.
10. Mark eleven decisions `superseded`, each citing this record. They are D14, never pre-write an action, through D78, an unmapped subtype keeps buttons, and the list sits under Evidence. Close G7, execute button blocked state unseen, and G16, purchase order route unfired, as moot. Regenerate the indexes.
11. Rewrite the marketplace descriptions, the READMEs, `CLAUDE.md` and the onboarding sheet. No line may say the dashboard approves or responds. D33, the page is the file. Add a `CLAUDE.md` line naming `actionable-retired/` as read-only reference.
12. Bump the four version sites in one commit. D43, four synced version sites.
13. Open one pull request. The maintainer claims ids in the last commit and merges. The merge sha goes into this record under Evidence.

**What stays.** D6, never act without an instruction, stays settled. It is now trivially true and still the right rule if execute mode returns. D29, auto mode, stays. D87, a run closes its tabs, stays.

**Evidence.**

- Surveyed 2026-09-18. Step 8 is one section plus one reference file per plugin. The controls sit in one row renderer, one bar element and one shared block per template.
- Eleven decisions describe execute behaviour only. D14, never pre-write an action. D18, never batch the click checks. D20, default the approval comment. D28, Approve With Notes stays primary. D37, render the execute bar always. D45, keep reference text out. D46, the bar ignores filters. D48, the message authorises only. D75, gate the two type lists. D76, purchase orders take bill route. D78, an unmapped subtype keeps buttons.
- Two gaps do. G7, execute button blocked state unseen. G16, purchase order route unfired.
- Built on branch 2026-09-18. The retired folder holds 21 files. Two shared blocks, the measurement script and the float header were not in the plan. The retired README names each. Merged 2026-09-18 as 4b0dff1. Reinstate with `git revert -m 1 4b0dff1`.

**Checks.** `python3 scripts/validate.py`, `python3 scripts/test_skill_code.py`, and `scripts/measure_float.js` by hand.
