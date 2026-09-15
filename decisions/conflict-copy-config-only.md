---
id: pending
slug: conflict-copy-config-only
kind: decision
status: settled
date: 2026-09-01
---
# Adopt config from conflict copy

**Rule.** Adopt `config` keys from a cloud-sync conflict copy and say so. Never merge its items or its actions.

**Outcome protected.** A setting the user asked for survives a sync conflict, and no verdict or click is invented.

**Argument.**

A machine-suffixed conflict copy of the state file is a third state, and it had no rule.

It is neither a foreign record to quarantine nor the canonical file.

The canonical file stays authoritative for items and actions, and it is the only file written.

Never merge items. A stale verdict returning looks exactly like a fresh one.

Never merge actions. They record what was clicked and must not gain an entry nobody observed.

Leave the copy in place and name it once. The sync client made it, so it is not a stray and not the user chore.

**Evidence.**

- Observed 2026-09-01. The copy carried newer `config` than the canonical file, including a setting the user had asked for. The run merged the two.

**Checks.** none
