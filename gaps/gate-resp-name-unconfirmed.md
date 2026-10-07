---
id: pending
slug: gate-resp-name-unconfirmed
kind: gap
status: unobserved
date: 2026-10-07
---
# Response name key never seen

**Outcome protected.** A response verb on a row is the real verb, never an object dump.

**Argument.** The gate maps each `available_responses` entry to `(x&&x.name)||String(x)`.
Nobody has read the raw entry shape on a live payload.
The `.name` key is a guess.

To clear it: log one raw entry from a live gate call.
Confirm the key that carries the verb.

**Evidence.** This claim is guessed, not proven.
An entry that is a plain string passes through as it is.

**Checks.** none.
