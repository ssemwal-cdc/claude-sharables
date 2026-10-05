---
id: G21
slug: office-attachment-route
kind: gap
status: unobserved
date: 2026-10-02
---
# A carrier navigation to an office file is unobserved

**Outcome protected.** A run names an office-document type as unobserved instead of assuming Chrome handles it safely.

**Argument.** The carrier-tab route is only ever navigated for a viewable type: pdf, png, jpg, jpeg, gif, tif, tiff, webp.

What a carrier navigation to `.xlsx`, `.docx`, `.csv` or `.msg` does was never run. Chrome may download it straight into the Downloads folder, which this skill's workspace rules do not expect or permit.

So every non-viewable type goes to the download fallback instead, named by the user, never navigated to directly.

This gap closes the moment someone runs that navigation once and reports what Chrome actually did.

**Evidence.**

- Measured live 2026-10-02: not run. Noted alongside F166, the carrier-tab reads that pass did measure.

**Checks.** none
