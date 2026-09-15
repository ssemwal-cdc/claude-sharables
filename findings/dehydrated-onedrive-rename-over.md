---
id: F92
slug: dehydrated-onedrive-rename-over
kind: finding
status: observed
date: 2026-09-01
---
# A dehydrated file needs rename-over

**Outcome protected.** A run on a cloud mount can still write its state file.

**Argument.**

Every pre-existing file in the workspace folder was a cloud-only placeholder. Opening one returned an EINVAL error.

So the file was unreadable and unwritable. Writing a new name and renaming it over the placeholder succeeded.

That is the opposite way round from what the overwrite-in-place rule expects.

Stating the rule as a property rather than a list of mechanisms is what made this resolvable. A write that lands on the destination and leaves nothing beside it satisfies the rule, whatever sequence got it there.

What stays forbidden is a file staged to move bytes.

Had the rule still been the mechanism list, the only working write on that mount would have been against the rules.

**Evidence.**

- Observed 2026-09-01.
- The property form is D72, no stray files in the workspace.

**Checks.** `test_step0_write_states` in `scripts/test_skill_code.py`.
