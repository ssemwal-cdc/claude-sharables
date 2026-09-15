---
id: pending
slug: frontmatter-name-description-only
kind: decision
status: settled
date: 2026-08-11
---
# Frontmatter is name and description

**Rule.** Give a skill frontmatter a `name` and a `description` only. Never trim the description.

**Outcome protected.** A skill fires when a teammate describes the job it does.

**Argument.**

The description carries the trigger phrases. It is what decides whether the skill fires.

So it is long and specific on purpose.

Do not trim it for tidiness.

Its start also carries the version marker. See D‹skill-version-lines›, four synced version sites.

**Evidence.**

- Both shipped skills follow this shape.

**Checks.** `scripts/validate.py` asserts the frontmatter name equals the skill folder name.
