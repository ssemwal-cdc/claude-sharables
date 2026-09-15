---
id: pending
slug: write-never-attempted
kind: gap
status: unobserved
date: 2026-08-27
---
# Refused write has no instance

**Outcome protected.** A run never claims a write failed without trying it.

**Argument.** Three runs blamed the platform for a write nobody attempted.
The pattern is stable across three different excuses.
The fix kept landing in the wrong file.

An earlier run wrote to a session path and blamed the never-attach rule.
The truth: `<workspace>` was an undefined placeholder.

On 2026-08-27 one run confirmed the write working, with folders appearing in Downloads.

On 2026-08-27 another run said the connected folder is OneDrive-synced and the container cannot
write there.
The truth: it never attempted the write, and cloud sync refuses deletes, not writes.

**The third run is the instructive one.** It contradicted two things in the file it was reading.
Step 0 says cloud-synced folders refuse deletes and renames while creates and overwrites work.
The 2026-08-15 sandbox note says the connected workspace folder is exactly what is mounted.
The plugin directory is the thing that goes missing.
Every phrase of the run's message came from `SKILL.md`.
`SKILL.md` had listed plausible causes a run could match against before trying.
It then supplied the degradation script verbatim.
That is why the message read as a finding rather than a guess.

**The rule against it existed in the maintainer index, which no run reads.** Step 0 carries it now.
Step 0 names three outcomes.
It ties the session-local fallback to `refused` alone.
It requires the write to be proven by reading it back.
It forbids inferring the outcome from any property of the folder.
It requires a genuine fallback to name the error that refused the write.

**What is still not established: whether the write ever genuinely fails on any surface.**
Two of the three reports were misdiagnoses.
The third was a success.
So `refused` has no confirmed instance at all.
The fallback path is specified and unexercised.
If a run does hit a real refusal, record the error it names, because it would be the first.

**Evidence.** `refused` is guessed, not proven, and has zero instances. `unmeasured`.
Nobody has watched the fallback run.
Do not cite it as established.
The 2026-08-28 stray file was a 6 KB `log.gz.b64` left beside the state file.
`test_step0_write_states()` fails the build if the three outcomes stop being named.
It is mutation-tested four ways.
F‹run-self-banned-login›, a run assembling a refusal from repo prose, is the same shape.

**Checks.** `test_step0_write_states()` in `scripts/test_skill_code.py`.
