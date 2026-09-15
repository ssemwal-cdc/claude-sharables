---
id: pending
slug: permission-mode-unreadable
kind: finding
status: settled
date: 2026-08-15
---
# Four rounds, no bug

**Outcome protected.** A permission question converges in one round instead of four.

**Argument.** A `javascript_tool` call was reported blocked.
Four rounds of probes followed.
Two wrong versions of a maintainer note followed.
An onboarding section was written and then deleted unshipped.
The actual answer: the run had been in skip-all rather than auto.
Nothing was ever wrong.
Three things made it expensive, and only the first is about permissions.

**The mode was reported from memory, and no tool can check it.**
An agent cannot read its own permission mode, because no tool returns it.
So the single fact the whole investigation turned on was unverifiable by the agent.
Only the person at the keyboard could record it, in the moment, and it was misremembered.
Capture the mode at the moment of the run.
Everything converged within one run of pinning it down, and nothing converged before.

**A diagnostic was treated as evidence about the workflow.**
The denied probe fetched five URLs across four CDNs.
Both skills only ever fetch cdnjs.
Two successive theories were built by generalising from a shape the real thing never takes.
The first was that auto mode blocks the fetch.
The second was that the classifier objects to the host list.

**A confounded comparison looked like a result.**
The before and after runs differed in the settings and in the host list.
The after run was read as proof the settings fixed it.
The user's own instinct to re-run the control is what caught it.
Change one variable, or the comparison says nothing.

**What went right is worth keeping.** The onboarding section reached the branch and never `main`.
The commit that added it carried the unresolved confound in its own message.
Writing the doubt down at the moment of committing stopped a fabricated step shipping to teammates.

**Evidence.** Dated 2026-08-15.
Four rounds of probes, two wrong note versions, one deleted onboarding section.
The probe fetched five URLs across four CDNs.
The permission mode of any past run is unrecordable after the fact. `unmeasured`.

**Checks.** none.
