# Retired execute mode

This folder is read-only reference. Nothing here installs and nothing here ships.
It sits outside `plugins/`, so no plugin, no check and no scanner reads it.

It holds every line of prose and code that `review-only-mode` cut out of the two plugins.
One file per source file, named after its original path. Each entry carries the original
path and the line range it occupied at the moment of the cut.

## What was removed

Execute mode. On each dashboard that is the decision controls, the batched execute bar,
the header mirror, and the per-item marks in `localStorage`. In each skill it is Step 8.
In the build it is the two shared-block checks that guarded execute.

## What was kept, on purpose

- Every state file key. The `actions` array stays in both schemas, empty on new runs, and is
  never read. `D15`, one state file per skill, and `D74`, adopt config from conflict copy.
- Every per-item marks key name, recorded in a comment in each `dashboard_template.html`.
  `ns_marks_v1` and `pc_marks_v1` are never renamed and never reused. `D38`, never rename a
  marks key.
- What each verdict means. A `clear` is still a recommendation and authorises nothing.
  `D63`, gate verdicts against publish.

## Reinstatement, by hand

Read the map below. Open each retired file, and paste each chunk back at the path it names.
Diff first, because the live file has moved on since the cut. A chunk headed `sentence trim`
records a `was:` line and a `now:` line. Put the `was:` text back over the `now:` text.

## Reinstatement, by git

The last `main` commit before the removal is `cdaaf90`. A local tag `execute-mode-last`
points at it. **That tag exists only in one working copy. It was never pushed, so it is not
on the remote and nobody else has it.** Use the sha, and re-create the tag if you want one.

Run `git revert -m 1 4b0dff1` on a branch. `<merge sha>` is the merge commit of the
removal pull request. Resolve drift against `cdaaf90`, then open a pull request. The
superseded decisions return to `settled` in that same pull request.

## Map

| Retired file | Original path | Lines at the time of the cut |
|---|---|---|
| `netsuite-approval-review/SKILL.md.cut.md` | `plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md` | 12-16, 30-31, 164, 578, 595-598, 608-609, plus 10 sentence trims |
| `netsuite-approval-review/references/step-8-execute.md` | `plugins/netsuite-approval-review/skills/netsuite-approval-double-check/references/step-8-execute.md` | whole file, 116 lines |
| `netsuite-approval-review/dashboard_template.cut.html` | `plugins/netsuite-approval-review/skills/netsuite-approval-double-check/assets/dashboard_template.html` | 58-71, 76-88, 127, 132, 164-165, 167-170, 176-178, 460-466, 502-596, 31-32, plus 13 sentence trims |
| `netsuite-approval-review/publish_dashboard.cut.py` | `plugins/netsuite-approval-review/skills/netsuite-approval-double-check/assets/publish_dashboard.py` | 1 sentence trim at line 7 |
| `procore-open-items-review/SKILL.md.cut.md` | `plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md` | 9-12, 18, 23, 25-27, 42, 523-525, plus 11 sentence trims |
| `procore-open-items-review/references/step-8-execute.md` | `plugins/procore-open-items-review/skills/procore-open-items-review/references/step-8-execute.md` | whole file, 22 lines |
| `procore-open-items-review/references/lenses-delivery-design.cut.md` | `plugins/procore-open-items-review/skills/procore-open-items-review/references/lenses-delivery-design.md` | 22 |
| `procore-open-items-review/dashboard_template.cut.html` | `plugins/procore-open-items-review/skills/procore-open-items-review/assets/dashboard_template.html` | 34-35, 58-73, 80-92, 132, 163, 196-197, 199-203, 230-232, 576-582, 622-722, 363-371, plus 11 sentence trims |
| `procore-open-items-review/publish_dashboard.cut.py` | `plugins/procore-open-items-review/skills/procore-open-items-review/assets/publish_dashboard.py` | 253-258, plus 3 sentence trims |
| `_shared/dash-header-mirror.block` | `plugins/_shared/dash-header-mirror.block` | whole file, 29 lines |
| `_shared/dash-band-track.cut.block` | `plugins/_shared/dash-band-track.block` | 1 sentence trim at line 5 |
| `_shared/dash-of-total.cut.block` | `plugins/_shared/dash-of-total.block` | 2-4 |
| `_shared/dash-float-css.cut.block` | `plugins/_shared/dash-float-css.block` | 17 |
| `_shared/dash-render-tail.cut.block` | `plugins/_shared/dash-render-tail.block` | 1-2 |
| `_shared/skill-artifact-host.cut.block` | `plugins/_shared/skill-artifact-host.block` | whole file as it stood, 1 line |
| `_shared/skill-close-down.cut.block` | `plugins/_shared/skill-close-down.block` | whole file as it stood, 4 lines |
| `scripts/shared_blocks.cut.py` | `scripts/shared_blocks.py` | 288-302, 346-391, 552-663, 513-514 |
| `scripts/validate.cut.py` | `scripts/validate.py` | 394, 396 |
| `scripts/test_skill_code.cut.py` | `scripts/test_skill_code.py` | 579-607 |
| `scripts/measure_float.cut.js` | `scripts/measure_float.js` | 174-183 |

A range is the range in the file as that one cut found it. Several cuts on one file shift the
numbering, so read the ranges in the order the retired file lists them.

## Three notes for whoever puts this back

`test_gate_states` is not here. The record's step 8 listed it, and the record was wrong.
That test covers the `__gate` block in Procore Step 2, which filters the queue by
`can_respond` and clicks nothing. It stayed in `scripts/test_skill_code.py`.


The floating header survived. Only its execute mirror went. `floatPaint()` now lives in
`plugins/_shared/dash-band-track.block`, and both templates call it where they once called
`renderBar()`. Reinstating `dash-header-mirror.block` means folding `floatPaint()` back into
it. Otherwise the bar gets painted twice.

Two shared-block checks left with the code they guarded. They are
`check_execute_type_coverage` and `check_execute_prompt_purity`, with `ITEM_TYPE_MANIFEST`,
`PROCEDURE_TOKENS` and `PROMPT_STMT`. They come back into `scripts/shared_blocks.py`. Their
two calls come back into `scripts/validate.py` and into that script's own `main()`.
