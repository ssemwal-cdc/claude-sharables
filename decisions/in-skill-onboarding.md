---
id: pending
slug: in-skill-onboarding
kind: decision
status: settled
date: 2026-09-25
---
# Onboarding lives in the skill

**Rule.** The skill onboards a new user on its first run. The teammate sheet is retired to a stub.

1. **Prerequisites.** At the start of a first run, check that Claude in Chrome tools are present. If they are absent, tell the user to install Claude in Chrome and sign in to the system, then stop.
2. **Setup advice, once.** On a first run, say in a few lines what works best: the latest Opus model, medium to high effort, and Cowork with the Downloads folder connected. Name only the items the run can see are off. The model is readable. The mode is read from the tools present. Effort is not readable, so state it as advice.
3. **Schedule offer.** After a successful first run, where a scheduling tool is present, offer a daily schedule. Ask for the first time, the retries and weekdays or all days. Create the task with the prompt in `assets/scheduled_prompt.md`, verbatim. Where no scheduling tool is present, say where to set one up and show the prompt path.
4. **One home for the prompt.** Each plugin ships `skills/<skill>/assets/scheduled_prompt.md`. It is the only copy. The prompt restates no skill rule.
5. **Sheet.** `docs/onboarding.html` becomes a short stub: install the plugin, then ask for a review. It carries no setup steps and no prompt.

**Outcome protected.** A new user who only installs the plugin reaches a working review and a working schedule without reading anything else. A scheduled task never runs a prompt that drifted from the skill.

**Argument.**
The owner chose this on 2026-09-25. Adding a plugin is now common knowledge, so the sheet's remaining value was setup advice and the schedule prompt.
The sheet copy of the schedule prompt drifted from the skill. A task carrying that copy stopped a run that the skill would have finished in browser mode.
Moving both into the plugin removes the second copy.

**Supersedes.** D33, the page is the file. D59, no terminal commands in sheet. D32, no theme attribute on Pages, applies only while the stub exists. D31, the docs folder is public, still applies.
