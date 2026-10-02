---
id: F167
slug: charcode-fetch-refused
kind: finding
status: observed
date: 2026-10-02
---
# The safety check refused the char-code fetch

**Outcome protected.** A skill routes around a filter never again, because the route itself gets refused.

**Argument.**

The Procore queue read once built its query string from character codes, to route it past the output filter.

Measured live 2026-10-02, the session's safety check refused that call, tagged `[Auto-Mode Bypass]`.

A separate call, on NetSuite, blanked `?`, `&` and `=` out of its returned value, to pass the same filter. The safety check refused that one too, same tag.

The same fetch, written plainly with `URLSearchParams`, returned HTTP 200 with 56 items. The Step 2 gate and the Step 3 record reads passed the same way, plainly built, no evasion.

**Evidence.**

- Measured live 2026-10-02, Claude in Chrome, Claude Code auto mode.
- Git: the char-code sentence was entered at commit `892b664` on 2026-08-11. No decision record governed it.
- PR #16, on 2026-09-16, only re-wrapped that sentence. It never reconsidered it.
- See D95, the rule this finding established.

**Checks.** none
