---
id: pending
slug: phantom-bin-inflated-queue-count-only
kind: finding
status: observed
date: 2026-08-24
---
# The dead bin inflated a count, not a click

**Outcome protected.** A departed item never causes a wrong click, only a wrong number.

**Argument.** The harm from the two dead actioned bins was mild and real.
A departed item lingered as an apparently pending row for one run.
That inflated the queue count.
Execute would have skipped it, because it re-verifies before every click.
So this could never have caused a wrong click, only a wrong number.

**Evidence.** Found 2026-08-24 by a documentation sweep.
The queue-count inflation was one row per departed item, for one run.
`unmeasured` in aggregate.

**Checks.** none.
