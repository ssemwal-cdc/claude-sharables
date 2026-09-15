---
id: F21
slug: fanout-three-states-cap
kind: finding
status: observed
date: 2026-08-14
---
# The fan-out caps concurrency

**Outcome protected.** A blip during a fan-out is named, not counted as an item with nothing to do.

**Argument.**

Both skills fan out their reads now, and the fan-out has one failure mode that governs the whole design.

The Procore gate used to issue one request per queue item, most of them only to learn the item was noise. NetSuite re-read each record page when the bulk query already carried most of those fields.

The dominant cost in both was round trips, not the size of any one response.

Turning sequential requests into concurrent ones changes what a failure looks like.

A request that fails and returns nothing is indistinguishable from an item with no workflow instance, which both skills define as already actioned elsewhere.

So a blip silently suppresses a live item and logs it as done, plurally and quietly. That is the same bug class as a change order resolving to the wrong workflow id.

Hence every fan-out returns three states per item, and a failure is named and excluded rather than folded into the suppressed count.

A rate-limit response is a failure, not an empty result. That is why concurrency is capped rather than let rip.

**Evidence.**

- Recorded 2026-08-14. The Procore queue was about 73 items, about 41 of them noise.
- Concurrency is capped at 8 to 10. The cap was chosen against the rate limit, which is `unmeasured`.
- The rule is D41, three states never a boolean.

**Checks.** `scripts/test_skill_code.py` runs the three-state fan-out, mutation-tested.
