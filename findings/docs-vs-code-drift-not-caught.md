---
id: pending
slug: docs-vs-code-drift-not-caught
kind: finding
status: observed
date: 2026-08-24
---
# Docs pointing at removed code go uncaught

**Outcome protected.** Prose that survives its own code's deletion is found, not left to
drift forever.

**Argument.** Removing dead code leaves live prose pointing at it, and nothing catches
that.
`validate.py` checks that the docs mention every plugin.
It never checks that the docs describe behaviour the code still has.
The NetSuite instruction that survived its own bin's deletion was found by
reading docs against code.
The verdict check covers one narrow machine-settleable slice of that.
The rest is still a person reading.

**Evidence.** Found 2026-08-24 by a documentation sweep.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py` covers
the settleable slice. The rest is `none`.
