---
id: G18
slug: dashboard-empty-context-strip
kind: gap
status: unobserved
date: 2026-09-15
---
# Empty context strip unobserved

**Outcome protected.** A reviewer sees no blank grey block on a dashboard row.

**Argument.**

Both dashboard templates write the `.po` element with a background and padding. Neither has an empty guard. A row with no context text renders an empty grey strip.

Procore fills `.po` from the item key `context`. NetSuite fills it from `poContext`.

Whether a real item arrives with that key empty is `unmeasured`. The fixtures leave it empty in all 18 captures.

Fix only if a real queue shows it. The fix bumps the template version and both skills.

**Evidence.**

- Seen 2026-09-15 in the first device-capture run. `F99, device shots first run`.
- 0 of 18 captures came from a real queue.

**Checks.** none
