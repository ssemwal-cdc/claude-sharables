---
id: F129
slug: floating-bar-mirrors-filter-and-commit
kind: finding
status: observed
date: 2026-08-27
---
# The floating bar mirrors filter and commit only

**Outcome protected.** A reader mid-queue has the filter state and the commit button on
screen.

**Argument.** The floating bar is a way back to the header, not a replacement for it.
Its filter control scrolls the real toolbar into view, which does move the
host scroller from inside a cross-origin frame.

What floats is only what is worth having in the second before a click.
That is the filter state, one press back, and the commit button.
It is a visual duplicate, so it is hidden from assistive technology and
removed from the tab order throughout.
These are controls already in the page.

The count on it follows the filter, and the execute mirror does not.
That is the same split as D46, the execute bar ignores the filter.

**Evidence.** Closed 2026-08-27.
The full header is about 380px.
Reproducing it would cost half a 700px viewport.

**Checks.** `test_dashboard_view` pins the mechanism, mutation-tested.
`scripts/measure_float.js` measures position by hand.
