---
id: F34
slug: promise-serialised-empty
kind: finding
status: observed
date: 2026-08-15
---
# A returned promise serialises empty

**Outcome protected.** A null result is never read as an empty result.

**Argument.**

An async self-invoking function returned the literal empty object.

The bridge serialised the pending promise before the fetches resolved.

So it is not an empty result. It is a null result, and reading it as everything came back empty would be the same misfile as the rest of these records.

Both skills already use the safe shape. That is a top-level await, and named async functions on the window object that a later call awaits.

That is load-bearing, not style. Do not tidy either into a self-invoking async function.

**Evidence.**

- Observed 2026-08-15.

**Checks.** none
