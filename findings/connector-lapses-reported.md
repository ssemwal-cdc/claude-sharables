---
id: F38
slug: connector-lapses-reported
kind: finding
status: observed
date: 2026-08-19
---
# The lapse cadence is reported

**Outcome protected.** A teammate files a lapsed connector as normal, not as a plugin bug.

**Argument.**

The connector lapses every few days, and the sheet says so up front.

Two things about that are deliberate. The cadence is reported, not measured. Nobody here has timed the session lifetime, so the sheet says every few days and never a number.

And it is framed as how the connector behaves generally, not as something these plugins cause. Otherwise the person hitting it files it as a plugin bug.

It pairs with the third-state rule. The run says it once, then carries on through the browser. What lapses is the cross-check, not the review.

**Evidence.**

- Added 2026-08-19 from teammate feedback. The session lifetime is `unmeasured`.
- The say-once rule is D36, say a stale session once.

**Checks.** none
