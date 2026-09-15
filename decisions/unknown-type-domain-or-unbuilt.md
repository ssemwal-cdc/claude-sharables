---
id: D73
slug: unknown-type-domain-or-unbuilt
kind: decision
status: settled
date: 2026-08-28
---
# Out of domain or unbuilt

**Rule.** Ask whether an unknown item type is out of domain or merely unbuilt. Surface a link for the first and name a defect for the second.

**Outcome protected.** A live item in domain gets a procedure instead of a link.

**Argument.**

The unknown-type rule was right and its scope was wrong.

It was written about request and submittal types, which genuinely are outside the skill. A commitment is not outside it. A commitment is the document the invoice and change order checks already tie back to.

So the rule stands and it gained a second branch.

Name an unbuilt type as a defect in the skill, not as a property of the record.

A missing procedure is not something a user can authorise their way out of. Asking implies it is.

The tell that this branch was missing: a run offered the user a choice between authorising a workaround and having the plugin fixed.

**Evidence.**

- The Procore case was reported 2026-08-28. A purchase order contract with a live responder at Financial Analyst Review, due that day, was handed over as a link with no response buttons.
- The NetSuite case was reported 2026-09-01. See F94, NetSuite reviewed a type it could not click.
- The valid type strings are listable. See F35, the tools endpoint needs v2.

**Checks.** `check_execute_type_coverage()` in `scripts/shared_blocks.py`.
