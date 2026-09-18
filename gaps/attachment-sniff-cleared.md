---
id: G6
slug: attachment-sniff-cleared
kind: gap
status: unobserved
date: 2026-08-20
---
# Two branches in the attachment sniff stay unfired

**Outcome protected.** A workbook or an image is read, not filed as unreadable.

**Argument.** `F67`, vendor workbooks and
images read outside mocks, closed the workbook and image branches. Two
branches are still unfired. Do not read them as covered.
The first is `scanned`, then rasterise, then look.
That is a PDF which parses but yields almost nothing.
It is distinct from an image attachment, which Chrome displays directly.
The second is the OCR fallback.
With it, the rule that an OCR-derived figure never produces a `clear` verdict is untested.

**The regression to watch for is a skip whose reason is vague.** The bug this replaced said
"support present but unreadable".
That reads the same for a scan, a workbook and a link that timed out.
Whole formats went unread for weeks with nothing in the log to show it.
A skip that cannot name which of the six outcomes caused it is that bug returning.

**Evidence.** The `scanned` branch and the OCR cap remain guessed, not proven.
Nobody has watched either on real data. `unmeasured`.
Do not cite either as established.
The six outcomes kept distinct are `text`, `spreadsheet`, `image`, `scanned`, `expired` and `unsupported`.

**Checks.** `scripts/test_skill_code.py`, mocks only for the sniff table.
