---
id: pending
slug: invalid-font-shorthand-dropped
kind: finding
status: observed
date: 2026-09-23
---
# An invalid shorthand was dropped

**Outcome protected.** A control renders in the font the template authored for it.

**Argument.**

Both dashboard templates wrote `font:500 12.5px/1 inherit` on their form controls.

That declaration is invalid. `inherit` is a CSS-wide keyword, and a CSS-wide keyword is legal only as a property's whole value. It cannot be one component of a shorthand.

So the browser discards the whole declaration, not the offending part alone. The control falls back to the user-agent default form font.

Nothing errors and nothing logs. Arial at weight 400 reads as a deliberate plain interface font, which is why this survived in both templates.

A second defect sat underneath it. `line-height:1` leaves no room for a descender, so the authored style clipped the `g` in "flagged" wherever it did apply.

Fixing the first defect is what exposed the second. Split a shorthand to longhands and the clip arrives with it.

**The trap for the next reader.** Splitting `font:...` to longhands at `line-height:1` reintroduces the clip. Use `1.2`.

**Evidence.**

- Reported 2026-09-23 from a screenshot of the NetSuite Sort control, clipped on "Verdict — flagged first".
- Measured in Chromium 1194. The shorthand computes to Arial, 400, 13.33px. The longhands compute to the authored family and weight.
- Measured twice, by two readers, independently.
- Six sites carried it. `select` and `input[type=text]` were fixed in commit `0efa8ed`. `button` and `.pwarn .more` were fixed in commit `49a5fcf`.
- The second commit was needed because the first argued that no `button` renders inside the toolbar. True, and irrelevant, because `button` is an unscoped element selector.
- `D70`, measure position in a browser, is the rule that catches a layout change of this kind.

**Checks.** none. No check reads computed style. `scripts/measure_float.js` measures position, never font.
