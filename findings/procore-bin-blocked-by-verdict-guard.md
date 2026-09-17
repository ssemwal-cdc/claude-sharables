---
id: pending
slug: procore-bin-blocked-by-verdict-guard
kind: finding
status: settled
date: 2026-08-24
---
# Procore's actioned bin never worked

**Outcome protected.** The queue count on the dashboard matches the queue.

**Argument.** A documentation sweep found this, not a run.
Procore's actioned bin never worked, and the guard that blocks it was added
deliberately.
Its template filtered `bin` on `verdict === "gone"`.
`gone` is not in Step 6's vocabulary.
The publish script's `VERDICTS` allowlist would abort on it.
So the bin never rendered in any run.
It could not render without a fourth verdict nobody defined.

Both carry-forward rules now say drop the item instead of keeping it for the
bin.
Both bins are gone.
Procore's markup, CSS and filter were removed once no run could reach them.
Finishing the bin would have meant inventing a fifth verdict nobody had asked
for.

**Evidence.** Found 2026-08-24 by a documentation sweep.
The Procore bin had never rendered in any run since it shipped.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py`.
