---
id: pending
slug: one-pin-per-plugin
kind: decision
status: settled
date: 2026-11-11
---
# One pin per plugin

**Rule.** A plugin's dashboard shells carry one pin: one commit sha, with the same `sha384` rule on every tag. `--pin` writes one sha into every shell, so one run of `--pin` meets the rule.

**Outcome protected.** A reviewer checks one commit per plugin. The plugin's dashboard code is one reviewed state.

**Argument.**

The check does not enforce this. It verifies each tag on its own and does not count shas. A shell whose two tags name two valid shas would pass the check.

Only `--pin` keeps the sha uniform. A check that counted shas per plugin would close the gap.

**Evidence.**

- Read of `check_asset_pins` in `scripts/shared_blocks.py`, 2026-11-11: each tag is checked alone.
- Read of `pin_templates` in the same file: one sha is written into every pinned tag.

**Checks.** none. The check verifies each tag alone.

Kind: process
Home: scripts/shared_blocks.py
