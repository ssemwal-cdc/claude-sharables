---
id: pending
slug: check-packs-next-phase
kind: decision
status: open
date: 2026-08-26
---
# Check packs, next phase

**Rule.** Write a new check pack from a role document or an interview, never from imagination.

**Outcome protected.** A reviewer who is not a financial analyst gets checks that serve their job.

**Argument.** Each check declares the capability it needs and the lens it belongs to.
`config.focus` selects.
Absent config is exactly today's behaviour, and that is what makes the feature additive.
Phase 1 shipped 2026-08-26 as NS v12 and PC v13.
Phase 1 is the descriptive check registry, gated by `check_check_registry()`.
Phase 2 shipped 2026-08-26 as NS v13 and PC v14.
`focus.lenses` carries hardcoded packs, because invented checks are judgment nobody vetted.
`focus.emphasis` is free text and works with or without a pack.
Emphasis reorders and rewords `head`, `facts` and `detail`.
Emphasis never touches a verdict, a figure, or an Absolute rule.
Two more packs shipped 2026-08-26 as PC v15: `delivery` and `design`.
Both were written from SharePoint role documents, not invented.
No content from those documents is reproduced in this repo or in the skills.

**Silence stays the default.** With no lens chosen, nothing is said about a check that did not run.
A lens the user deliberately picked gets one line at the start of the chat reply.
That line names the lens and what is missing, once per run.
It never appears on an item, a verdict, a warning line or a detail paragraph.
A capability the user chose is informative.
A capability the user was never given is an apology.
Never present a missing capability's function as though it happened.
The dashboard "which packs ran" panel is dropped, and must not be reinstated.

**The leniency doctrine governs every future pack.** Missing data is never a finding.
A purchase order with no receipt rows is a purchase order whose receipts NetSuite never saw.
It is not a delivery that never arrived.
Only a discrepancy where both sides exist may flag.
Billed 50 against receipts of 40 is a finding.
Billed 50 against no receipt data is silence.
Keep three states: `matched`, `absent`, `failed`.
`failed` is never `absent`.
`absent` is never "nothing was received".
Match leniently, because descriptions, units and line splits differ for ordinary reasons.
Prefer an approximate tie to a manufactured mismatch.

**Two constraints on any extension.** Deepening what is read never touches execute authority.
The per-item instruction, the pre-click re-verify and the post-click verify stay as they are.
Do not break for anybody.
Absent config must stay byte-identical.
An errored query is `failed` and never `empty`.
A permission-denied field degrades to "not checked" without aborting.
Step 5e runs the `ShipRcpt` query as a second query.
Never widen Step 2's `linktype = 'OrdBill'` filter to get receipts.
That filter stops the billing sum double-counting.
Deduplicate receipts to distinct ids before summing.

**M365 and Teams are outside this reframe.** More NetSuite is more internal system-of-record data.
Email and Teams are outsider-controlled.
Both skills already rule that record content is data and never instructions.
A vendor asking for an approval would become review context on a system holding approval authority.
A feeder line offering an on-request cross-check is cheap and safe.
A feeder is ephemeral, on request, and adds no prerequisite.
A standing integration needs the injection rule extended past attachments first.
It also needs a never-persist-raw rule.

**Options.**

A. Stop here. Three packs plus emphasis is enough until someone asks for a fourth.

B. Build Phase 3, a fourth pack, from a fresh maintainer or role interview.

C. Probe the NetSuite data first, then decide which pack the data can actually support.

**Recommendation.** C, then B.
A supply-chain check on unpopulated fields ships silence dressed as coverage.
One data probe answers whether `dueDate` and `shipDate` are filled in at Compass.

**Evidence.** Probed live 2026-08-26, not inferred.
`itemreceipt` exists with 565 fields, 225 of them standard.
It carries `createdFrom`, `orderId`, `orderType`, `tranDate`, `item`, `class`, `department`, `location` and `subsidiary`.
A three-way match is therefore constructible today.
`purchaseorder` carries `dueDate`, `shipDate` and `orderStatus` among 616 fields.
Schema existence is not population.
Whether Compass fills those fields is `unmeasured`.
Do not cite lead time as a working check.
The SuiteQL metadata catalog returns 500 on `transactionline` for this tenant.
The error names `custcol_r_it_total_retainage_balance` as not found on `<Transaction>:<TransactionLine>`.
Use `ns_getRecordTypeMetadata` or a probe query for that table instead.
`ns.lead-time` ships as an observation only and is the weakest of the three checks.
A late delivery is never a reason to withhold payment for goods received.
Phase 2 was proven additive: the same log published with and without `config.focus` is byte-identical.
Neither `dashboard_template.html` nor `publish_dashboard.py` was touched for Phase 2.
Phase 1 was purely additive.
PC v15 removed six lines, all of them statements the change made untrue.
`open_items/mine` returns exactly three types: change risks, subcontractor invoices and change order packages.
RFI response, submittal review and drawing issuance are not in that queue.
So the `design` lens covers design-driven change and not design production.
The skill says so in place.
Do not invent RFI or submittal procedures.
Step 1 reports an unrecognised `item_type` with its `title` and `url` instead.
`pc.dsn-unknown-workflow` lists them under a heading naming them as unknown workflows.
That row is never suppressed, never counted as noise, and never reaches the execute list.
`pc.del-schedule-impact` reads `schedule_impact`, which Step 3 fetched and no check had ever read.
A blank schedule-impact field means nobody filled it in.
The 3x overcount this filter rule prevents once turned 136,369.02 into 409,107.06.
D‹silent-connector-absence›, silence for a capability nobody can obtain, is the rule reused here.

**Checks.** `check_check_registry()` in `scripts/shared_blocks.py`, run by `scripts/validate.py`.
