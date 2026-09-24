---
id: pending
slug: netsuite-connector-extra-files
kind: gap
status: unobserved
date: 2026-09-24
---
# NetSuite connector misses extra files

**Outcome protected.** A new file on a bill that was already reviewed gets read before the verdict carries forward.

**Argument.**

A NetSuite bill can hold several attached files. The maintainer confirmed that on 2026-09-24.

In connector mode, the skill lists only the files that the AP INVOICE or CHANGE ORDER ATTACHMENT field names. No connector query lists the other files on a transaction.

So in connector mode, a new unnamed file on a carried clear bill is not detected. The carry holds, and nobody reads the new file.

Browser mode reads every `media.nl` link on the record page, so it sees every file. That read is designed, but no run has executed it.

The skill names this limit as a bandaid. One fix is a connector route that lists every file on a transaction. Another is the browser link read in both modes.

**Evidence.**

- The review of the NetSuite carry change found the limit on 2026-09-24. It predates that change, because connector mode never listed the other files.
- Whether any real bill has changed its unnamed files after a clear verdict is `unmeasured`.

**Checks.** none
