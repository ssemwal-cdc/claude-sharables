---
id: F110
slug: netsuite-bin-fed-dead-live-state
kind: finding
status: settled
date: 2026-08-24
---
# NetSuite's actioned bin fed dead state

**Outcome protected.** The queue count on the dashboard matches the queue.

**Argument.** A documentation sweep found this, not a run.
Both skills' carry-forward rules kept an item for one run after it left the
queue. That let the dashboard show it in an actioned bin.
Neither bin could render.

NetSuite's was collateral from the same day.
Its bin was fed by the `gone` state.
That state belonged to the dead `live` machinery, removed earlier that day as
unreachable.
The instruction that fed the bin was not updated with it.
That is self-inflicted drift, caught within hours only because the sweep went
looking.

**Evidence.** Found 2026-08-24 by a documentation sweep.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py`.
