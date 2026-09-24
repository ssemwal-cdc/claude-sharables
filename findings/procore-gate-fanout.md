---
id: F164
slug: procore-gate-fanout
kind: finding
status: observed
date: 2026-09-24
---
# Procore gate fan-out confirmed solid

**Outcome protected.** A live item is never logged as done because one request failed.

**Argument.** The three-state rule is mock-tested and mutation-tested.
Concurrency is capped at 8 to 10, because a 429 is a `failed` and not an `empty`.
Actionable plus suppressed plus failed must equal the queue length on every run.
A `failed` item must never be folded into the suppressed count.

**Evidence.** Reported 2026-09-24 by the maintainer: the fan-out counts hold on real runs.
The report does not say a 429 was ever seen.
Whether the 429 branch itself fired live stays `unmeasured`.
`python3 scripts/test_skill_code.py` covers the three-state fan-out against mocks.
It is mutation-tested: collapsing a 429 into `empty` fails the build.

**Checks.** `scripts/test_skill_code.py`, the three-state fan-out test.
