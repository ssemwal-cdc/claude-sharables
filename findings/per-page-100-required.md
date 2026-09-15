---
id: pending
slug: per-page-100-required
kind: finding
status: observed
date: 2026-08-15
---
# Workflow queries need per_page

**Outcome protected.** A live workflow instance is found instead of skipped.

**Argument.**

A page size of 100 is required on the workflow instances endpoint.

On the default page size the endpoint hid live instances outright.

The likely mechanism is that the page window is applied before the filters, so on a project with many instances the filtered one is not on page 1.

It now rides on every gate query, for every item type.

It matters because an empty response becomes an empty state, and an empty state means skip the item.

**Evidence.**

- Observed 2026-08-15. The mechanism is inferred, not read from the API, so it is `unmeasured`.

**Checks.** none
