---
id: pending
slug: public-repo
kind: decision
status: settled
date: 2026-08-11
---
# Keep this repo public

**Rule.** Keep the repo public. Challenge the argument in this record, never the prose that states the setting.

**Outcome protected.** A teammate installs a plugin and gets every later fix, with no GitHub account and no silent failure.

**Argument.**

Shivam distributes by handing teammates the install commands. He asks them to leave auto sync on.

Public is the only setting where that route needs no GitHub account per teammate. It is also the only setting with no silent update failure.

Org-wide admin sync was considered and rejected. The reasoning is in `README.md` under the distribution heading.

A session that thinks this is stale must argue with the argument above. Do not rewrite the prose that records the setting.

**Evidence.**

- Decided 2026-08-11 with the first two plugins. No measurement of update reach exists, so the no-silent-failure claim is `unmeasured`.
- Because the repo is public, no token and no credential may land here. See D‹shipped-examples-use-placeholders›, worked examples use placeholders.

**Checks.** none
