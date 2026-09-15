---
id: F17
slug: attachment-sniff-six-outcomes
kind: finding
status: observed
date: 2026-08-14
---
# Six attachment outcomes

**Outcome protected.** A workbook and an image are read instead of reported unreadable.

**Argument.**

Both skills read every attachment as a PDF, and everything else fell into the wrong bucket.

PDFs reviewed fine. Excel and image support came back unreviewed.

It was not a limitation. It was one missing type check, and the misfiling is what hid it.

Neither skill sniffed the bytes. The pdf.js loader throws an invalid-PDF error on a workbook, which is the same error a corrupt download gives.

Both skills then read that error through a two-state rule with no room for it. The Procore rule folded a non-PDF into the expired case, a clause written for expired-signature XML that a spreadsheet also satisfies.

So Excel support was re-fetched, failed identically, and landed as skipped, sometimes described as a scanned image. The retry had no exit and no type check.

The NetSuite rule was blunter. It said non-PDF attachments are unusual, handle them the same way and note the type. That is an instruction to feed a workbook to pdf.js, resting on a frequency assumption that was simply wrong.

Six outcomes are now kept distinct. They are text, spreadsheet, image, scanned, expired and unsupported.

The scanned outcome is the narrow one. The bytes were a PDF, it parsed, and it yielded almost nothing.

Anything that threw is named by what the bytes were.

**Evidence.**

- Reported from production 2026-08-14.
- This is the same bug class as the change order id and the fan-out states. See D41, three states never a boolean.
- The table was later reported working. See F46, the sniff table is reported working.

**Checks.** `scripts/test_skill_code.py` runs the code the attachment step carries.
