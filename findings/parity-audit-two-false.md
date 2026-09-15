---
id: F80
slug: parity-audit-two-false
kind: finding
status: observed
date: 2026-08-26
---
# Two audit findings were wrong

**Outcome protected.** A parity audit is read as evidence, not as a diff of vocabularies.

**Argument.**

An audit across the two skills asked whether the stated best practices are followed rather than asserted, and was told to raise rather than fix.

Three of five findings were real. Two were wrong, and both false positives came from the same move, grepping one plugin for the vocabulary of the other.

Two were caught and fixed. Procore recorded nothing about which file backed a verdict. The NetSuite record capability row still assumed pre-opened tabs, an hour after the queue step stopped opening them.

Withdrawn on inspection: the claim that NetSuite never names the successful fan-out state. It has no such fan-out at all, and every leg of each three-state instance it does have is named.

Withdrawn on inspection: the claim that the Procore workflow gate is missing from its capability table. It is handled in the gate step with the strictest three-state code in either plugin.

The capability table answers what happens to a check when its input is missing. The gate decides whether an item is reviewable at all. Two kinds of absence, correctly filed apart.

Do not re-raise that by diffing the two capability tables. The asymmetry is the point.

The real finding came from the maintainer correcting the question. See D67, ask once for the queue.

**Evidence.**

- Run 2026-08-26 before a commit.
- The Procore support-read list is F73, name the file behind a verdict.

**Checks.** none
