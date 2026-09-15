---
id: pending
slug: no-end-to-end-run
kind: gap
status: unobserved
date: 2026-08-15
---
# No end-to-end run

**Outcome protected.** A reviewer's verdicts come from a path somebody has watched work.

**Argument.** This is the single biggest gap.
No full review has been watched from queue to execute on either plugin.
Every change from 2026-08-13 and 2026-08-14 rests on mocks.
Those changes are in-page pdf.js extraction, the fan-out gate and the bulk `transactionline` query.
They also include the size-budgeted page reads and the attribution note.
The one live test was pdf.js in a chat on bill 2532506.

To clear it: run a full review on each plugin.
Then execute against one low-value item.
Compare the verdicts against a previous run's verdicts.
Expect the same figures and the same clear or flagged calls.
Treat any difference as a regression until it is explained.

**Partially observed, Procore.** A live run gated two previously `ungated` Align change orders.
They gated as actionable at Financial Analyst Review with Approve and Revise and Resubmit.
The gate ran through the `CommitmentChangeOrder` join.
That is the first real-data confirmation of the CCO recipe.
It also confirms the step-not-subject verb pairing.
The ids came from `wfId` values already recorded in the log.
So the `line_items[].holder.id` read is still unobserved.
Execute mode has still not been walked.

**Partially observed, NetSuite.** One approval completed live on record 2534442.
It executed by navigating the Approve button's own URL after the button no-opped five times.
That confirms the URL recovery in Step 8.6 and not the ordinary path.
Approve With Notes remains unwalked, so no approval has gone through the primary route with a note.
The same run surfaced the Step 0 mount gap.
Its dashboard was therefore rendered from workspace copies synced a day earlier.
The gate results stand, because the gate runs from `SKILL.md`, which ships with the plugin.

**Evidence.** This claim is guessed, not proven.
It is tested against mocks or fixtures and shipped.
Nobody has watched a full run on real data.
Do not cite it as established.
`python3 scripts/test_skill_code.py` covers the logic against mocks.
It cannot cover this gap, because this gap is about a real system.
Partial observations dated 2026-08-15, Procore and NetSuite.
Record 2534442, NetSuite, one live approval by URL.
Bill 2532506, one live pdf.js test.
G‹netsuite-notes-page›, the notes page nobody has seen, blocks the primary NetSuite route.

**Checks.** `scripts/test_skill_code.py`, mocks only.
