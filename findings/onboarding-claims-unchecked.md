---
id: F63
slug: onboarding-claims-unchecked
kind: finding
status: observed
date: 2026-08-24
---
# Four claimed tests were absent

**Outcome protected.** Every claim about the onboarding sheet has a reader or is deleted.

**Argument.**

The notes described assertions about chip rows, paragraph placement and mutation checks over the onboarding sheet.

No file in the repo read that path. So no test asserted any of the four claims, and the claims are gone.

What is genuinely checkable without a browser is now checked. The file decodes as UTF-8, carries a doctype and a character-set meta tag, closes its root element, and defines every custom property it uses on a bare root selector.

Anything visual still needs a person to look. Do not add assertions about paragraph placement, which is what the deleted claims tried to do.

**Evidence.**

- Found 2026-08-24. Four claims, zero readers.
- This is the second time these records claimed coverage that did not exist. The first is in D46, the bar ignores filters.

**Checks.** `check_onboarding_page()` in `scripts/shared_blocks.py`.
