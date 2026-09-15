---
id: D25
slug: ocr-never-clear-verdict
kind: decision
status: settled
date: 2026-08-14
---
# An OCR figure never clears

**Rule.** Look at an image in the browser. Use OCR as a fallback, and never let an OCR figure produce a `clear` verdict.

**Outcome protected.** A misread digit in an eight-figure line never passes as verified.

**Argument.**

Chrome renders the file, so navigating to it and reading it visually is more accurate and needs no CDN.

OCR is the fallback only. An OCR-derived figure is labelled as read by OCR and not independently verified, and the item stays flagged for a human.

A misread digit in an eight-figure line is worse than an honest skip, and a table is exactly where OCR misreads.

If that cap ever feels noisy, fix the visual read. Do not relax the cap.

**Evidence.**

- Recorded 2026-08-14. The visual read tool is confirmed. See F20, one visual read exists.
- The OCR branch has never fired, so the noise level is `unmeasured`.

**Checks.** none
