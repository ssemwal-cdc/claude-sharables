---
id: pending
slug: audit-list-worked
kind: finding
status: settled
date: 2026-08-24
---
# Working the audit list

**Outcome protected.** An audit finding ends as a check or a stated reason, never as a note.

**Argument.** 38 audit items needed no decision.
This record says what happened to them and what is left.

**Two maintainer answers changed the work mid-pass.**
NetSuite change orders should be executable, so they have a real bracket instead of a documented gap.
Their records carry no `approvalstatus` and no next approver.
Their approval buttons render only while the item is pending and still assigned to the signed-in approver.
So on that record type the buttons are the gate.
Step 8 reads the page before the click and re-reads it after.
That reorders the buttons-absent diagnosis.
Already-actioned is now the first hypothesis for a single item.
The browser-role theory is reserved for when every item in the batch shows no buttons.
The old ordering would have logged a whole batch as actioned on a role mistake.

**The shipped examples are sanitised.** Every live value a teammate could copy is a placeholder now.
Those were a company id, a tool id, three custom-field ids and a named subcontractor.
They also included a project label, a commitment balance, and real bill and purchase order numbers.
`README.md` no longer claims the plugins carry no customer data while carrying some.
Defect provenance is deliberately exempt and stays.
A flagged bill cited by id is the evidence that a documented bug was real.
This repo's epistemics rest on findings being traceable to a record and a date.
The rule now states that distinction instead of banning both cases and doing neither.

**Three fixes were to things the same session had just built.**
Procore's dashboard still filtered on `verdict !== "gone"` after the bin was removed.
That filter can exclude nothing, and the prose certified the filter deleted.
The reachability check missed it because its regex matched only `==` and `===`.
It is widened to catch the inequality form.
`check_template_versions()` read only the first version mention per file.
The verdict allowlist caught a wrong verdict but not a missing one.

**The shared-block loop is now demonstrated rather than argued.**
A wording fix belonging to `pub-render-archive` was made in `plugins/_shared/`.
`--check` failed both plugins for being out of step.
`--sync` pushed the fix into both, and the build went green.
That is the loop working in anger for the first time.
It had been listed as unestablished.

**Newly enforced, where a claim used to stand in for a check.**
`test_skill_code.py` now runs in CI, which it never did while `README.md` said it would.
`check_onboarding_page()` checks four properties that were asserted as tested and read by no file.
`check_execute_prompt_purity()` keeps procedure out of the authorising message.
An unrecognised Procore response verb now fails conservatively on both axes.
It requires a reason, and it counts as affirmative for the no-support caution.
It previously answered false to both.

**Not done, and why.** The 2026-08-20 dashboard fixtures were not committed.
The measurements behind them were never reproducible.
The honest fix was to withdraw the certification rather than fabricate fixtures after the fact.
The `zip` against `xl/` sniff distinction is documented as a rule rather than implemented.
The sniff reads four bytes and cannot see inside the container.
SheetJS yielding no sheets is the real signal, and that is what the rule says.

**Evidence.** Pass dated 2026-08-24, immediately after the audit.
F‹nine-agent-prose-audit›, 122 findings and 29 surviving, is the audit this worked through.
G‹dashboard-widget-host-unseen›, the uncommitted 2026-08-20 fixtures, carries the withdrawn certification.
D‹shared-blocks›, canonical copy plus a check, is the loop demonstrated here.

**Checks.** `scripts/validate.py`, `scripts/test_skill_code.py` in CI, `scripts/shared_blocks.py`.
