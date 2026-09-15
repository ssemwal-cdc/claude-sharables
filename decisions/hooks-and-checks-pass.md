---
id: D82
slug: hooks-and-checks-pass
kind: decision
status: open
date: 2026-09-15
---
# Hooks and checks pass

**Rule.** Turn each prose rule into a hook or a check once the prose pass has landed.

**Outcome protected.** A rule is enforced by a command, not by a maintainer remembering it.

**Argument.** The mandate says a file is the fallback, not the enforcement.
Today nothing enforces the prose rules.
Two candidate mechanisms exist.
The first is `.claude/settings.json` hooks, which refuse a forbidden command before it runs.
The second is widening `scripts/validate.py` with prose-only rules.
Prose-only rules include a sentence-length ceiling, a required frontmatter block and a citation form.
Doing this before the prose pass lands would gate files that are mid-rewrite.

**Options.**

A. Do nothing. Keep the mandate as a document.

B. Install the hooks and widen `validate.py`, after the prose pass lands.

C. Install the hooks now and widen `validate.py` later.

**Recommendation.** B.
The prose pass changes every file the new checks would read.
Landing the checks first fails the build on work in progress.

**Evidence.** Deferred at the interview on 2026-09-15.
`scripts/validate.py` checks 2 of about 28 published strings today.
No hook exists in this repo. The count is zero.
The mandate asks for a hook that refuses `git stash`, `git reset`, `git checkout <path>` and `git restore`.

**Checks.** none yet. This decision creates them.
