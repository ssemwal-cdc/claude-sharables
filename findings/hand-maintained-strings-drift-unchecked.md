---
id: F108
slug: hand-maintained-strings-drift-unchecked
kind: finding
status: observed
date: 2026-08-24
---
# Hand-maintained strings drift unchecked

**Outcome protected.** A claim that names an identifier gets a mechanical check, not just a
human re-read.

**Argument.** A nine-agent prose audit found a general pattern behind its specific defects.
Every number a command regenerates was verified correct that day.
Almost every string a human retyped had drifted.

The corpus's defects cluster on hand-maintained text that no command reads.
That argues for extending mechanical checks into prose wherever a claim names an
identifier.
Treat any unchecked string near a click as suspect by default.

**Evidence.** Audit dated 2026-08-24.
122 raw findings, 29 surviving contest.

**Checks.** none.
