---
id: pending
slug: check-registry-with-manifest
kind: decision
status: settled
date: 2026-08-26
---
# Declare checks in a registry

**Rule.** Declare every check with an id, a lens and a capability, and add the id to the manifest in the same edit.

**Outcome protected.** A later lens can select checks by id, and a check cannot vanish unnoticed.

**Argument.**

Each skill verify step opens with a check registry. Each row carries an id, the lens it serves and the capability it needs.

Above a capability table, the registry says what happens when each capability is absent.

The registry is descriptive, not a selector. The `core` lens is the whole table, so a run with no configured lenses does exactly what every earlier run did.

The gate is what makes it worth having. `REGISTRY_MANIFEST` hardcodes every id, so a check that stops being declared fails the build.

Prose is not a gate. A row can vanish in an edit with nothing noticing.

Lenses are checked against a fixed list. Capabilities are checked against the capability table of the skill itself, so a new capability needs no script change.

A capability with no stated absence behaviour is rejected.

Adding a check therefore takes two edits, the row and the manifest entry. That friction is the feature.

**Evidence.**

- Added 2026-08-26. Mutation-tested three ways on the day it landed. Dropping a row, inventing a capability and inventing a lens all fail.
- The absence asymmetry inside it is D‹silent-connector-absence›, silence on an absent connector.

**Checks.** `check_check_registry()` in `scripts/shared_blocks.py`.
