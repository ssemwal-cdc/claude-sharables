---
id: F98
slug: absent-verdict-key-defaulted-clear
kind: finding
status: settled
date: 2026-08-24
---
# A missing verdict defaulted to clear

**Outcome protected.** A missing verdict key fails loud instead of defaulting to an
approvable one.

**Argument.** The verdict allowlist added that same morning caught a wrong verdict.
It did not catch a missing one.
`it.get("verdict", "clear")` defaulted an absent key to `clear` and sailed through the
check.
Procore's sibling code defaulted an absent key to `skipped` instead.

The fix removed the default entirely.
An absent verdict key now aborts the allowlist instead of passing as `clear`.

**Evidence.** Found 2026-08-24, in a nine-agent prose audit of that morning's own fix.

**Checks.** none.
