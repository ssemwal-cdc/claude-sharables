---
id: G6
slug: attachment-sniff-cleared
kind: gap
status: observed
date: 2026-08-20
---
# Attachment sniff, cleared partly

**Outcome protected.** A workbook or an image is read, not filed as unreadable.

**Argument.** Real vendor workbooks are read.
Real images are looked at.
Both paths have been exercised outside the mocks.
This item leaves the unverified list for those two formats.
The two plugin READMEs are therefore accurate on reading spreadsheets sheet by sheet.
They are accurate on looking at images rather than extracting them.

**Two branches are still unfired.** Do not read them as covered.
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

**Evidence.** Evidence class: a user report, not a session transcript.
Reported working on real support 2026-08-20 by the person running the plugins.
That is weaker than the CCO gate's record ids and dates.
It is stronger than a mock.
Nobody has posted the figures a workbook produced.
So "that workbook's numbers reached the tie-out correctly" is assumed, not shown. `unmeasured`.
The `scanned` branch and the OCR cap remain guessed, not proven.
Nobody has watched either on real data.
Do not cite either as established.
The six outcomes kept distinct are `text`, `spreadsheet`, `image`, `scanned`, `expired` and `unsupported`.

**Checks.** `scripts/test_skill_code.py`, mocks only for the sniff table.
