---
id: pending
slug: skipped-rows-compact
kind: decision
status: settled
date: 2026-10-07
---
# A skipped row publishes compact

**Rule.** A skipped item carries only its key, link fields, head, attachment names and amount. The publish script strips comments from the page. It writes no second copy.

**Outcome protected.** The render fits one read, so the reviewer sees every row.

**Argument.**

A skipped row is one line and a head. Nobody acts on its facts or detail.

The field run on company 2866 had 67 items. Skipped rows still carried full text, and the comments rode along.

The slim copy saved little. See F123, the slim build is no fallback.

**Evidence.**

- Owner ruling, 2026-10-07, from the 67-item field run.

**Checks.** `test_field_run` in `scripts/test_skill_code.py`.
