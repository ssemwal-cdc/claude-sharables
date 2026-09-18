---
id: D78
slug: unmapped-subtype-keeps-buttons
kind: decision
status: superseded
date: 2026-09-01
---
# An unmapped subtype keeps buttons

**Superseded by** D91, review-only plugins, on 2026-09-18. Execute mode was retired. The rule returns with it, and the text lives on in `actionable-retired/`.

**Rule.** Strip the record link and the `clear` verdict from an unmapped subtype. Keep its response buttons.

**Outcome protected.** A reviewer keeps live items they can action while a link is fixed.

**Argument.**

This fail-closed is deliberately narrower than the change order one, and the difference is the rule.

A commitment with a missing workflow type risks the click landing on nothing, so the buttons must go.

An unmapped subtype risks the reading only. The gate is per item, and one workflow type covers every custom tool.

Stripping buttons would have cost the user 37 live items to fix a link.

**Evidence.**

- Recorded 2026-09-01 from the run in F97, a second custom tool went unchecked.
- The wider fail-closed is D30, demote a missing wfId.

**Checks.** `test_custom_tool_subtype` pins both halves.
