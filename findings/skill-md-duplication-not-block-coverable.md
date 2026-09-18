---
id: F121
slug: skill-md-duplication-not-block-coverable
kind: finding
status: observed
date: 2026-08-24
---
# SKILL.md duplication resists the block mechanism

**Outcome protected.** Nobody expects the shared-block mechanism to reach prose it cannot
cover.

**Argument.** The `SKILL.md` duplication found by the drift audit is mostly
near-identical rather than identical.
It is the same paragraph with the plugin's own name and workspace folder
substituted.
So the block mechanism can never cover most of that surface as written.
See D49, do not widen a block over near-identical prose.

**Evidence.** Audit dated 2026-08-24.
`dashboard_template.html`: 528 lines against 603, with 308 identical, 54.5%
Dice.
`publish_dashboard.py`: 148 lines against 238, with 106 identical.
The CSS blocks alone were 92.5% identical.
Across the two `SKILL.md` files, 250 to 300 of 1,495 lines were duplicated or
near-duplicated.
Only 72 of about 1,500 lines sit in contiguous byte-identical runs.
Only about 34 of those have clean paragraph boundaries.

**Checks.** none.
