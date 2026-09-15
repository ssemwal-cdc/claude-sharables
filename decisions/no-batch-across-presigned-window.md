---
id: D24
slug: no-batch-across-presigned-window
kind: decision
status: settled
date: 2026-08-14
---
# Do not overrun the window

**Rule.** Batch attachment reads inside one presigned window only. Re-navigate and retry a fetch that failed or expired.

**Outcome protected.** A live invoice is never recorded as a scanned image.

**Argument.**

The presigned window is per window, not per file, so batching inside it is free.

An expired link yields no text. No text already means the support is a scanned image.

So an overrun batch converts live invoices into skipped verdicts nobody ordered.

Only a successful fetch that parsed and yielded nothing is a scan.

**Evidence.**

- Recorded 2026-08-14 with the attachment sniff table.
- The six outcomes are in F17, six attachment outcomes.

**Checks.** none
