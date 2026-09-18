---
id: F111
slug: netsuite-co-buttons-are-the-gate
kind: finding
status: settled
date: 2026-08-24
---
# NetSuite change orders gate on their buttons

**Outcome protected.** A whole batch is never logged as actioned on a role mistake.

**Argument.** A maintainer answer changed the audit's own work mid-pass.
NetSuite change orders should be executable, so they now have a real bracket
instead of a documented gap.
Their records carry no `approvalstatus` and no next approver.
Their approval buttons render only while the item is pending and still
assigned to the signed-in approver.
So on that record type, the buttons are the gate.

Step 8 reads the page before the click and re-reads it after.
That reorders the buttons-absent diagnosis.
Already-actioned is now the first hypothesis for a single item.
The browser-role theory is reserved for when every item in the batch shows no
buttons.
The old ordering would have logged a whole batch as actioned on a role
mistake.

**Evidence.** Pass dated 2026-08-24, immediately after the audit.

**Checks.** `scripts/test_skill_code.py` in CI.
