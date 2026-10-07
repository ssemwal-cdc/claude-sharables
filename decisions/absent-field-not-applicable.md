---
id: pending
slug: absent-field-not-applicable
kind: decision
status: settled
date: 2026-10-07
---
# An absent field is not applicable

**Rule.** A check whose input field the tool lacks entirely is `not applicable`. Setup records it in `absentFields`. It never blocks `tied` or `clear`. `not mapped` still blocks.

**Outcome protected.** A verified item is not held back by a check that can never run.

**Argument.**

Customer Change Risk has no proposed-cost field. Check 4 could never run there.

Calling that `not mapped` blocked every item on the tool.

Blank, not mapped and not applicable are three states. D41, three states never a boolean, argues the same.

**Evidence.**

- Owner ruling, 2026-10-07, from the field run on company 2866.
- That tool's Cost Impact read null on all 37 items.

**Checks.** none yet. The rule lives in the skill prose.
