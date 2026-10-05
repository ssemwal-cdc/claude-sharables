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

A `.docx` or `.doc` now has a route. Decision D‹run-downloads-word-files›, a run downloads Word files itself, allows it. A run navigates a carrier tab to the attachment URL on purpose. Chrome then saves the file into Downloads. The run reads it there with `__read_docx`. That route is still unobserved end to end. Whether Chrome saves the file silently, or asks where to save it, is unmeasured. No real run has tried it yet.

A workbook, a `.csv`, or a `.msg` still has no route beyond the download fallback. What a carrier navigation to one of those does was never run. None is planned. They stay named by the user, never navigated to directly.

This gap closes for Word files once a real run tries that route and reports what Chrome actually did. For the other types, it closes only if a route is built for them.

**Evidence.**

- Measured live 2026-10-02: not run. Noted alongside F166, the carrier-tab reads that pass did measure.
- 2026-10-05: the user opted in to the Word route (D‹run-downloads-word-files›, a run downloads Word files itself). Still unmeasured live.

**Checks.** none
