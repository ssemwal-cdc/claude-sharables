---
id: D15
slug: one-state-file-per-skill
kind: decision
status: settled
date: 2026-08-12
---
# One state file per skill

**Rule.** Give each skill one state filename that no other skill shares. Quarantine a foreign record rather than merging it.

**Outcome protected.** A verdict from one system never lands in the other log.

**Argument.**

Each skill owns exactly one file and carries that as an absolute rule.

A foreign record is quarantined, never merged.

Never give two skills the same state filename, however different their folders.

A cloud-sync conflict copy is a different case. See D74, adopt config from conflict copy.

**Evidence.**

- Recorded 2026-08-12 after F11, a shared filename crossed records.

**Checks.** none
