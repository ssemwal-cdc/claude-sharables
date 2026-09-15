---
id: pending
slug: cco-read-before-gate
kind: decision
status: settled
date: 2026-08-14
---
# Read a CCO before gating

**Rule.** Read a commitment change order before gating it. Gate every other item type first.

**Outcome protected.** A change order is gated at all, instead of rendering ungated for everyone.

**Argument.**

Every other item type is gated first, so the fan-out can discard the noise cheaply.

Inverting that for one type looks like an inconsistency to tidy up. It is not.

The read is what produces the lookup id, so a change order cannot be gated before it is read.

The wasted reads are bounded by the change order count, which is small. The alternative is no gate at all.

**Evidence.**

- Recorded 2026-08-14 with F‹cco-holder-id-route›, a CCO workflow hangs off holder.id.
- The change order share of a queue is `unmeasured` beyond being described as small.
- The verbs follow the workflow step. See F‹cco-verbs-follow-step›, CCO verbs follow the step.

**Checks.** none
