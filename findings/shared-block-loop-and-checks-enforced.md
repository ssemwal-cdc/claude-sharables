---
id: pending
slug: shared-block-loop-and-checks-enforced
kind: finding
status: observed
date: 2026-08-24
---
# The shared-block loop ran for real

**Outcome protected.** A claim that used to stand in for a check now runs as a check.

**Argument.** The shared-block loop is now demonstrated rather than argued.
A wording fix belonging to `pub-render-archive` was made in
`plugins/_shared/`.
`--check` failed both plugins for being out of step.
`--sync` pushed the fix into both, and the build went green.
That is the loop working in anger for the first time.
It had been listed as unestablished.

Several claims became enforced checks in the same pass.
`test_skill_code.py` now runs in CI, which it never did while `README.md` said
it would.
`check_onboarding_page()` checks four properties that were asserted as tested
and read by no file.
`check_execute_prompt_purity()` keeps procedure out of the authorising
message.
An unrecognised Procore response verb now fails conservatively on both axes.
It requires a reason, and it counts as affirmative for the no-support caution.
It previously answered false to both.

**Evidence.** Pass dated 2026-08-24, immediately after the audit.
See D58, canonical copy plus a check, the loop demonstrated here.

**Checks.** `scripts/validate.py`, `scripts/test_skill_code.py` in CI,
`scripts/shared_blocks.py`.
