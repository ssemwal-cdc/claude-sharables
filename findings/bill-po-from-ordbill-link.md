---
id: pending
slug: bill-po-from-ordbill-link
kind: finding
status: observed
date: 2026-08-20
---
# Bill PO comes from linkage

**Outcome protected.** No correctly coded bill is flagged as miscoded.

**Argument.**

A bill purchase order comes from the transaction linkage. The typed reference custom field has never been the coding.

The skill flagged bills as coded to the wrong purchase order. The System Information tab did show a purchase order field with the wrong value.

The Related Records panel showed the right one. The teammate was right and the flags were false.

Both records carried a second field that agreed with the linkage and contradicted the flag. Neither was read.

It was systematic, not two records. All four bills from one vendor read one purchase order and all four are applied to another. Three were already approved.

So the headline was phantom. Acting on it meant chasing reversals on correctly posted transactions.

Three compounding defects sat behind it, all now fixed in the cross-check step.

First, a typed reference was read as the coding. The linkage fields and the Related Records panel appeared zero times in the whole repo. The query step already read the right table and never asked it for the link.

Second, contract and billed-to-date were computed off two unjoined keys. The contract came from a document-number string match, and the billed total came from a vendor and memo sum with no purchase order predicate at all.

Third, the zero-evidence was inverted. A first draw and any pending bill both show no billed amount on the purchase order, so that reading is expected, not corroboration.

The history query selected the approval status and no rule ever spent it.

**Evidence.**

- Found by a teammate and confirmed against production 2026-08-20.
- Bill `2325026-07`, internal id 2534437, named `PO11120` and is applied to `PO16093`, whose contract field reads 5,400.
- Bill `182743734-0004`, internal id 2535881, named `PO16033` and is applied to `PO16034`, whose contract field reads 284,078.31.
- The flag headline claimed 182,526.82 dollars cumulative on the wrong purchase order. That is the correct commitment at 64% of its 284,078.31 contract.
- The second flag claimed 130% of contract and 478,012.50 dollars billed on `PO11120`. The two bills actually applied to it total exactly its 372,500 contract.
- The teammate two independent sources disagreeing is what settled it, the same device that made the change order recipe trustworthy.

**Checks.** `scripts/test_skill_code.py` runs the code the cross-check step carries.
