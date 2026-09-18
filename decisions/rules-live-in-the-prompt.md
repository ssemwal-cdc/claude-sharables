---
id: D71
slug: rules-live-in-the-prompt
kind: decision
status: settled
date: 2026-08-27
---
# Run rules live in prompts

**Rule.** Write any rule about what a run may claim into the `SKILL.md` the run reads.

**Outcome protected.** A rule that would stop a bad claim is in front of the run making it.

**Argument.**

The rule that would have caught the never-attempted write existed in the
maintainer notes. The running skill cannot see that file.

Maintainer prose is not a prompt. The skill file is the prompt.

That is the transferable lesson. A rule about what a run may claim has to be in the file the run reads.

A check then fails the build if the rule stops being stated.

**Evidence.**

- Recorded 2026-08-27 from F86, three write states.
- The same shape recurred with the login rung. See
  `F135`, a run banned itself from login.

**Checks.** `test_step0_write_states` and `test_login_states` in `scripts/test_skill_code.py`.
