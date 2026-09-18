---
id: pending
slug: attachment-sniff-workbooks-images-read
kind: finding
status: observed
date: 2026-08-20
---
# Vendor workbooks and images read outside mocks

**Outcome protected.** A workbook or an image is read, not filed as unreadable.

**Argument.** Real vendor workbooks are read.
Real images are looked at.
Both paths have been exercised outside the mocks.
This clears two of the six attachment outcomes.
The two plugin READMEs are therefore accurate on reading spreadsheets sheet by sheet.
They are accurate on looking at images rather than extracting them.
`G6`, two branches still unfired, tracks what this finding does not cover.

**Evidence.** Evidence class: a user report, not a session transcript.
Reported working on real support 2026-08-20 by the person running the plugins.
That is weaker than the CCO gate's record ids and dates.
It is stronger than a mock.
Nobody has posted the figures a workbook produced.
So "that workbook's numbers reached the tie-out correctly" is assumed, not shown. `unmeasured`.

**Checks.** `scripts/test_skill_code.py`, mocks only for the sniff table.
