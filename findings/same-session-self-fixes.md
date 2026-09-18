---
id: F116
slug: same-session-self-fixes
kind: finding
status: settled
date: 2026-08-24
---
# Three fixes to that session's own work

**Outcome protected.** A reachability check catches the inequality form of a filter, not
only the equality form.

**Argument.** Three fixes in the audit pass were to things the same session had just
built.

Procore's dashboard still filtered on `verdict !== "gone"` after the bin was
removed.
That filter can exclude nothing, and the prose certified the filter deleted.
The reachability check missed it because its regex matched only `==` and
`===`.
It is widened to catch the inequality form.

`check_template_versions()` read only the first version mention per file.
The verdict allowlist caught a wrong verdict but not a missing one.

**Evidence.** Pass dated 2026-08-24, immediately after the audit.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py`.
