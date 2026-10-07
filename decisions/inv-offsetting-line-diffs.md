---
id: pending
slug: inv-offsetting-line-diffs
kind: decision
status: settled
date: 2026-10-07
---
# Offsetting line differences warn only at zero net

**Rule.** Offsetting whole-dollar differences on lines other than payment due give a warning naming the lines. Three conditions must hold. Each differing line is off by at most $1. Payment due ties exactly. The differences net to $0. Anything larger is a FLAG.

**Outcome protected.** A rounding wash does not bury a real error among flags.

**Argument.**

Whole-dollar differences that cancel leave the amount due correct.

A difference that does not cancel moves money. It is a flag.

**Evidence.**

- Owner ruling, 2026-10-07, from the 2026-10-07 field run.

**Checks.** none yet. The rule lives in the skill prose.
