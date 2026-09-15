---
id: D64
slug: workspace-folder-downloads
kind: decision
status: settled
date: 2026-08-24
---
# Declare the workspace folder Downloads

**Rule.** Tell the reader to use Downloads as the workspace folder. Never offer a choice of folder.

**Outcome protected.** A second run finds the state file and skips first-run setup.

**Argument.**

The idempotency gate reads `<folder>/_netsuite_review_log.json`. A reader who picks a different folder on the second run is a new user to that gate.

Such a reader is asked every setup question again. So a declared folder is load-bearing, not tidiness.

Downloads is safe because neither skill writes an attachment there. Both read PDFs and workbooks in the page.

The onboarding sheet used to say to point it at any folder. That was two defects in one line. The phrase is picker jargon, and the choice buys the reader nothing.

**Evidence.**

- Changed 2026-08-24 in `docs/onboarding.html`.
- The write to that folder works and the folder appears in Downloads, confirmed 2026-08-27. See F85, the workspace write works.

**Checks.** none
