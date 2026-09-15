---
id: pending
slug: no-stray-files-in-workspace
kind: decision
status: settled
date: 2026-08-28
---
# No stray files in workspace

**Rule.** Let only the files the skill steps name exist in the workspace folder. Write each destination file whole.

**Outcome protected.** Nobody is handed a cleanup chore in a folder that refuses deletes.

**Argument.**

The rule states a property. The mechanisms are examples under it.

Anything the steps do not name is a stray, whatever its purpose. Staging a file to move bytes in or out is forbidden by name.

The alternative is stated rather than implied. Write the destination file itself, whole, with the file tools.

Where that genuinely cannot be done, the outcome is refused and it takes the one-line report.

The reason the rule is a property and not a list is F‹prohibition-list-let-a-stray-through›, a list let a stray through.

A run once invented a to-delete folder and asked the user to empty it. That folder appears nowhere in this repo.

The rule already existed in two places and had never been stated for the first step. The publish script survives a refused move, and the render archive is a fixed set of weekday slots overwritten in place.

That archive is fixed precisely because anything that accumulates can never be cleaned up.

The mechanism behind the refused deletes was never established. The fix does not depend on knowing it, because nothing is created that would need removing.

**Evidence.**

- Stated as a property 2026-08-28. Stated as mechanisms 2026-08-27, which failed.
- One workable write on a cloud mount is a rename over a placeholder. See F‹dehydrated-onedrive-rename-over›, a dehydrated file needs rename-over.

**Checks.** `test_step0_write_states` in `scripts/test_skill_code.py`, mutation-tested.
