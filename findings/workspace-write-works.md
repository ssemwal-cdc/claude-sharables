---
id: pending
slug: workspace-write-works
kind: finding
status: observed
date: 2026-08-27
---
# The workspace write works

**Outcome protected.** State persists between runs, so first-run setup is asked once.

**Argument.**

The folders are created and the log persists. The folder appears in Downloads.

An earlier run wrote to a session path and blamed the never-attach rule. It was resolving an undefined placeholder, not hitting a surface limit.

So the fix was defining the placeholder, and attempting the write is now the stated rule.

Do not re-diagnose this as a platform constraint without a fresh observation.

**Evidence.**

- Confirmed 2026-08-27, after the workspace placeholder was defined.
- It was re-diagnosed wrongly a third time the same day. See F‹write-states-kept-refused-not-attempted›, three write states.

**Checks.** `test_step0_write_states` in `scripts/test_skill_code.py`.
