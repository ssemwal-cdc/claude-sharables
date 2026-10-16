---
id: D93
slug: main-only-by-pr
kind: decision
status: settled
date: 2026-09-24
---
# Main moves only by pull request

**Rule.** The parent rule git-main-only-by-pr governs this repo. This record adds one argument: the version-bump check needs a pull request. Merge only on the owner's word. D114, no standing merge grant. The merge tool is the only CI check on `main`. D113, no GitHub required checks.

**Outcome protected.** Every release passes the whole build gate, the version-bump check included.

**Argument.**

The bump check diffs a branch against its merge-base with `main`. On a direct push to `main`, the merge-base is HEAD. So the check has nothing to compare, and it skips.

A pull request gives the check a base. Its CI run compares the branch against `main`. A skill that changed without a bump then fails before it ships.

The merge is still a push to `main`. So D9, no version field anywhere, and D79, repo workflow beats org protocol, keep their meaning.

**Evidence.**

- Decided 2026-09-24 by the maintainer.
- A local simulation of a push to `main` skipped the bump check with "no commits ahead of origin/main".

**Checks.** `.github/workflows/validate.yml` runs `scripts/validate.py` on every pull request. `scripts/check_version_bump.py` is the bump check.
