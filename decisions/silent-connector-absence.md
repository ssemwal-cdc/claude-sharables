---
id: pending
slug: silent-connector-absence
kind: decision
status: settled
date: 2026-08-26
---
# Silence on an absent connector

**Rule.** Skip the connector checks in silence when the connector is absent. Name the outcome when an attachment is missing.

**Outcome protected.** A reader is told about every absence they can act on, and about no absence they cannot.

**Argument.**

This is a named exception to the global rule that an item is never dropped without saying so. The exception is narrow and it is argued, not assumed.

A missing attachment skips the item and names the outcome. A missing connector skips the connector step and says nothing at all.

The two look inconsistent and are not. A caveat nobody can act on is an apology on a loop. The connector needs a separate provisioned account, so an unprovisioned reader cannot fix it this run.

Naming is right for an attachment because the word unreadable once hid whole file formats going unread.

The general form: a capability the user chose not to have is informative. A capability they cannot obtain is an apology.

The exception covers the never-provisioned case only. An expired session is a third state and is named once. See D‹stale-connector-said-once›, say a stale session once.

Any future lens that reports a check as not run inherits this split.

**Evidence.**

- Recorded 2026-08-26 with the check registry. Both skill registries state the split.
- Reaffirmed in the 2026-09-15 interview as decision 3. The silence is kept and recorded as an exception with its argument attached.
- The reader benefit of silence is `unmeasured`. No run has been timed with and without the caveat.

**Checks.** `check_check_registry()` in `scripts/shared_blocks.py` asserts every capability states an absence behaviour.
