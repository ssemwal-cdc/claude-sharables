---
id: pending
slug: pdf-geometry-line-math-confirmed
kind: finding
status: observed
date: 2026-09-24
---
# PDF geometry line math confirmed

**Outcome protected.** A quantity times rate check reads the invoice's real columns.

**Argument.** NetSuite rebuilds invoice rows from pdf.js geometry.
It buckets by y, sorts by x, and pads by a character width from `item.width / str.length`.
Both tools merge left and right columns when rows share a y coordinate.
That is a parsing constraint to split on an x threshold, not a regression to fix.

**Evidence.** Reported 2026-09-24 by the maintainer: NetSuite runs have flagged or cleared line
math correctly on multi-column invoices.
Tested live 2026-08-13 against bill 2532506, before any file was changed.
Checked against `pdftotext -layout` on a 3-page utility invoice.
That check gave the same three columns and the same figures.
`python3 scripts/test_skill_code.py` extracts this code from `SKILL.md` and runs it against mocks.

**Checks.** `scripts/test_skill_code.py`, which reads the extractor out of `SKILL.md`.
