---
id: F153
slug: toolbar-select-overflow
kind: finding
status: observed
date: 2026-09-23
---
# Long option text overflows toolbar

**Outcome protected.** A reader on a narrow panel is not made to scroll sideways.

**Argument.**

A toolbar `select` carries no `max-width`. Its width follows its longest option.

A long filter value therefore pushes the toolbar wider than the panel. The reader gets a horizontal scroll.

This is recorded rather than fixed, and that is deliberate. Capping the control truncates a vendor name, which on a filter is arguably worse than a scroll.

Two fixes exist. A `max-width` with an ellipsis, or letting `.fgrp` wrap internally. Both are layout decisions nobody has made.

It does not reproduce on the repo's own fixtures, so a reader who meets it will think it is new. That is what this record is for.

**Evidence.**

- Measured 2026-09-23, during the font shorthand pass.
- A 58-character vendor name pushed the toolbar to 407px against a 380px viewport.
- Pre-existing. Measured at 427px before the font fix and 407px after. The font fix shrinks it slightly and did not cause it.
- The repo's shipped fixtures overflow by 0px at every width `scripts/measure_float.js` captures.
- `D81`, device usability check, is the rule the capture pass serves.

**Checks.** `scripts/measure_float.js`, which reports 0 horizontal overflow on the shipped fixtures and cannot see this case.
