---
id: D67
slug: queue-source-ask-once
kind: decision
status: settled
date: 2026-08-26
---
# Ask once for the queue

**Rule.** Read the configured queue source before assuming a default. Ask once when a described queue cannot be resolved.

**Outcome protected.** A review runs against the queue the user meant.

**Argument.**

The Procore queue is a fixed endpoint that scopes itself server-side. The NetSuite queue is a user-named portlet on a homepage dashboard.

So NetSuite already had per-user configuration and Procore needed none.

Neither could be told where a queue actually lives. NetSuite took a portlet name, not a link, and Procore took nothing.

The config now carries a URL and a free-text description on both. Both are optional and empty by default, and empty is exactly the old behaviour.

Both queue steps consult it before assuming their default. A declared field that no step reads is worse than no field. So the wiring is the change, not the schema entry.

When a described queue cannot be resolved, ask once. Never substitute the nearest queue found.

A review of the wrong queue looks exactly like a review of the right one.

**Evidence.**

- Landed 2026-08-26 from F80, two audit findings were wrong.
- The found-none case was missing. See F83, no portlet found lacked rule.

**Checks.** none
