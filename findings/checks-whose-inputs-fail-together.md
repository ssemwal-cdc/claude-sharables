---
id: F101
slug: checks-whose-inputs-fail-together
kind: finding
status: observed
date: 2026-08-24
---
# Some checks fail together with their inputs

**Outcome protected.** A freshness check keeps one input that cannot go stale.

**Argument.** A check whose two inputs fail together cannot detect that failure.
Any freshness check needs one input that cannot go stale.

This is the same family as the connector-lag rule, verify the record, not the
queue. That is because the queue lags with it.
It is the same family as the CCO wrong-id case, where a 200-empty response
looks like no instance.

**Evidence.** Found 2026-08-24, generalised from
`F126`, the version check blind to
lockstep.

**Checks.** none.
