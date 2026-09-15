---
id: pending
slug: getdocument-needs-uint8array
kind: finding
status: observed
date: 2026-08-13
---
# getDocument needs a typed array

**Outcome protected.** A valid PDF parses instead of sending someone to debug the fetch.

**Argument.**

Passing an array buffer to the pdf.js document loader throws an invalid-PDF error on valid bytes.

Wrapping the buffer in a typed array fixes it immediately.

The Procore recipe always wrapped. That looked like style and is load-bearing.

Both skills now carry a comment saying so, because the wrap is exactly what a later pass removes as redundant.

The error it produces sends you debugging the download instead of the call.

**Evidence.**

- Observed 2026-08-13. Right content type, a `%PDF-1.6` header and 1,126,323 bytes, and it still threw.

**Checks.** `scripts/test_skill_code.py` extracts the loader from `SKILL.md`.
