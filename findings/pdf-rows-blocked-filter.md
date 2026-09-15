---
id: F15
slug: pdf-rows-blocked-filter
kind: finding
status: observed
date: 2026-08-13
---
# Stub rows trip the filter

**Outcome protected.** An extracted invoice page returns figures instead of a redaction marker.

**Argument.**

Returning a whole extracted page came back as a blocked cookie or query-string marker.

The payment stub barcode rows and a 30-digit remittance string read as query-string data.

Dropping rows that are only spaces, zeroes and ones, and rows carrying 20 or more consecutive digits, clears it.

Long returns also truncate, so pages come back one per call.

Procore already documented this filter for JavaScript source. This is the same filter reached from a direction that note did not cover.

**Evidence.**

- Observed 2026-08-13. The drop costs 15 of 60 rows, all stub noise, no figures.
- The same filter has a second trigger. See D21, a blocked marker is never a value.

**Checks.** `scripts/test_skill_code.py` runs the size-budgeted page reads.
