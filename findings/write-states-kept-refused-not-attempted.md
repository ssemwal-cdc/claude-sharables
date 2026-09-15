---
id: F86
slug: write-states-kept-refused-not-attempted
kind: finding
status: observed
date: 2026-08-27
---
# Three write states

**Outcome protected.** A run that never tried the write says so, instead of reporting a failure.

**Argument.**

A run announced that state would not persist, blamed the cloud-synced folder and the container, and never attempted the write.

Both halves were wrong. Cloud sync refuses deletes and renames, not creates and overwrites, which the first step says two paragraphs above the fallback the run invoked.

And the connected workspace folder is precisely what a Cowork shell can reach. It is the plugin directory that goes missing there. The run inverted a note in the file it was reading.

Every phrase in that message came from the skill file, which is what made it sound authoritative.

The step offered a list of plausible causes that a run can match against before trying, then supplied the exact degradation script. So a run could assemble a confident announcement with the one precondition, an actual attempt, never stated.

The cause list is gone.

Three states were collapsed into two. Kept, refused and not attempted. The state that means nobody looked reported as the state that means it failed.

The step now names all three, ties the session-local fallback to the refused state alone, and requires the write to be read back rather than merely issued.

It forbids inferring the outcome from any property of the folder, and requires a genuine fallback to name the error that refused it.

A claim that state will not persist, with no error in it, is the unreadable defect again.

**Evidence.**

- Observed 2026-08-27, the third such run that day.
- This is the sixth instance of the shape. See D41, three states never a boolean.
- The write has still never been observed failing. See G13, the refused write is unobserved.

**Checks.** `test_step0_write_states` in `scripts/test_skill_code.py`, mutation-tested four ways.
