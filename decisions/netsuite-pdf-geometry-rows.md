---
id: D17
slug: netsuite-pdf-geometry-rows
kind: decision
status: settled
date: 2026-08-13
---
# Rebuild NetSuite rows from geometry

**Rule.** Rebuild PDF rows from pdf.js geometry on NetSuite. Never flatten a page by joining item strings.

**Outcome protected.** The quantity, rate and line-tie checks read aligned columns.

**Argument.**

Joining the pdf.js item strings flattens the page and destroys column alignment.

Column alignment is what the quantity by rate check and the line-tie check read.

So NetSuite buckets items by y and sorts by x. It then pads by a character width derived from the item width over the string length.

Both tools merge a left and a right column on a two-column page when rows share a y coordinate. That is a parsing constraint to split on an x threshold, not a regression to fix.

**Evidence.**

- Checked 2026-08-13 against a layout-preserving command-line extraction of a 3-page utility invoice. Same three columns and same figures.
- pdf.js runs in the record tab. See F16, pdf.js runs in-page.
- The loader needs a typed array. See F14, getDocument needs a typed array.
- The scratch tab is an XML document. See F26, the scratch tab is XML.

**Checks.** `scripts/test_skill_code.py` runs the layout extractor out of `SKILL.md`.
