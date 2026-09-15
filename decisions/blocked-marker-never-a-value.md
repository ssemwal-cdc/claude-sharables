---
id: D21
slug: blocked-marker-never-a-value
kind: decision
status: settled
date: 2026-08-14
---
# Never trust a blocked marker

**Rule.** Re-return a redacted field in another shape. Never let a blocked marker reach a verdict, a comment or a dashboard.

**Outcome protected.** A redacted figure is read again instead of read as empty.

**Argument.**

A blocked marker is never a value.

Re-return the field in another shape and read it again.

Never read the marker as the field being empty. A redaction that reads as an empty field is the same silent misfile as the rest of these records.

**Evidence.**

- Recorded 2026-08-14 from F23, the filter has a second trigger.
- The first trigger is F15, stub rows trip the filter.

**Checks.** none
