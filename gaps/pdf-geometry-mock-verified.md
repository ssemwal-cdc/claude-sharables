---
id: G1
slug: pdf-geometry-mock-verified
kind: gap
status: unobserved
date: 2026-08-14
---
# PDF geometry extractor, mock verified

**Outcome protected.** A quantity times rate check reads the invoice's real columns.

**Argument.** NetSuite rebuilds invoice rows from pdf.js geometry.
It buckets by y, sorts by x, and pads by a character width from `item.width / str.length`.
That extractor is verified against mocks and one live chat test.
It has never run inside a watched review.
Do not flatten the page with `items.map(z => z.str).join(' ')`.
Flattening destroys the column alignment the quantity, rate and line-tie checks read.
Both tools merge left and right columns when rows share a y coordinate.
That is a parsing constraint to split on an x threshold.
It is not a regression to fix.

To clear it: watch one review read a multi-column invoice and tie its lines out.
Compare the extracted rows against `pdftotext -layout` on the same file.

**Evidence.** This claim is guessed, not proven.
It is tested against mocks or fixtures and shipped.
Nobody has watched it work on real data inside a review.
Do not cite it as established.
`python3 scripts/test_skill_code.py` extracts this code from `SKILL.md` and runs it against mocks.
It cannot cover this gap, because this gap is about a real system.
Tested live 2026-08-13 against bill 2532506, before any file was changed.
Checked against `pdftotext -layout` on a 3-page utility invoice.
That check gave the same three columns and the same figures.
F‹end-to-end-runs-routine›, watched runs now happen routinely, but this pdf.js branch stays unwatched inside them.

**Checks.** `scripts/test_skill_code.py`, which reads the extractor out of `SKILL.md`.
