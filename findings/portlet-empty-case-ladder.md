---
id: F83
slug: portlet-empty-case-ladder
kind: finding
status: observed
date: 2026-08-27
---
# No portlet found lacked rule

**Outcome protected.** A partial queue is named as partial in the same breath as its count.

**Argument.**

The queue step had a rule for a renamed portlet and nothing for found none.

On an account with no stored portlet setting, the run inspected the home and approvals pages. It found no approval portlets, said so, and published the other types.

Change orders were structurally absent. That step is the only place they can be identified. The transaction table cannot be queried for their pending status.

This was not a regression. The navigation instruction is byte-identical to what it always was. What was missing was the empty case.

The fix is a ladder. Go and look first. Surface what is actually on the dashboard as candidates. Only then ask for a link.

The second rung is the common case, where the portlet exists and its saved-search title simply does not announce itself.

Asking for a URL before enumerating what is there would skip the answer most accounts already have on screen.

The answer is recorded either way, including the answer that there is no such portlet, so it is asked once.

A partial queue is never presented as the whole one. The missing type is named in the same breath as the count, not in a separate note.

**Evidence.**

- Reported from a first run on an account with no stored portlet setting, 2026-08-27.

**Checks.** none
