---
id: pending
slug: inv-offsetting-line-diffs
kind: decision
status: settled
date: 2026-10-07
---
# Offsetting line differences warn only at zero net

**Rule.** Offsetting whole-dollar differences on lines other than payment due give a warning naming the lines. That holds only when payment due ties exactly and the differences net to $0. Otherwise FLAG.

**Outcome protected.** A rounding wash does not bury a real error among flags.

**Argument.**

Whole-dollar differences that cancel leave the amount due correct.

A difference that does not cancel moves money. It is a flag.

**Evidence.**

- Owner ruling, 2026-10-07, from the field run on company 2866.

**Checks.** none yet. The rule lives in the skill prose.
