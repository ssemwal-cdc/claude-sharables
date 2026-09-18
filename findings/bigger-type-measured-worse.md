---
id: F54
slug: bigger-type-measured-worse
kind: finding
status: observed
date: 2026-08-24
---
# Bigger type measured worse

**Outcome protected.** A density change is judged by a measurement, not by a look.

**Argument.**

Two things were tried and measured wrong before landing. Both were caught by measuring the render rather than looking at it.

Raising type sizes while trying to cut density was the first. Fewer type settings is the goal. Larger type is not.

Replacing a variable-width pill with a variable-width label was the second. It shifts titles in exactly the same way the pill did.

The first pass looked better and measured worse.

**Evidence.**

- Measured 2026-08-24. The type increase cost 435px across 9 cards and bought nothing.

**Checks.** none
