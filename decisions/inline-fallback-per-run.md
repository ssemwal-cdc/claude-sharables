---
id: pending
slug: inline-fallback-per-run
kind: decision
status: settled
date: 2026-11-11
---
# Inline fallback lasts one run

**Rule.** Publish inlines a dashboard asset whose tag still holds `__PIN_`. A run may also pass `--inline` to inline every asset. The flag is for that run only. Nothing stores it. The next run tries the CDN again.

**Outcome protected.** If the CDN fails, a dashboard still renders. A later run returns to the pinned copy with no manual reset.

**Argument.**

A stored flag has no way back. Once set, every later run would inline the code. No run would try the CDN again.

The fallback is licensed by an observed failure. See D77, render first, believe the guard: the CDN banner is that failure.

**Evidence.**

- The publish script on branch `claude/cdn-split` says `--inline` is a flag for one run and is never stored.
- The same script inlines a tag that still holds `__PIN_`.

**Checks.** none.

Kind: process
Home: plugins/procore-open-items-review/skills/procore-open-items-review/assets/publish_dashboard.py
