---
id: F120
slug: six-one-sided-dashboard-defects
kind: finding
status: settled
date: 2026-08-24
---
# Six defects from one-sided drift

**Outcome protected.** A fix that reaches one plugin reaches the other one.

**Argument.** An audit compared the two plugins' assets against each other.
A question about making them more modular prompted it.
The finding worth keeping is the shape, not any single bug.
Every one of these is a case where one copy learned something and the other
never did.

Six defects were fixed in one commit, on the NetSuite side unless noted.

1. Browser mode could not publish, so a complete review died at Step 7.
2. There was no verdict allowlist, so a typo'd verdict fell through the pill
   logic to "Clear". That is fail-open on the field that decides what gets
   approved. Procore has aborted on this since it shipped.
3. `var live=null` was never assigned, so about 45 lines were unreachable.
   Those lines held the gone and changed states, `newRow`, the bin and a
   permanently zero card.
4. Marks were never pruned, so a mark for an approved bill stayed in
   `ns_marks_v1` forever. It would reappear if NetSuite reused the id. Procore
   sweeps them.
5. The money card had no rollover, so a 2.7m dollar queue rendered as
   `$2702k`.
6. The abort message named `_review_log.json`, the pre-migration name, in both
   copies. So the rename fix reached neither string.

Defect 1 and an unused-config-keys defect share one root cause, an over-broad
`required` list.
That is why this is six defects and not seven.
`me` and `tool` were injected and read by the page and never used.
Only `account` is used.

**Evidence.** Audit dated 2026-08-24.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py` covers
defect 2.
