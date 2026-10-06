---
id: D98
slug: claim-through-the-stamp
kind: decision
status: settled
date: 2026-10-06
---
# Claim record ids through the stamp

**Rule.** A branch writes `id: pending`. `merge <pr> --confirm` claims the numbers through the stamp (`.github/stamp.json`) before the merge. This repo keeps no claim command of its own.

**Outcome protected.** A record id stays permanent and unique. No one numbers a record by hand.

**Argument.**

The stamp from claude-settings claims the same ids and rewrites the same citations as the old claim command. It was measured on a fixture with six pending records, three kinds and a retired id.

One claim in one place serves every repo that adopts the stamp. A second claim here would drift from it.

The CI `records` job refuses a number a branch adds without a `Record-claim` trailer, and any pending record on main.

`check_no_pending_on_main` and `check_claim_dry_run` stay in `scripts/check_records.py`. `validate.py` runs them locally, without node or a base ref.

**Evidence.**

- The owner ruled it on 2026-10-06, in the claude-settings deferred record `sharables-adopts-the-stamp`.
- Every main merge since PR #21 is a merge commit. Main has no branch protection. The slowest job takes about 2 minutes.
- `scripts/test_check_records.py` is removed. The stamp's own tests (`test_stamp.mjs`, claude-settings) now cover claim behaviour.

**Checks.** The `records` job in `.github/workflows/validate.yml`, and `check_no_pending_on_main` in `scripts/check_records.py`.
