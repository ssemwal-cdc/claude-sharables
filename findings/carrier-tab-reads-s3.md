---
id: pending
slug: carrier-tab-reads-s3
kind: finding
status: observed
date: 2026-10-02
---
# A carrier tab reads the presigned S3 link in place

**Outcome protected.** An attachment is read without a file moving between tabs, a download, or a route built around a refusal.

**Argument.**

Three claims this skill once carried are wrong, each measured live 2026-10-02 against a real Procore attachment.

`javascript_tool` does attach to a PDF tab. `document.contentType` reads `application/pdf` there.

A presigned `s3.amazonaws.com` link is not readable off a `tabs_context_mcp` or `navigate` result. Its `X-Amz-*` signature parameters come back redacted. Inside the page, `location.href` stays intact.

`getDocument` detaches the `ArrayBuffer` it is handed. `byteLength` has to be read before parsing, never after.

The route that holds given those three facts: one carrier tab on `app.procore.com`, never the fetch tab. It fetches the record JSON, then schedules `location.href = attachment.url` with `setTimeout(..., 50)`, so the call returns before the tab unloads. The next call in that tab, inside the 60-second window, lands on the presigned link already. It fetches it there, same-origin, no CORS wall.

Measured on a real attachment: an 18-page, 4,784,043-byte PDF extracted in 853 ms. pdf.js 4.0.379 loaded from cdnjs, worker fetched as a blob. No download. No cross-tab traffic. No refusal.

A PNG attachment sniffed `137,80,78,71`, `image/png`, 188,644 bytes, shown inline. A `computer` screenshot of that same carrier tab read the drawing.

**Evidence.**

- Measured live 2026-10-02, Claude in Chrome, Claude Code auto mode, real Procore attachments.
- Corrects the "javascript_tool cannot attach to a PDF tab" claim this skill once carried.
- Corrects the "the presigned URL is readable in the tool result" claim too.

**Checks.** `scripts/test_skill_code.py` runs `__sniff` against the same byte patterns.
