---
id: D106
slug: skipped-rows-compact
kind: decision
status: settled
date: 2026-10-07
---
# A skipped row publishes compact

**Rule.** A skipped item carries only its key, link fields, head, attachment names and amount. The publish script strips every comment from the page except the two data markers. It writes no second copy.

Detail on a flagged or clear row is capped at 240 characters. The full text is one read-only `sendPrompt` click away. The cap lives in shared block `pub-detail-cap`.

**Outcome protected.** The render fits one read, so the reviewer sees every row.

**Argument.**

A skipped row is one line and a head. Nobody acts on its facts or detail.

The 2026-10-07 field run had 67 items. Skipped rows still carried full text, and the comments rode along.

Before commit `c888908` the publish script did not strip comments. The cap on flagged and clear detail came with that commit, to keep long detail out of the render.

The slim copy saved little. See F123, the slim build is no fallback.

**Evidence.**

- Owner ruling, 2026-10-07, from the 67-item field run.

**Checks.** `test_field_run` in `scripts/test_skill_code.py`.
