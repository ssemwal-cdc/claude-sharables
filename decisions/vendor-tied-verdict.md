---
id: D107
slug: vendor-tied-verdict
kind: decision
status: settled
date: 2026-10-07
---
# A sixth verdict where only the vendor's proposal ties

**Rule.** An `icr` with a blank accepted cost and a blank Cost Impact earns `vendor-tied`. Vendor Proposed must be populated and found verbatim as the attached proposal's total. Checks 3 and 5 must pass. The support outcome must be `text` or `spreadsheet`. `supportRead` must not be empty. It ranks below `tied` and above `skipped`. A Vendor Proposed that does not match stays `skipped`, and the row names the mismatch. It is not a flag.

**Outcome protected.** An item whose only checkable figure was verified reaches the reviewer. It is never buried beside items where nothing was verified.

**Argument.**

The 2026-10-07 field run skipped 49 items on a blank accepted cost. Some carried a vendor proposed figure that ties to the proposal. `skipped` hid that evidence.

`tied` cannot take them. It asserts an approved figure, and none exists. Check 2, tie to accepted, never to proposed, still holds wherever an accepted cost exists.

The name states evidence, never action (D6, never act without an instruction). The verdict is in the allowlist, the review step vocabulary and the template together (D63, gate verdicts against publish).

A Cost Impact that is present goes to check 7 as before. `vendor-tied` never applies then.

D105, no folder, no reads where nothing can tie, now has a limit. It skips only if Vendor Proposed is blank, absent or not mapped. Otherwise a `vendor-tied` can be found.

**Evidence.**

- Incident: the 2026-10-07 field run, 49 skips from a blank accepted cost.
- Related: D92, fifth verdict for a verified blank.

**Checks.** `scripts/test_skill_code.py`: `test_vendor_tied_verdict`, `test_vendor_tied_vocabulary_checks`. `check_verdict_vocabulary()` and `check_capability_verdicts()` in `scripts/shared_blocks.py`.
