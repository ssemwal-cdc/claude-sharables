---
id: D46
slug: bar-ignores-filter
kind: decision
status: superseded
date: 2026-08-24
---
# The bar ignores filters

**Superseded by** D91, review-only plugins, on 2026-09-18. Execute mode was retired. The rule returns with it, and the text lives on in `actionable-retired/`.

**Rule.** Build the execute bar from every item, never from the filtered list. Count the tiles against the filter.

**Outcome protected.** A decision made before a filter was applied still executes.

**Argument.**

The bar reads the full item list, never the filtered one.

A marked item that is currently filtered off screen still has to execute.

Narrowing the bar to what is visible is the obvious-looking tidy-up. It would silently drop decisions the user made before they filtered.

The tiles are the opposite case, and the distinction is load-bearing. A tile reading 9 above a list showing 2 was a real contradiction.

So the tiles count the filtered set against the whole queue. That helper is a shared block.

Both the block comment and the test say which side is which. Do not remove either.

One detail is worth keeping. The helper emits the of-total half in a small light span. At full size a filtered money figure wraps inside a 136px tile and makes the whole row 18px taller.

**Evidence.**

- The tile contradiction was fixed 2026-08-24.
- The bar test was missing until 2026-08-20. The note asserted one existed for a day and it did not. That is worth remembering the next time these records claim coverage.
- The card rules came from a blind critique. See F55, four rules from a critique.
- The per-row amber caveat is gone. See F52, amber was the real finding.
- Larger type measured worse. See F54, bigger type measured worse.
- The freshness fold needed a flex fix. See F58, a fold restored the height.
- The more control needs real clipping. See F59, a clamp needs real clipping.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
