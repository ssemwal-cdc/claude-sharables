---
id: pending
slug: bar-ignores-filter
kind: decision
status: settled
date: 2026-08-24
---
# The bar ignores filters

**Rule.** Build the execute bar from every item, never from the filtered list. Count the tiles against the filter.

**Outcome protected.** A decision made before a filter was applied still executes.

**Argument.**

The bar reads the full item list, never the filtered one.

A marked item that is currently filtered off screen still has to execute.

Narrowing the bar to what is visible is the obvious-looking tidy-up. It would silently drop decisions the user made before they filtered.

The tiles are the opposite case, and the distinction is load-bearing. A tile reading 9 above a list showing 2 was a real contradiction.

So the tiles count the filtered set against the whole queue. That helper is a shared block.

Both the block comment and the test say which side is which. Do not remove either.

One detail is worth keeping. The helper emits the of-total half in a small light span, because at full size a filtered money figure wraps inside a 136px tile and makes the whole row 18px taller.

**Evidence.**

- The tile contradiction was fixed 2026-08-24.
- The bar test was missing until 2026-08-20. The note asserted one existed for a day and it did not, which is worth remembering the next time these records claim coverage.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
