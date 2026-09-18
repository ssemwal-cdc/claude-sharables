---
id: F145
slug: pending-id-checks-gate-main-and-citations
kind: finding
status: observed
date: 2026-09-16
---
# Pending-id checks gate main and citations

**Outcome protected.** No numbered record is claimed on a branch, and no citation stays
unresolved after claiming.

**Argument.** `D82`, hooks and checks pass, turns prose rules into checks.
This closes one more: no numbered record on a branch.

`check_no_pending_on_main()` fails a build on `main` that still carries
`id: pending`.
`check_claim_dry_run()` fails when a slug citation would stay unresolved after
claiming.
`--check-claim` runs the same check by hand.

**Evidence.** Measured 2026-09-16, on this branch, with a `.bak` copy as the
undo.
Set one record's id to `pending`, with `GITHUB_REF=refs/heads/main`.
The check went red, and named the record and the claim command.
Restored the id.
The same run went green.
Off `main`, the same pending record was a note, not a failure.
Added a slug citation naming no pending record.
The check went red, and named the file, the line and the slug.
Restored the file.
The check went green.

**Checks.** `python3 scripts/validate.py`.
`GITHUB_REF=refs/heads/main python3 scripts/validate.py` for the
pending-on-main case.
