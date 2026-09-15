---
id: pending
slug: connector-needs-second-account
kind: finding
status: observed
date: 2026-08-19
---
# The connector needs another account

**Outcome protected.** A teammate knows whether they were provisioned or not.

**Argument.**

The NetSuite connector needs a separate, Claude-enabled NetSuite account. It is a second account issued on top of the usual login.

A normal NetSuite login is not connector access. People who hold one account assume it is.

If the connector is not listed, they were never provisioned. The route is an email invite from Compass, otherwise IT.

Approvals must still come from their normal account, because that is whose name lands on them.

**Evidence.**

- Stated in `docs/onboarding.html`. Reported by teammates through 2026-08.

**Checks.** none
