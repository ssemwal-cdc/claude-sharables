---
id: F71
slug: phantom-po-miscoding-flag-was-wrong
kind: finding
status: observed
date: 2026-08-20
---
# Bill PO comes from linkage

**Outcome protected.** No correctly coded bill is flagged as miscoded.

**Argument.** A bill purchase order comes from the transaction linkage.
The typed reference custom field has never been the coding.

The skill flagged bills as coded to the wrong purchase order.
The System Information tab did show a purchase order field with the wrong
value.
The Related Records panel showed the right one.
The teammate was right, and the flags were false.

Both records carried a second field that agreed with the linkage and
contradicted the flag.
Neither was read.

It was systematic, not two records.
All four bills from one vendor read one purchase order and all four are
applied to another.
Three were already approved.
So the headline was phantom.
Acting on it meant chasing reversals on correctly posted transactions.

**Evidence.** Found by a teammate and confirmed against production 2026-08-20.
Bill `2325026-07`, internal id 2534437, named `PO11120` and is applied to
`PO16093`, whose contract field reads 5,400.
Bill `182743734-0004`, internal id 2535881, named `PO16033` and is applied to
`PO16034`, whose contract field reads 284,078.31.
The flag headline claimed 182,526.82 dollars cumulative on the wrong purchase
order.
That is the correct commitment at 64% of its 284,078.31 contract.
The second flag claimed 130% of contract and 478,012.50 dollars billed on
`PO11120`.
The two bills actually applied to it total exactly its 372,500 contract.
Two independent sources disagreeing is what settled it, the same device that
made the change order recipe trustworthy.

**Checks.** `scripts/test_skill_code.py` runs the code the cross-check step
carries.
