---
id: pending
slug: shipped-examples-now-placeholders
kind: finding
status: settled
date: 2026-08-24
---
# Shipped examples now use placeholders

**Outcome protected.** A teammate cannot copy a live value out of a shipped example.

**Argument.** Every live value a teammate could copy is a placeholder now.
Those were a company id, a tool id, three custom-field ids and a named
subcontractor.
They also included a project label, a commitment balance, and real bill and
purchase order numbers.
`README.md` no longer claims the plugins carry no customer data while carrying
some.

Defect provenance is deliberately exempt and stays.
A flagged bill cited by id is the evidence that a documented bug was real.
This repo's epistemics rest on findings being traceable to a record and a
date.
The rule now states that distinction instead of banning both cases and doing
neither.

**Evidence.** Pass dated 2026-08-24, immediately after the audit.

**Checks.** none.
