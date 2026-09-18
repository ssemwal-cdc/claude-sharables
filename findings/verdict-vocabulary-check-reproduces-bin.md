---
id: F127
slug: verdict-vocabulary-check-reproduces-bin
kind: finding
status: settled
date: 2026-08-24
---
# The verdict check reproduces the dead bin

**Outcome protected.** A check that passes because its own mutation never landed is
caught, not trusted.

**Argument.** The dead-bin finding turned out to be automatable.
The first version of this note said it probably was not.
`check_verdict_vocabulary()` asserts every verdict a template branches on is
one its script can emit.
It reproduces the Procore bin exactly, and it is mutation-tested.

The first attempt at that test passed silently, because the injecting `sed`
had not applied.
So the check looked verified when nothing had been checked.
Re-run properly, it fires and names the file, the verdict and the allowlist.
A check that passes because the mutation never landed is worse than no check.
It also certifies itself.

**Evidence.** Found 2026-08-24 by a documentation sweep.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py`,
mutation-tested.
