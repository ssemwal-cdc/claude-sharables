---
id: pending
slug: mandate-gaps-closed
kind: finding
status: observed
date: 2026-09-16
---
# Three mandate gaps closed

**Outcome protected.** Three mandate rules run as a command, not a memory.

**Argument.**

`D82`, hooks and checks pass, turns prose rules into checks. This finding closes
three more: no waiter loop, every screen measured, and no numbered record on a
branch.

`check_waiter_loops()` reads `CLAUDE.md`, the three `README.md` files, every
record, both `SKILL.md` files and every shared block. It fails on an unbounded
wait-and-retry sentence.

`check_device_shots()` reads `.claude/shots/summary.txt`. It fails on any
capture overflow, or on fewer than 18 rows. A new `shots` CI job runs the
capture and this check together. `D81`, device usability check, names the check.

`check_no_pending_on_main()` fails a build on `main` that still carries
`id: pending`. `check_claim_dry_run()` fails when a slug citation would stay
unresolved after claiming. `--check-claim` runs the same check by hand.

**Evidence.** Measured 2026-09-16, on this branch, each with a `.bak` copy as the undo.

- `check_waiter_loops()`: inserted one unbounded wait-and-retry sentence into a record.
- The check went red. It named the file, the line and the sentence.
- Restored the record. The check went green.
- `check_device_shots()`: edited one capture's overflow to 12 in `summary.txt`.
- The check went red. It named the file and the overflow count.
- Restored the file. The check went green with 18 rows and zero overflow.
- `check_no_pending_on_main()`: set one record's id to `pending`, with `GITHUB_REF=refs/heads/main`.
- The check went red. It named the record and the claim command.
- Restored the id. The same run went green.
- Off `main`, the same pending record was a note, not a failure.
- `check_claim_dry_run()`: added a slug citation naming no pending record.
- The check went red. It named the file, the line and the slug.
- Restored the file. The check went green.
- Playwright 1.56.1 captured 18 files in `.claude/shots`, with zero overflow.

**Checks.** `python3 scripts/validate.py`. `GITHUB_REF=refs/heads/main python3 scripts/validate.py`
for the pending-on-main case.
