---
id: pending
slug: no-filter-evasion
kind: decision
status: settled
date: 2026-10-02
---
# A skill never shapes its way past a filter

**Rule.** A skill never shapes code or output so a filter or safety check misses it. No char codes. No splitting, spacing out, encoding or rewording a value to get it past one. Build every query string plainly, with the platform's own query-string builder. Keep each URL inside the page that holds it. Return parsed values, never a URL or a piece of one. Never move bytes, a URL or page state between tabs. Never design a route around a safety-check refusal.

**Outcome protected.** A run passes the safety check honestly, and never hides data from it.

**Argument.**

A filter and a safety check both exist to see what a run is doing.

A char-code recipe, a split value, or a route built around a refusal is the same move. Each one makes the flagged thing stop looking like itself.

The session's own safety check drew that line already. It refused the char-code fetch. It refused a blanked-character return value too. Both carried the tag `[Auto-Mode Bypass]`.

The plain version of the same call worked. `URLSearchParams`, a real query string, a real fetch, 56 items back.

The evasion bought nothing. It bought a false "had to work around it" story, and a route the safety check actively rejects.

The fix is not a cleverer evasion. Write the call the way it always had to run: plainly, visibly, refusable if it should be refused.

**Evidence.**

- See F‹charcode-fetch-refused›, the safety check refused both the char-code and the blanked-value fetch.
- See F‹chrome-filter-per-field›, the filter is narrower than assumed, which removed the reason to route around it.
- Git: the char-code sentence was entered at commit `892b664` on 2026-08-11, with no decision record.
- PR #16, on 2026-09-16, only re-wrapped that sentence. It never reconsidered it.

**Checks.** none
