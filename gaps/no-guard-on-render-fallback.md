---
id: pending
slug: no-guard-on-render-fallback
kind: gap
status: unobserved
date: 2026-09-23
---
# No guard on the render fallback

**Outcome protected.** A verdict the allowlist accepts always reaches its own branch on the dashboard, never the `clear` default.

**Argument.** `itemRow()` branches on `it.verdict` with an `if`/`else if` chain and a bare `else` that renders `clear`.

A reviewer removed the `else if(it.verdict==="tied")` branch as a test.
`validate.py`, `test_skill_code.py` and `shared_blocks.py --check` all stayed green.

The "tied survives publish" test only reads the JSON payload in `index.html`.
It never calls `itemRow()`.
So nothing here would catch a dropped branch, only a manual render check would.

This is the same shape as F98, a missing verdict defaulted to clear.
D63, gate verdicts against publish, covers adding a verdict.
It does not cover one falling back out of the template later.

**Evidence.** Observed 2026-09-23, by removing the `tied` branch and re-running every automated check with none of them failing.

**Checks.** none. Clearing this needs a check that drives the real classifier. Render each allowlisted verdict through `itemRow()`, or an equivalent extracted function. Fail if any verdict lands on the `clear` branch instead of its own.
