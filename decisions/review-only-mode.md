---
id: pending
slug: review-only-mode
kind: decision
status: open
date: 2026-09-18
---
# Review-only mode

**Rule.** Ship review-only as a stored config key inside each existing plugin, never as a second plugin or a cloned repo. In `review-only` the skill has no Step 8.
The dashboard renders no mark button and no execute bar. It renders no header mirror.

**Outcome protected.** A reviewer with no approval authority gets a shorter dashboard, and one push to `main` still fixes every copy.

**Argument.**

The two plugins already run in review mode by default. Execute mode is Step 8, and it runs only on an explicit instruction. So the review path exists. What does not exist is a way to hide the decision controls. Some readers will never issue that instruction.

Two ways to get there were weighed.

A. A second plugin per lens, `netsuite-approval-review-readonly` and `procore-open-items-review-readonly`, each a copy with Step 8 removed.

B. One config key per plugin, asked once in Step 0 and stored in the state file.

B wins on the recorded arguments. D55, persona plugins, abandoned a fork per persona and named the cost: a second copy drifts. D56, plugins are prerequisite buckets, buckets by external prerequisite. Approval authority is not an external prerequisite. Both variants sign in to the same NetSuite or Procore. D2, first-run setup is per plugin, already gives the question a home. D79, repo workflow beats org protocol, is why a cloned repo is out: the teammate would hold two copies.

**Plan, in order.**

1. Add `mode` to the Step 0 setup questions in both `SKILL.md` files. Two values, `full` and `review-only`. Default `full`, so every existing state file keeps its behaviour. Store it under `config.mode`. D74, adopt config from conflict copy, covers it on a conflict.
2. In both `SKILL.md` files, add one line to the Two modes section. In `review-only`, Step 8 is not available. An execute instruction gets one line naming the mode and the key that changes it. Leave the Absolute rules alone. They are read-only rules and still hold.
3. In both `publish_dashboard.py` scripts, pass `config.mode` into the payload beside `me` and `tool`.
4. In both `dashboard_template.html` files, gate three things on the payload mode. The Approve, Approve with notes, Reject buttons and the reject-reason input in the row renderer. The execute bar in the `#bar` element. The header mirror. In review-only the row keeps the link, the details and the verdict pill. The bar region renders nothing, and the queue gets the height back.
5. The header mirror lives in `plugins/_shared/dash-header-mirror.block`. Edit the canonical block, then sync and check. D58, sync shared blocks from canonical. Test the gate inside the block, never in the two host templates, or the block drifts.
6. Extend `test_dashboard_view` in `scripts/test_skill_code.py`. Render both templates with `mode: review-only` and assert zero `onclick="mark(`, an empty `#bar`, and no mirror markup. Render with `mode: full` and assert the existing counts. A guard counts only once it goes red on the defect it guards. Break the gate once and watch it fail.
7. Run the float measurement by hand on the review-only render. D70, measure position in a browser. Record the bar height as zero and the queue rows visible in the first 700px.
8. Bump the four version sites in one commit. D43, four synced version sites.
9. Add a README line per plugin naming the mode and the question that sets it.

**What D37, render the execute bar always, says, and why this is not a repeal.** D37, render the execute bar always, protects a first-time reader. They see step 2 before doing step 1.

In review-only there is no step 2.
The bar would teach a step that does not exist for this reader.
Hiding it protects the same outcome from the other side. The reader is not shown a control they cannot use.
D37, render the execute bar always, stays settled for `full`. This record adds the one condition.
D46, the bar ignores filters, and D45, keep reference text out, are untouched. The bar is absent, not restyled.

**What this record does not do.** It does not change what a verdict means. A `clear` in review-only is still a recommendation. It does not add a third plugin, and it does not touch the marketplace file.

**Evidence.**

- Unmeasured. The 2026-08-24 measurement in D45, keep reference text out, put the bar at 153px in a 700px viewport. Review-only should return about a fifth of the frame to the queue. Confirm with step 7.
- The row buttons sit in the renderer at one site per template, observed 2026-09-18. The bar is one element. The mirror is one shared block. Three gates, no fourth.

**Checks.** `python3 scripts/validate.py`, `python3 scripts/test_skill_code.py`, and `scripts/measure_float.js` by hand.
