---
id: pending
slug: netsuite-no-slim-build
kind: finding
status: observed
date: 2026-08-24
---
# NetSuite cannot fold rows

**Outcome protected.** Nobody adds a feature to NetSuite that would copy a file byte for byte.

**Argument.**

The NetSuite verdict vocabulary is exactly `clear` and `flagged`. That is precisely the actionable set of the slim build, and the fold branch is the other case.

So nothing would ever fold. The output would be a byte-for-byte copy of the full page, every run.

NetSuite has no `skipped` concept by design. A missing attachment flags an item rather than skipping it.

It could not be a shared block even if it were wanted, because the folded keep-list is per-domain.

Do not add it for symmetry.

**Evidence.**

- Recorded 2026-08-24. The Procore keep-list names project, due, project id, contract id, kind, workflow and key fields against the NetSuite transaction date.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py` pins the NetSuite vocabulary.
