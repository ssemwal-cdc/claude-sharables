---
id: pending
slug: hook-proved-with-15-payloads
kind: finding
status: observed
date: 2026-09-15
---
# The shared-tree hook was proved on 15 payloads

**Outcome protected.** A forbidden shared-tree command exits 2 before it runs, and a safe
one does not.

**Argument.** The Bash hook was proved with 15 sample payloads on stdin.
Each forbidden form exited 2 with one line on stderr.
The forbidden forms are the stash, the reset and the restore. They also
include a checkout naming a path, a pattern kill and a pid list.

A bare branch name, a new branch and a harmless command exited zero.
A forbidden form after a separator still exited 2, so a separator hides
nothing.
A forbidden form inside a shell wrapper exited 2, after the quote strip was
added.
A quoted mention inside an `echo` exited 0, and so did a `grep` for the word.
The `sed` fallback was proved with `jq` off the path.

**Evidence.** Measured on 2026-09-15, on this branch over `3a63144`, with 15
payloads on stdin.

**Checks.** `.claude/settings.json` runs `scripts/refuse_shared_tree.sh` before
every Bash call.
