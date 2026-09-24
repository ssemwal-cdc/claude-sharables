---
id: pending
slug: dashboard-empty-context-strip
kind: finding
status: observed
date: 2026-09-24
---
# Dashboard context strip arrives with text

**Outcome protected.** A reviewer sees no blank grey block on a dashboard row.

**Argument.** Both dashboard templates write the `.po` element with a background and padding.
Procore fills `.po` from the item key `context`. NetSuite fills it from `poContext`.
Real queue items arrive with that key filled, not empty.

**Evidence.** Reported 2026-09-24 by the maintainer: real rows arrive with context text.
No blank strip has been seen.
Neither template carries an empty guard on `.po`.
An empty key would still render a grey strip.

**Checks.** none.
