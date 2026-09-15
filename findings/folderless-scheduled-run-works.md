---
id: F77
slug: folderless-scheduled-run-works
kind: finding
status: observed
date: 2026-08-26
---
# Folderless scheduled run works

**Outcome protected.** A teammate schedules a run without first choosing a folder.

**Argument.** A scheduled run with no folder connected works.
The schedule was set to automatic and the computer was left on.
The run went through onboarding by itself.
The run did not stall for answers.
Nothing was written to `Documents/Claude`, so that candidate path is dead.
The per-session storage explanation stands.
Two claims in `docs/onboarding.html` were falsified and pulled.
The first claim said a folderless scheduled run does not work at all.
The second claim said connecting Downloads before scheduling is not optional.
Both were derived from the shipped prompt text, not observed.
The mild version survives and is true by construction.
With nothing persisted the idempotency gate cannot trip.
Every fire time then repeats the whole review.
Later fire times do not stand down.
That is waste, not danger.
The review is read-only.
Execute still needs an explicit per-item instruction.
The sheet recommends Downloads rather than requiring it.
Do not point the state file at a stable path instead.
The motivating problem was folderless scheduling failing, and it does not fail.
The remaining cost is a repeated review, which a connected folder already fixes.
See G11, unattended Step 0 identity branch.

**Evidence.** 2026-08-26, third maintainer correction of that day.
One reported run, no transcript.
The repeat-review cost is `unmeasured`.
The shipped scheduled prompt reads `_netsuite_review_log.json` and stops when `lastCompletedRun` is today.
Its own fallback treats a missing or unreadable file as no run today.

**Checks.** none.
