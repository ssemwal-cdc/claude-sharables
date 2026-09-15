---
id: pending
slug: shipped-examples-use-placeholders
kind: decision
status: settled
date: 2026-08-24
---
# Shipped examples use placeholders

**Rule.** Use placeholders in every shipped worked example. Never ship a live value.

**Outcome protected.** Nothing a teammate copies carries customer data into a public repo.

**Argument.**

No token and no credential may land in this repo, ever. If a ported skill carries any, stop and raise it before committing.

The shipped worked examples are the config blocks and log schemas a teammate copies. They use placeholders only.

That means no tenant or company id, no custom-field id, no counterparty name, no project label and no real amount.

Defect provenance is the other case and the rule differs. See D‹provenance-ids-allowed›, provenance may cite ids.

Anything genuinely confidential belongs in neither category and does not go here at all. That covers a rate, a contract term and a person details.

**Evidence.**

- Sanitised 2026-08-24. Before that both skills shipped a real company id, a real tool id, 3 custom-field ids, a named subcontractor and a real commitment balance.
- `README.md` claimed at the same time that the plugins carried no customer data.
- The repo is public by decision. See D‹public-repo›, keep this repo public.

**Checks.** none. No script greps shipped examples for live values.
