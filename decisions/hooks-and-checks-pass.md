---
id: D82
slug: hooks-and-checks-pass
kind: decision
status: settled
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

**Chosen.** B, taken on 2026-09-15 after the prose pass landed at `3a63144`.
The hook and the five checks landed in the same pass.

**Evidence.** Deferred at the interview on 2026-09-15.
`scripts/validate.py` checked 2 of about 28 published strings before this pass.
No hook existed in this repo. The count was zero.
The mandate asks for a hook that refuses `git stash`, `git reset`, `git checkout <path>` and `git restore`.
Every check below went red on the defect it guards before it was trusted.
See `F100`, the mutation results.

**Checks.**

- `.claude/settings.json` denies the two NetSuite write tools. It also runs the hook below before every Bash call.
- `scripts/refuse_shared_tree.sh` refuses `git stash`, `git reset`, `git restore`, a `git checkout` that names a path, `pkill -f` and `lsof -t`. A bare branch name passes.
- `check_frontmatter` reads every record. It asserts the five keys, the slug, the kind, the status, the date, a unique id, an H1 and an outcome line.
- `check_citations` asserts that every citation resolves and carries a gloss. It refuses a path citation.
- `check_index_fresh` regenerates each `_index.md` from frontmatter and refuses a stale file.
- `check_index_size` holds `CLAUDE.md` at 150 lines or fewer, naming both plugins.
- `check_sentence_length` refuses a sentence over 30 words in the index, the three READMEs and every record.
- `scripts/validate.py` calls the five checks, so they gate the build and CI.
