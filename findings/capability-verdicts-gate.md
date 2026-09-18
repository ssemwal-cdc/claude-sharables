---
id: F74
slug: capability-verdicts-gate
kind: finding
status: observed
date: 2026-08-26
---
# Capability rows name real verdicts

**Outcome protected.** A capability table cannot promise a verdict the publish script rejects.

**Argument.**

The NetSuite attachment row said a missing attachment makes the item skipped. That verdict is not in the NetSuite allowlist, and the publish script aborts on it.

It was almost certainly copied from Procore, where that verdict is real.

The template-branch check did not catch it. That check reads the template branches, not the skill prose telling a run which verdict to assign. The two are different surfaces and both now have a gate.

It bit on the first attempt. The gate reads every backticked verdict in the absence-behaviour column. So a sentence explaining that the verdict does not exist here failed it too.

The row says so in plain words for that reason. Do not re-add the backticks.

**Evidence.**

- Added 2026-08-26 and mutation-tested. Putting the wrong verdict back fails the build.
- The template-branch gate is D63, gate template verdicts against publish.

**Checks.** `check_capability_verdicts()` in `scripts/shared_blocks.py`.
