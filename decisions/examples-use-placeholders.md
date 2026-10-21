---
id: D112
slug: examples-use-placeholders
kind: decision
status: settled
date: 2026-08-24
---
# Shipped examples use placeholders

**Rule.** Use placeholders in every shipped worked example. That covers a counterparty name, a project label, a real amount, a token and a credential. A tool id, a custom-field number or the company id may appear, but only as an observed example. Ids differ per company, so a skill maps them again on each run.

**Outcome protected.** Nothing a teammate copies carries customer data into a public repo.

**Argument.**

No token and no credential may land in this repo, ever. If a ported skill carries any, stop and raise it before committing.

The shipped worked examples are the config blocks and log schemas a teammate copies. They use placeholders only.

They carry no counterparty name, no project label, no real amount, no token and no credential.

A tool id, a custom-field number and the company id are low-sensitivity. Owner ruling, 2026-10-21, process-only. They may appear in shipped text as an observed example. A skill never treats one as fixed: it maps the ids on each run.

Defect provenance is the other case and the rule differs. See D57, provenance may cite ids.

Anything genuinely confidential belongs in neither category and does not go here at all. That covers a rate, a contract term and a person details.

**Evidence.**

- Owner ruling, 2026-10-21: tool ids, custom-field numbers and the company id may ship as observed examples. Counterparty names, project labels, real amounts, tokens and credentials stay out.
- Sanitised 2026-08-24. Before that both skills shipped a real company id, a real tool id and 3 custom-field ids. They also shipped a named subcontractor and a real commitment balance.
- `README.md` claimed at the same time that the plugins carried no customer data.
- The repo is public by decision. See D13, keep this repo public.

**Checks.** none. No script greps shipped examples for live values.
