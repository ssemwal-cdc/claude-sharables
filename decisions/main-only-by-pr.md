---
id: D93
slug: main-only-by-pr
kind: decision
status: settled
date: 2026-09-24
---
# Main moves only by pull request

**Rule.** Change `main` only by merging a pull request. Never push to `main` directly.

**Outcome protected.** Every release passes the whole build gate, the version-bump check included.

**Argument.**

The bump check diffs a branch against its merge-base with `main`. On a direct push to `main`, the merge-base is HEAD. So the check has nothing to compare, and it skips.

A pull request gives the check a base. Its CI run compares the branch against `main`. A skill that changed without a bump then fails before it ships.

The merge is still a push to `main`. So D9, no version field anywhere, and D79, repo workflow beats org protocol, keep their meaning.

The other option was to diff a direct push against the commit before it. The maintainer chose pull requests instead.

**Evidence.**

- Decided 2026-09-24 by the maintainer.
- A local simulation of a push to `main` skipped the bump check with "no commits ahead of origin/main".
- Branch protection is a GitHub setting, outside this repo. Whether it is on is `unmeasured` here.

**Checks.** `.github/workflows/validate.yml` runs `scripts/validate.py` on every pull request. Branch protection on GitHub enforces the rule itself.
