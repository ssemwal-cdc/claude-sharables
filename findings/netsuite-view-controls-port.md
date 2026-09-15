---
id: F40
slug: netsuite-view-controls-port
kind: finding
status: observed
date: 2026-08-19
---
# NetSuite got the Procore toolbar

**Outcome protected.** Both dashboards sort, filter and search the same way.

**Argument.**

A teammate asked why the NetSuite dashboard did not sort while the Procore one filtered.

It had no view controls at all. It had a hardcoded sort by verdict and nothing else.

So the Procore toolbar was ported across, with identical names and idiom, so the two templates stay diffable.

NetSuite has no campus or building, so its axes are type and vendor. Vendor narrows to the chosen type, the way the Procore buildings narrow to campus.

Sort, search and a reset control came with it.

**Evidence.**

- Asked 2026-08-19.
- One rule in that port is load-bearing. See D46, the execute bar ignores the filter.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
