---
id: D32
slug: no-data-theme-on-pages
kind: decision
status: settled
date: 2026-08-17
---
# No theme attribute on Pages

**Rule.** Keep a plain colour-scheme media query in the onboarding sheet. Do not add theme-attribute blocks.

**Outcome protected.** The sheet renders correctly on the default system setting.

**Argument.**

The sheet had both halves of the artifact host three-state pattern. A dark theme attribute block, and a guard on the dark media query.

On Pages both are dead, because nothing sets the attribute and there is no toggle to set it.

So they were removed, leaving a plain colour-scheme query and a comment in the file saying why.

The rule mandating all three states is correct for artifacts. This file stopped being one when it moved to Pages.

Do not restore them from that rule.

**Evidence.**

- Removed 2026-08-17.

**Checks.** `check_onboarding_page()` in `scripts/shared_blocks.py` checks the bare root selector.
