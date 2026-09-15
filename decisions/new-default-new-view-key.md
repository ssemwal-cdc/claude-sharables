---
id: D39
slug: new-default-new-view-key
kind: decision
status: settled
date: 2026-08-20
---
# A new default needs key

**Rule.** Ship a new view default under a new view key, and migrate the old key rather than discarding it.

**Outcome protected.** A new default reaches the people who have used the toolbar.

**Argument.**

A stored view overrides the default on every load.

So shipping a new default under the old key reaches nobody who has ever touched the toolbar, which is everyone it is for.

Both templates migrate the old key. Filters and search carry across, and only the sort resets.

The marks-key rule is untouched and still absolute. See D38, never rename a marks key.

**Evidence.**

- Both view keys were bumped 2026-08-20 with the newest-first default.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
