---
id: G28
slug: shared-tree-guard-user-only
kind: gap
status: unobserved
date: 2026-10-15
---
# The shared-tree guard runs only for the owner

**Outcome protected.** No session loses another session's work in a shared checkout.

**Argument.** D115, the parent CLAUDE.md always wins, deleted this repo's own shared-tree hook. The parent guard now refuses the destructive git commands. That guard runs from the owner's user settings. A session without those settings has no guard in this repo. That covers a teammate, a cloud session or a fresh machine.

**Evidence.** Review round 3 of the tidy batch, 2026-10-15, found it. Nobody has seen a session without the guard run here. `unmeasured`.

**Checks.** none
