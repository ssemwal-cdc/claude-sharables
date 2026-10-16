---
id: pending
slug: parent-rules-win
kind: decision
status: settled
date: 2026-10-15
---
# The parent CLAUDE.md always wins

**Rule.** The file `claude-settings/CLAUDE.md` always wins over this repo's text. This repo may be stricter or fill a gap. It may not restate a parent rule. Past owner approvals do not override the parent.

**Outcome protected.** One rule has one home, so two copies never disagree.

**Argument.**

The owner ruled this on 2026-10-15. A sentence that restates a parent rule is deleted. A sentence that adds a domain rule stays.

Process-only ruling.

**Follow-on rulings, 2026-10-15, process-only.**

- Simplified Technical English covers every Markdown file in the repo, `actionable-retired/` included.
- Every record slug is 32 characters or fewer. The slug length check (`check_slug_length`) enforces it.
- The 50 long-named numbered records were deleted and added again as pending records. The stamp keeps a numbered record's key, so a rename is not allowed. Each old number is retired.

**Holes, named.**

- The repo's own shared-tree hook is deleted. The parent guard runs from the owner's user settings, not from this repo. A session without that guard has no shared-tree guard here. That covers a teammate, a cloud session or a fresh machine. The debt is G‹shared-tree-guard-user-only›, the guard runs only for the owner.

**Evidence.**

- Ruled by the owner on 2026-10-15.

**Checks.** none
