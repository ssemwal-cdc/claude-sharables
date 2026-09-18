---
id: pending
slug: nine-agent-audit-corrected-four-claims
kind: finding
status: observed
date: 2026-08-24
---
# Interview corrected four audit claims

**Outcome protected.** A maintainer interview catches an auditor's wrong premise before it
ships as a rule.

**Argument.** Five auditors read the whole prose corpus cold.
They had none of the session's conclusions and did not read git history.
Three debaters then contested the pooled findings, as defence, prosecution and adjudication.
The maintainer interview corrected four of the panel's own assumptions.

First, the panel asked whether NetSuite change orders should be executable at all.
The maintainer had conflated Procore's CCO gate, already resolved, with NetSuite's own change orders.
NetSuite change orders carry no approval status and no next approver.
So they cannot be gated or confirmed that way.
The two systems used the same word for different things, and the docs now
separate them.

Second, the maintainer reported that browser-mode execute works through Claude in Chrome.
That is a user report, not an observed run.
It answers a narrower question than the panel asked.
Clicks landing is not the gate running.

Third, the maintainer believed the repo was enterprise-private.
The GitHub API says otherwise.
The sensitivity judgment is the maintainer's to make.
Its premise was checkable, and wrong.

Fourth, the precedence question resolved on two facts no auditor could have known.
Execute is always pressed in the session that ran the review.
The run is not watched.

Auditors reason from the documents, and the documents are not the system.
That is why the interview existed.

**Evidence.** Audit dated 2026-08-24.
122 raw findings, 29 surviving contest.
The GitHub API reported `"private": false`, `"visibility": "public"`, forkable, personal account.
See `D13`, public is a decision.

**Checks.** none.
