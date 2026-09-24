---
id: F161
slug: no-guard-on-render-fallback
kind: finding
status: observed
date: 2026-09-24
---
# No guard on the render fallback

**Outcome protected.** A verdict the allowlist accepts always reaches its own branch on the dashboard, never the `clear` default.

**Argument.** `itemRow()` branches on the verdict. Procore uses an `if`/`else if` chain. NetSuite uses a ternary. Both end in a fallback that renders `clear`.

A reviewer once removed the `else if(it.verdict==="tied")` branch as a test.
`validate.py`, `test_skill_code.py` and `shared_blocks.py --check` all stayed green.

The "tied survives publish" test only read the JSON payload in `index.html`.
It never called `itemRow()`.
So nothing there caught a dropped branch. Only a manual render check would.

This was the same shape as F98, a missing verdict defaulted to clear.
D63, gate verdicts against publish, covers adding a verdict.
It did not cover one falling back out of the template later.

What is fixed: `test_verdict_render_guard` reads each plugin's `VERDICTS` constant.
It reads it straight from `publish_dashboard.py`, never a copy.
It renders one item per verdict through the template's real `itemRow()`.
It fails if a non-`clear` verdict's row carries `clear`'s own row class.

**Evidence.** Measured 2026-09-24. The `tied` branch was deleted from the Procore template. The guard went red, 2 of 2 new checks failing. Restored from a `.bak` copy, the guard passed again. The `flagged` branch was broken the same way in the NetSuite template. The guard went red again, 2 of 2 new checks failing. Restored, the guard passed again. 4 of 4 mutations caught.

**Checks.** `scripts/test_skill_code.py::test_verdict_render_guard`.
