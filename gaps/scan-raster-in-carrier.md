---
id: pending
slug: scan-raster-in-carrier
kind: gap
status: unobserved
date: 2026-10-02
---
# Rasterising a scan in the carrier tab is probed, not proven

**Outcome protected.** A scanned-PDF read is trusted only as far as it was actually run.

**Argument.** The carrier tab is an ordinary HTML page, so `OffscreenCanvas` and pdf.js rendering work there with no DOM workaround.

That was probed live 2026-10-02, on a PDF tab against a public file, not an S3 attachment.

A scanned Procore or NetSuite attachment, rasterised this way and then visually read, has not been run.

This gap closes the moment a real scanned attachment goes through the route and someone reports the outcome.

**Evidence.**

- Measured live 2026-10-02: `OffscreenCanvas` and pdf.js probed on a public PDF tab only.
- Same pass as F‹carrier-tab-reads-s3›, the carrier-tab reads.

**Checks.** none
