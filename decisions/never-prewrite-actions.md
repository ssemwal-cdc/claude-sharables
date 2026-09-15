---
id: pending
slug: never-prewrite-actions
kind: decision
status: settled
date: 2026-08-12
---
# Never pre-write an action

**Rule.** Write an outcome to the actions log only after it is observed.

**Outcome protected.** The action log records what happened and nothing else.

**Argument.**

The connector lag is why this matters. A pre-written entry is a fabrication.

Later it reads exactly like a real one, so nothing can tell them apart.

The log is the record of what was clicked. It must not gain an entry nobody observed.

**Evidence.**

- Recorded 2026-08-12 with F‹connector-lag-verify-record›, verify the record not the queue.
- The same rule governs a conflict copy. See D‹conflict-copy-config-only›, adopt config from conflict copy.

**Checks.** none
