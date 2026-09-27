---
id: D3
slug: frontmatter-name-description-only
kind: decision
status: settled
date: 2026-08-11
---
# Frontmatter is name and description

**Rule.** Give a skill frontmatter a `name` and a `description` only. Never drop a trigger phrase. Keep the description within the installer limits: 1024 chars for a skill description, 500 for a plugin description. `scripts/validate.py` enforces both.

**Outcome protected.** A skill fires when a teammate describes the job it does.

**Argument.**

The description carries the trigger phrases. It is what decides whether the skill fires.

So it is specific on purpose, never trimmed of a trigger phrase for tidiness.

But it must fit the installer's own limits. Past that limit, the install is rejected and the skill never fires.

Its start also carries the version marker. See D43, four synced version sites.

**2026-09-27.** The owner amended this decision. The installer rejected both plugins. Two skill descriptions exceeded 1024 chars. One plugin description exceeded 500. "Never trim" had grown the text past the installer's limit. The fix rewrites for length. It keeps every trigger phrase. `validate.py` now gates the limit so this cannot recur silently.

**Evidence.**

- Both shipped skills follow this shape.
- 2026-09-27: install rejection on both plugins. NetSuite skill description measured 1128 chars. Procore skill description measured 1139. Procore plugin description measured 558.

**Checks.** `scripts/validate.py` asserts the frontmatter name equals the skill folder name.
