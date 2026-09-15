---
id: F20
slug: computer-only-visual-read
kind: finding
status: observed
date: 2026-08-14
---
# One visual read exists

**Outcome protected.** A scanned invoice is looked at instead of reported unreadable.

**Argument.**

The screenshot tool is the only visual read in the browser tool set.

The page-text and read-page tools extract text. The find tool locates text. The console and network tools read logs. The image upload tools are inputs rather than reads.

So a scanned invoice or a photographed proposal is read by screenshotting.

No text extractor will ever return anything for one. Reaching for them is precisely what produced support present but unreadable.

With a real visual read available, OCR should be a rare fallback rather than the normal path.

**Evidence.**

- Confirmed against the live tool list 2026-08-14.

**Checks.** none
