---
id: F93
slug: invented-threshold-in-comment
kind: finding
status: observed
date: 2026-09-01
---
# An asset invented a threshold

**Outcome protected.** A run cannot assemble an authoritative refusal out of repo text.

**Argument.**

`publish_dashboard.py` shipped a comment claiming that past roughly 90 KB the render stops being reliable and gets refused.

It shipped for months. The skill prose twelve lines away called a claim of exactly that form a prediction written as a fact.

A run reads both. So the repo supplied the words for an authoritative-sounding refusal.

That is the third time a refusal was assembled out of repo text.

The comment is gone. Grep for invented thresholds after writing prose that forbids them. The prose does not police the assets.

**Evidence.**

- Found 2026-09-01. The 90 KB figure was never measured and appears in no observation.
- The refusal it fed is F96, the read side had a real wall.

**Checks.** none. No script greps assets for invented thresholds.
