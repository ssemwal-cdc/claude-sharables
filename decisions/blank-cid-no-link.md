---
id: D100
slug: blank-cid-no-link
kind: decision
status: settled
date: 2026-10-07
---
# A blank commitment id gives no link

**Rule.** An invoice or CCO with a blank `commitmentId` publishes a WARNING naming its key. Its row shows no link.

**Outcome protected.** No row links to the wrong page.

**Argument.**

The invoice and CCO links carry the commitment id in the path. A blank id leaves an empty segment.

An empty segment opens a page that is not the record. That page looks real.

The same fail-closed rule covers a missing workflow id. See D30, demote a missing workflow id.

**Evidence.**

- Owner ruling, 2026-10-07, from the 2026-10-07 field run.

**Checks.** `test_field_run` in `scripts/test_skill_code.py`.
