---
id: F18
slug: cco-holder-id-route
kind: finding
status: observed
date: 2026-08-14
---
# CCO workflow hangs off holder.id

**Outcome protected.** A commitment change order gets response buttons instead of a dead gate.

**Argument.**

Step 2 used to say that `ChangeOrderPackage` returns a 400 and that those items cannot be gated. So every CCO rendered as `ungated` with no response buttons.

The 400 is real. It is also real on every other package-style type string and on `CommitmentContractChangeOrder`.

What made it look unsolvable is where the error points. It names a company-level `workflows/tools` endpoint that an ordinary account gets a 403 on, which reads as a permissions wall. It is not one.

The workflow is simply not attached to that object. Query `workflowable_object_type=CommitmentChangeOrder` with the commitment change order id and the instance returns immediately.

That id is not the package id. It is `line_items[].holder.id` on the package payload.

The `fetch(packageUrl, {redirect:'follow'})` trick is gone deliberately. A client-side route resolution returns the URL you sent, which is the package id, the wrong id. `holder.id` gets the same saving with none of that hedge. Do not reintroduce it.

The independent check is the UI, and it is worth keeping because the failure mode is silent. An actionable item renders a live Respond button naming the user against the current step role.

Two independent sources agreeing is what makes the recipe trustworthy. The gate alone cannot detect its own miss.

**Evidence.**

- Found by a teammate running the plugin 2026-08-13. Confirmed 2026-08-14 against 5 packages. All 5 then gated as actionable at Financial Analyst Review.
- Observed on CE #019. Respond shown, user named as Financial Analyst, gate returning `can_respond` true.
- A package can span several commitment change orders, because `holder` is per line. See D22, several holders stay ungated.
- The read must precede the gate for CCOs. See D23, read before gate for CCOs.

**Checks.** `test_skill_code.py` pins the ungated demotion in D30, demote a missing wfId.
