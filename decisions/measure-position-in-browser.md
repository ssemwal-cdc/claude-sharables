---
id: D70
slug: measure-position-in-browser
kind: decision
status: settled
date: 2026-08-27
---
# Measure position in a browser

**Rule.** Run `scripts/measure_float.js` by hand after touching the dashboard layout.

**Outcome protected.** A bar this repo calls pinned is actually pinned.

**Argument.**

Everything the floating header claims is positional, and the static checks cannot see position.

This repo has shipped a pinned bar that was not pinned twice, and both times the CSS read correctly.

So the script reproduces the host arrangement and measures it. That is a cross-origin frame sized to its own content, a scrolling parent, and both dashboards published from fixtures.

It is not in CI, and `validate.py` may not assume a browser.

Run it after touching the band track block, the float CSS block, the header mirror block, or anything that changes the page height.

Invoke it with the global module path exported, then node and the script path.

**Evidence.**

- Added 2026-08-27. The two wrong pins are F47, sticky resolves against its parent, and F82, the widget frame does not scroll.

**Checks.** `test_dashboard_view` pins the mechanism. The position itself is checked by hand only.
