---
id: F16
slug: pdfjs-in-page-csp-allows
kind: finding
status: observed
date: 2026-08-13
---
# pdf.js runs in-page

**Outcome protected.** No attachment reaches disk, and no download step can fail.

**Argument.**

The question was whether the content security policy would allow a CDN import inside a NetSuite tab. It does.

A dynamic import from cdnjs inside a NetSuite app tab loads. The worker fetches as text and is assigned as a blob URL, exactly as the Procore recipe does.

A credentialed same-origin fetch of the NetSuite media URL returns the PDF. Nothing reaches disk.

NetSuite loads pdf.js in the record tab rather than a scratch tab because the media URL needs the session cookie. So the fetch must be same-origin, and pdf.js must be where that origin is.

Testing this before changing any file is the order worth keeping. The question is answerable in a chat in ten minutes and it gates the whole design.

**Evidence.**

- Tested live 2026-08-13 against bill 2532506, before any file was changed.

**Checks.** none
