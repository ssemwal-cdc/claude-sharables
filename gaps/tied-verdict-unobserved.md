---
id: pending
slug: tied-verdict-unobserved
kind: gap
status: unobserved
date: 2026-09-23
---
# Tied verdict unobserved live

**Outcome protected.** A `tied` row on the dashboard is never cited as proven until a real run produced it.

**Argument.** The `tied` verdict is new.
It is unit-tested and mutation-tested against fixtures only.
No live Procore run has ever produced one.

To clear it: run a full review against a live queue.
Find an item where every core check ran and agreed, and exactly one field is blank in Procore.
Confirm it lands as `tied`, not `skipped`.
Its `supportRead` must name the file actually read.
The reviewer must confirm the blank field really is blank in Procore, not misread.

This gap sits inside G4, no end-to-end run.

**Evidence.** This claim is guessed, not proven.
It is tested against mocks or fixtures only.
Nobody has watched a `tied` row against a live queue.
Do not cite it as established.
`python3 scripts/test_skill_code.py` covers the demotions and the widget fold against mocks.
It cannot cover this gap, because this gap is about a real system.

**Checks.** `scripts/test_skill_code.py`, the tied-verdict cases, mocks only.
