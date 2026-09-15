---
id: pending
slug: three-states-never-boolean
kind: decision
status: settled
date: 2026-08-20
---
# Three states, never a boolean

**Rule.** Keep a successful read, a genuine absence and a failure as three named states. Never collapse them.

**Outcome protected.** A failed read is never reported as an absent thing.

**Argument.**

This is the shape these records keep recording. A distinct failure folded into a category that means something else never surfaces.

The purchase order linkage has three states. Linked means that purchase order is the coding and is authoritative. Unlinked means the query succeeded and found none, and the typed value is all there is. Failed means the query errored, which is unknown and never unlinked.

Every fan-out returns three states per item. An ok state, an empty state where the API genuinely returned nothing, and a failed state carrying the code.

A failed state is named and excluded. It is never folded into the suppressed count.

A rate-limit response is a failure, not an empty result.

The same rule covers the write states in the workspace folder, the attachment outputs, and the connector call.

**Evidence.**

- Applied to the purchase order path 2026-08-20, the fifth instance of the shape at that date.
- The four earlier instances are the fan-out empty state against its failed state, and the change order wrong id returning 200 empty. The other two are a workbook read as expired, and a redaction marker read as an empty field.
- The sixth instance is the workspace write. See F‹write-states-kept-refused-not-attempted›, three write states.
- The gate query needs an explicit page size. See F‹per-page-100-required›, workflow queries need per_page.
- The link rows need deduplication. See F‹ordbill-dedupe-line-pairs›, dedupe the link rows first.
- The fan-out design is F‹fanout-three-states-cap›, the fan-out caps concurrency.

**Checks.** `scripts/test_skill_code.py` runs the three-state fan-out, mutation-tested. Collapsing a rate-limit response into the empty state fails the build.
