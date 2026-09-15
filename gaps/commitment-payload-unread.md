---
id: pending
slug: commitment-payload-unread
kind: gap
status: unobserved
date: 2026-08-28
---
# Commitment payload half unread

**Outcome protected.** A commitment's figures come from fields the payload really has.

**Argument.** The queue has a fourth type, the commitment, shipped as PC v24.
A maintainer's run hit a purchase order contract with a live responder at Financial Analyst Review.
It was due that day.
Step 1's unknown-type rule handed over a link with no buttons.

**Why the type had not been built.** `open_items/mine` had returned exactly three types in every
recorded observation, so a fourth was hypothetical.
The unknown-type rule was written two days earlier, deliberately.
The design lens weighed surface the link against invent a procedure, and the link won.
The rule was written with RFIs and submittals in mind, which are out of this skill's domain.
A commitment is not out of domain.
It is the document the invoice and CCO checks already tie back to.
The rule was right and its scope was wrong.
So the fix is a fourth procedure, not a change to the rule.

**What is observed is exactly one thing.** The run reported the step name, the due date and a live
responder for that row.
Those can only have come from a workflow instance.
So the Step 2 fan-out sent the queue's `item_type` verbatim and the endpoint accepted it.

**The payload is now observed for half the type.** Step 3's field names were borrowed from the
`change_order_packages` read that shares the collection.
They shipped as an explicit guess with an instruction to report the payload's keys back.
Against a real purchase order contract, `grand_total`, `line_items` and `retainage_percent` held.
The counterparty's display string is `vendor.company`, not `vendor.name`.
Borrowing names from the sibling endpoint is the right method and is not guessing.
Three of four held because they came from a payload in the same collection.
Keep using the family as the source.
Keep labelling a borrowed name unconfirmed.
One name in four was wrong, and it was the one no check runs on, so nothing would have failed loudly.
`WorkOrderContract` is still unread.
Step 3 narrows the report-the-keys instruction to that collection rather than dropping it.
Same tool, separate collection, very likely identical.
That reasoning is exactly what produced `vendor.name`.

**One design decision looks like over-caution and is not.** `com` covers two collections.
`publish_dashboard.py` demotes a commitment with no `wfType` to `ungated`.
It does not default to `PurchaseOrderContract`.
Both strings are valid workflowable types.
So the wrong one carrying the right id returns 200 with zero rows, not a 400.
Step 8 reads an empty instance as already actioned elsewhere.
That would log a live contract as done with no click.

**What was deliberately not written.** Five mechanical checks shipped.
They are the SOV footing, the total appearing in the support, line integrity, retainage and queue context.
Nothing commercial shipped.
Whether the scope, the rate or the counterparty are right is the reviewer's judgement.
A commitment out for approval is the baseline the other three types are checked against.
A substantive FA checklist comes from asking the maintainer, never from inventing one.

**Evidence.** Evidence class: a maintainer's report of a run, not a transcript.
That is weaker than the CCO gate's record ids and dates.
Dates: the run 2026-08-28, the payload read 2026-08-28.
`developers.procore.com` is blocked by the sandbox egress proxy, so the primary source was unreadable.
`WorkOrderContract` is unread. `unmeasured`.
`test_commitment_kind` pins the demotion and is mutation-tested.
Removing the guard fails three assertions.

**Checks.** `test_commitment_kind` in `scripts/test_skill_code.py`.
