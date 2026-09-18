---
id: pending
slug: citation-regex-was-blind-once
kind: finding
status: settled
date: 2026-09-15
---
# The slug-citation check was blind once

**Outcome protected.** A slug citation that names no pending record fails the build, and
did not always.

**Argument.** The slug-citation mutation row was blind on the first run, one of
several mutation checks over `scripts/check_records.py`.
The pattern asked for a word boundary after the closing guillemet, which never
comes.
So a slug citation matched nothing and passed.
The fix landed before the check was trusted.

**Evidence.** Measured on 2026-09-15, on this branch over `3a63144`, as part of
mutation-testing `check_citations`.
See `F‹check-mutations-all-caught-defect›`, every check's mutation, for the
full table.

**Checks.** `python3 scripts/validate.py`, which calls `check_citations`.
