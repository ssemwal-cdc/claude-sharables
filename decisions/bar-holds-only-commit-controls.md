---
id: pending
slug: bar-holds-only-commit-controls
kind: decision
status: settled
date: 2026-08-24
---
# Keep reference text out

**Rule.** Put reference text in the note below the bar. Keep the bar to what a reviewer needs before a click.

**Outcome protected.** A reviewer can see the queue the bar floats over.

**Argument.**

The stale-snapshot warning and the stale-safe explainer moved below the bar into the note element.

Inside the bar they made it over a third of a 700px viewport tall.

Anything added to the bar is paid for in queue you cannot see.

**Evidence.**

- Measured 2026-08-24. The bar was 249px with the reference text and both dashboards now measure 153px.

**Checks.** `scripts/measure_float.js` by hand.
