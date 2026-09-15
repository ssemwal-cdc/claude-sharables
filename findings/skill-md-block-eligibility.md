---
id: pending
slug: skill-md-block-eligibility
kind: finding
status: observed
date: 2026-08-24
---
# Only 34 SKILL.md lines eligible

**Outcome protected.** Nobody rewords a correct skill to raise a sharing percentage.

**Argument.**

Most of what the two skills share is near-identical, not identical.

The same paragraph carries the NetSuite skill name in one file and the Procore name in the other. Some paragraphs differ by a path.

So the shared coverage is much smaller than the duplication suggests.

Do not force it by rewording one plugin to match the other. The names are correct as they are.

**Evidence.**

- Measured 2026-08-24. 72 lines sit in contiguous byte-identical runs across the 800-line and 660-line files.
- About 34 of those 72 have clean paragraph boundaries.
- Most of the Step 0 ladder is ineligible. Its second rung carries a per-plugin asset path inside a list item.

**Checks.** `shared_blocks.py --check` fails a block that is not byte-identical in both plugins.
