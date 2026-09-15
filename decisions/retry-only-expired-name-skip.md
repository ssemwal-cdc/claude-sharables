---
id: pending
slug: retry-only-expired-name-skip
kind: decision
status: settled
date: 2026-08-14
---
# Retry only an expired link

**Rule.** Retry an expired link at most twice. Name the outcome that caused every skip.

**Outcome protected.** A format that cannot parse is not retried forever, and no skip hides a whole file format.

**Argument.**

A retry is legitimate for an expired link only, and it is bounded at two.

A file that parsed as the wrong type will parse as the wrong type again.

A skip must name which of the six outcomes caused it.

The word unreadable is what hid the format defect. It reads identically whether the file was a scan, a workbook or a link that timed out.

So entire formats went unread with nothing in the log to show it.

**Evidence.**

- Recorded 2026-08-14 from F‹attachment-sniff-six-outcomes›, six attachment outcomes.

**Checks.** `scripts/test_skill_code.py` runs the attachment code.
