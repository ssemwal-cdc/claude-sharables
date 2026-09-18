---
id: D57
slug: provenance-ids-allowed
kind: decision
status: settled
date: 2026-08-24
---
# Provenance may cite ids

**Rule.** Cite the record id and the date in a defect finding. Keep those ids out of shipped examples.

**Outcome protected.** Every documented defect is traceable to a record and a date.

**Argument.**

A finding that names the bill and the two purchase orders is the evidence that the bug was real.

The epistemics of this repo rest on claims being traceable to a record and a date.

Stripping those ids would leave the findings unfalsifiable, which is worse.

They live in maintainer-facing records, not in patterns a teammate copies.

The copied patterns are covered by D60, shipped examples use placeholders.

**Evidence.**

- Separated from the placeholder rule 2026-08-24, when the two cases were conflated.
- The worked example is `F‹phantom-po-miscoding-flag-was-wrong›`, bill PO
  comes from linkage.

**Checks.** none
