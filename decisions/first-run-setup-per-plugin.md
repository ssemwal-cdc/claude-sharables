---
id: pending
slug: first-run-setup-per-plugin
kind: decision
status: settled
date: 2026-08-11
---
# First-run setup is per plugin

**Rule.** Ask the user to confirm the identifiers that differ per person or per company, and store them in the state file.

**Outcome protected.** A second run asks nothing and reviews immediately.

**Argument.**

Each plugin asks its own setup questions, because the identifiers differ per person and per company.

The answers live in the state file in the workspace folder.

That is why the folder is declared rather than chosen. See D‹workspace-folder-downloads›, declare the workspace folder Downloads.

A declared field that no step reads is worse than no field, so every stored key must be read by a step.

**Evidence.**

- Both plugins follow this shape.
- One stored field was written and never read. See F‹two-custom-tools-unchecked›, second custom tool unchecked.

**Checks.** none
