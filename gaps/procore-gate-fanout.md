---
id: pending
slug: procore-gate-fanout
kind: gap
status: unobserved
date: 2026-08-24
---
# Procore gate fan-out untried live

**Outcome protected.** A live item is never logged as done because one request failed.

**Argument.** The three-state rule is mock-tested and mutation-tested.
It has never issued 70 or more concurrent requests at the live Procore API.
A request that fails and returns nothing looks like an item with no workflow instance.
Both skills read no instance as already actioned elsewhere, and skip it.
So a blip can suppress live items quietly and plurally.

To clear it: on the first real run, check the reported counts add up.
Actionable plus suppressed plus failed must equal the queue length.
Every `failed` item must be named.
A `failed` item must never be folded into the suppressed count.

**Evidence.** This claim is guessed, not proven.
It is tested against mocks or fixtures and shipped.
Nobody has watched the fan-out against live Procore.
Do not cite it as established.
`python3 scripts/test_skill_code.py` covers the three-state fan-out against mocks.
It is mutation-tested: collapsing a 429 into `empty` fails the build.
It cannot cover this gap, because this gap is about a real system.
The old sequential gate issued one GET per item across a queue of about 73 items.
About 41 of those requests only learned the item was noise.
Concurrency is capped at 8 to 10, because a 429 is a `failed` and not an `empty`.
G‹no-end-to-end-run›, no watched run, is the wider gap this sits inside.

**Checks.** `scripts/test_skill_code.py`, the three-state fan-out test.
