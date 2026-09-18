---
id: pending
slug: onboarding-check-silent-on-missing-file
kind: finding
status: observed
date: 2026-09-18
---
# The onboarding page check passed on a missing file

**Outcome protected.** A missing `docs/onboarding.html` fails the build, per
`D‹markdown-compliance-fix-plan›`, the markdown compliance fix plan,
ruling 3.

**Argument.**

`scripts/shared_blocks.py`'s `check_onboarding_page()` returned an empty
problem list whenever `docs/onboarding.html` did not exist. `validate.py`
treats an empty list as success. So a deleted or unmerged onboarding page
would ship clean.

This is the fail-open shape `validate.py`'s own comments call out for a
missing check. The file is load-bearing. GitHub Pages serves it verbatim,
and `README.md` links straight to it.

**Evidence.**

- Observed 2026-09-18, reading `check_onboarding_page()` at the point this
  lane started.
- Mutation-tested 2026-09-18: renaming `docs/onboarding.html` away made the
  fixed check fail, and putting it back made the check pass again.

**Checks.** `scripts/shared_blocks.py`'s `check_onboarding_page()` now
returns a failure instead of `[]` when the file is missing.
