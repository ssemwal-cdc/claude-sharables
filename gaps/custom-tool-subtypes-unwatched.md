---
id: pending
slug: custom-tool-subtypes-unwatched
kind: gap
status: unobserved
date: 2026-09-01
---
# Custom tool subtypes unwatched

**Outcome protected.** A check reads the right field on the right custom tool.

**Argument.** Both the subtype reconciliation and the compact render shipped as PC v26 and NS v24.
Neither has been watched.
Both came out of one Procore run's report.

**What is observed.** Two custom tools appeared in one queue.
They are Internal Change Risk and Customer Change Request.
The second was 37 of 62 items.
The report named the tool ids and the queue's `item_subtype` as the discriminator.
`custom_field_522888` on the second tool is Duration in Weeks, not money.
That tool's two cost fields were blank on all 37 items.
The file sizes were reproduced here against a fixture.

**What is not observed.**

- **The reconciliation has never run.** Step 1 subtracts the config's keys from the queue's subtypes.
  Setting up a new tool mid-run and naming it in the run report is designed and fixture-tested.
  No run has done it.
- **The second tool's cost field names.** `ROM Cost` and `Approved Customer Cost` are names off a
  rendered record, mapped by label by that run.
  They are almost certainly right and are not confirmed against a payload.
  They were blank on every item seen, so no ICR check has ever tied on that tool.
  A `clear` verdict on a Customer Change Request has never been produced by anything.
- **Nothing has rendered at 161 KB.** The compact serialiser makes the file readable in one read.
  That read is the wall the run actually hit.
  Whether `show_widget` accepts 161 KB inline is still unknown.
  99 KB and 43 items remains the largest render anyone has observed.
  The integrity banner settles it, and it has never fired.
- **The dehydrated-file write path.** `EINVAL` on every pre-existing file is one report from one mount.
  Rename-over succeeding is from the same report.
  Step 0's property-shaped rule accommodates it.
  Nobody has watched a run take that route with the rule in place.
- **The conflict-copy rule.** A machine-suffixed state file with newer `config` happened once.
  It was merged by hand.
  The rule written for it has never been exercised.
  That rule is canonical for `items` and `actions`, adopt only missing `config` keys, and say so.
- **`python3 -B`.** Trivially correct, never run in anger.

**What is now a failed build rather than a silent miss.** An unmapped subtype cannot take another
tool's tool id, and cannot keep a `clear` verdict.
A large render cannot run past one file read on either axis.
Neither gate says whether the field mapping is right, which is the part above a gate cannot reach.

**Evidence.** Evidence class: a maintainer's report of a run, not a transcript.
Reported 2026-09-01: 62 items across two custom tools, 37 of them the second tool.
Reproduced against a fixture: 174 KB, 2,834 lines, 55,118 bytes of template before data.
The run reported 164 KB, 62 items and 55 KB of template.
`test_custom_tool_subtype` pins both halves of the fail-closed.
`test_render_fits_one_read` pins both axes and is mutation-tested.
Restoring `indent=1` fails the build at 3,013 lines.
`show_widget` acceptance at 161 KB is `unmeasured`.

**Checks.** `test_custom_tool_subtype` and `test_render_fits_one_read` in `scripts/test_skill_code.py`.
