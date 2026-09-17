# The `supply-chain` lens

Read this file only when `config.focus.lenses` names `supply-chain`. It is Step 5's
5e-5g, moved out of the spine because most runs never select this lens.

- **Skip this whole file unless the lens is selected.** Absent it, Step 5 ends at 5d.
- **Read this first, because it governs all three checks.** Not all of what supply chain deals with lives in NetSuite. A PO with no receipt rows is overwhelmingly a PO whose receipts NetSuite never saw, not a delivery that never arrived. So these checks are lenient by design.

- **Missing data is never a finding.** No receipt rows, no PO lines, an unpopulated date: report nothing, or report it as context. It never flags an item and never skips one.
- **Only a real discrepancy, where both sides are present, can flag.** Billed 50 against receipts totalling 40 is a finding. Billed 50 against no receipt data at all is silence.
- **Three states, never a boolean.** `matched` means both sides present and compared. `absent` means the query succeeded and NetSuite holds no such rows. `failed` means the query errored. **`failed` is never `absent`**, and `absent` is never "nothing was received".
- **Match leniently.** Descriptions, units and line splits differ between a PO, a receipt and an invoice for ordinary reasons. Tie on item and quantity where you can, tolerate a reworded description, and prefer an approximate tie to a mismatch manufactured out of formatting. The lens adds evidence when NetSuite happens to hold it. It must never stop someone working the queue.

- **5e. Receipt against billed quantity.** Step 2's link query discards `ShipRcpt` rows, which is correct for summing billings. With this lens on, run the same query a second time for `linktype = 'ShipRcpt'` rather than widening the first. The billing sum must keep its own filter untouched.
- **Deduplicate to distinct receipt ids before summing anything.** The link table carries one row per line pair, so a three-line receipt returns three rows. Same trap as the billing side. Compare receipt quantities to the bill's `tl.quantity` from Step 2. Report the position, such as *"PO receipts total 40 of the 50 units billed"*. Flag only a genuine over-bill against receipts that exist. Under-receipt on a partial delivery is context, not a finding.

- **5f. PO line price against billed rate.** Pull that PO's lines with the same `transactionline` shape used in Step 2 and compare `rate` against the bill's. Report a material difference with both figures. Immaterial rounding, a unit-of-measure difference, or a line that cannot be matched confidently is not a finding. Say what tied and leave the rest alone.
- **5g. Lead time, as an observation only.** Where the PO carries `dueDate` and a receipt carries `tranDate`, the gap between them is worth stating. **Never a flag on its own.** A late delivery is not a reason to withhold payment for goods received.
- **These fields are confirmed to exist and are not confirmed to be populated.** Probed 2026-08-26: `purchaseorder` carries `dueDate` and `shipDate`. Whether Compass fills them in is `unmeasured`. An empty date is the `absent` state. Say nothing and move on.
