---
id: F91
slug: a-wrong-run-found-four-defects
kind: finding
status: observed
date: 2026-09-01
---
# A wrong run found defects

**Outcome protected.** A run is judged claim by claim, not accepted or dismissed whole.

**Argument.**

The run that broke the render rule did four things right. That bears on how much to trust the rest of it.

It cross-checked the gate against the live user interface before believing it. It clicked nothing.

It named the error that refused each write. It reported the stale template rather than working around it.

It reported its own divergence from the render step instead of presenting the file as the deliverable.

Four of the findings from that run are ones this repo could not have produced on its own.

A run can be wrong about one thing and be the reason four others got fixed.

**Evidence.**

- Observed 2026-09-01. The four findings are the 55 KB template floor and the cloud-placeholder open error. The other two are the second custom tool and the duration field read as a cost.
- The rule it broke is D77, render first, believe the guard.
- The template floor is in F96, read-side wall, fixed by serialise.
- The placeholder error is in F92, a dehydrated file needs rename-over.
- The tool and field findings are in F97, second custom tool unchecked.

**Checks.** none
