---
id: F25
slug: xlsx-cdnjs-import-works
kind: finding
status: observed
date: 2026-08-14
---
# The cdnjs import works

**Outcome protected.** A workbook attachment is read with the simplest loader.

**Argument.**

A dynamic import of the cdnjs build populates the global on the first attempt. A workbook then round-trips through the read and the sheet-to-CSV calls.

Four fallbacks sat behind it and none was reached. So none is known to work.

Do not add one back as a safety net. An untested fallback is not a safety net.

The reason this took two rounds is worth keeping. Reachability is not executability.

The first probe fetched five CDNs and all five returned a 200 response. That says the connect directive allows them and says nothing about the script directive.

cdnjs was the only host with evidence for executing code. That evidence was the pdf.js recipe already doing it in production.

Anyone extending this to a new library should test the import, not the fetch.

The pinned version predates the SheetJS prototype-pollution and ReDoS fixes. That is accepted deliberately, because parsing happens in a scratch tab holding no session. The output is also data that is never executed.

The SheetJS CDN serves a current build and fetches fine. Executing from it is untested for exactly the reason above.

**Evidence.**

- Probed live 2026-08-14. The pin is xlsx 0.18.5.
- The four unreached fallbacks were a blob import, a namespaced script element and a function constructor. The fourth was an ES module from the vendor CDN.
- A target version for the pin is an open decision. See D86, name the fixed xlsx version.

**Checks.** `check_pins()` in `scripts/shared_blocks.py`.
