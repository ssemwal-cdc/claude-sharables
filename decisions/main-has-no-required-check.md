---
id: D113
slug: main-has-no-required-check
kind: decision
status: settled
date: 2026-10-15
---
# The merge tool is the only check on main

**Rule.** Main has no GitHub required checks and no branch protection rule for them. The merge tool is the only gate. CI results still print on each pull request.

**Outcome protected.** One gate holds the merge, so a merge never waits on a second, drifting setting.

**Argument.**

The owner ruled this on 2026-10-15. D93, main moves only by pull request, once said a GitHub ruleset enforces the rule. No read confirms it. D98, claim through the stamp, records that main has no branch protection.

Process-only ruling. It names where the gate lives.

**Evidence.**

- Ruled by the owner on 2026-10-15.
- The GitHub setting is unmeasured from this repo.

**Checks.** none
