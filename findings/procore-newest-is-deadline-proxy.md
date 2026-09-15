---
id: F44
slug: procore-newest-is-deadline-proxy
kind: finding
status: observed
date: 2026-08-20
---
# Procore newest is a proxy

**Outcome protected.** Nobody reads a Procore deadline as an origin date.

**Argument.**

Newest means different things on the two dashboards.

NetSuite sorts on the transaction date, a real document date, with the internal id descending as the same-day tiebreak.

Procore has no creation date anywhere in its pipeline. Its only per-item date is the workflow step deadline.

So newest first there is latest deadline first. It is labelled as such so nobody reads it as an origin date.

Adding a real creation date means adding it to the record reads, the log schema and the publish script together. Do not relabel without doing that.

**Evidence.**

- Recorded 2026-08-20.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
