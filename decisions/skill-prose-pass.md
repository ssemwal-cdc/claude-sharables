---
id: pending
slug: skill-prose-pass
kind: decision
status: open
date: 2026-09-15
---
# Skill prose pass

**Rule.** Do not rewrite either `SKILL.md` until this decision is taken.

**Outcome protected.** A run reads a short, governed prompt and still meets every safety rule.

**Argument.** The prose pass covered five maintainer and teammate markdown files.
The two `SKILL.md` prompts were held back to their own pass.
Two questions are open.
First, which mandate rules bind a prompt.
Second, whether each prompt splits into a router plus a `references/` folder.
A prompt is read by a model on every run, not by a maintainer looking something up.
So the prose form and engineering rules apply to it.
The chat output shape does not, because skills run in teammate sessions.
See D‹skill-spine-plus-references›, never move safety prose into an on-demand file.

**Options.**

A. Leave both prompts as they are. Record that the mandate does not reach them.

B. Apply the prose form and engineering rules, and split each prompt into a router plus `references/`.

C. Apply the prose rules only. Keep each prompt whole.

**Recommendation.** B.
The prose form and engineering rules bind.
The output shape does not.
Split the prompts.
Keep safety and policy prose in the router.

**Evidence.** Deferred at the interview on 2026-09-15.
The two prompts are about 800 and 660 lines.
About a third of each is dead weight on any given run. `unmeasured`.
`scripts/test_skill_code.py` reads `SKILL.md` by path with no fallback.

**Checks.** none yet. Any split must re-point `scripts/test_skill_code.py` in the same commit.
