---
id: D34
slug: connector-failure-never-empty
kind: decision
status: settled
date: 2026-08-19
---
# A failed call is unknown

**Rule.** Switch a run to the browser route when a connector call errors or returns anything that is not a result set.

**Outcome protected.** A user is never told their approval queue is empty because a call failed.

**Argument.**

The bulk query step is what finds bills pending approval.

So an authentication failure read as no rows reports an empty approval queue, and the user closes the tab believing nothing is waiting.

An error, an authentication challenge, or any non-result-set response means switch that run to the browser route.

That is the same three-state rule as the workflow gate, reached from a different direction.

It is the highest-consequence instance of that rule in either skill.

**Evidence.**

- Recorded 2026-08-19.
- The general rule is D41, three states never a boolean.

**Checks.** none
