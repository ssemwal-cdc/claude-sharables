---
id: pending
slug: tick-must-not-render
kind: finding
status: observed
date: 2026-08-24
---
# The tick must not render

**Outcome protected.** An open detail stays open while the reader reads it.

**Argument.**

A live run reported that show detail worked for some rows and not all, and felt random.

It was not random. The render call rebuilds the row list from markup, so every expanded detail and every opened more control collapsed.

Which rows survived depended only on where the 60-second boundary fell relative to the clicks.

The tick now ages the freshness line and flips the snapshot pill, and touches nothing else.

That is the whole job a tick has here. The page is a snapshot and the data never changes.

So this is not a narrower guard. It is the removal of work that should never have been in the interval.

Any future expandable is safe by construction rather than by remembering to opt in.

The old guard covered input and select elements only. So typing a rejection reason was safe and reading a card was not.

**Evidence.**

- Measured on template v9. A click gives an expanded display value, and one render later it is empty with the label back to show detail.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
