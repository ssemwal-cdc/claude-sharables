---
id: D53
slug: not-shared-per-domain
kind: decision
status: settled
date: 2026-08-24
---
# Never share per-domain machinery

**Rule.** Leave genuinely per-domain content out of shared blocks.

**Outcome protected.** Each plugin keeps the filter axes, date format and URL shapes its own system needs.

**Argument.**

Some machinery differs for real reasons and must not be forced into a block to raise the sharing percentage.

NetSuite filters on type and vendor. Procore filters on campus, building and type.

NetSuite parses month-day-year dates. Procore parses ISO dates.

NetSuite has three fixed buttons. Procore reads its verbs from the workflow step.

The record URL shapes differ per system.

**Evidence.**

- Recorded 2026-08-24 with D58, sync shared blocks from canonical.

**Checks.** none
