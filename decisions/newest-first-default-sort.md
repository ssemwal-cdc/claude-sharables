---
id: pending
slug: newest-first-default-sort
kind: decision
status: settled
date: 2026-08-20
---
# Sort newest first by default

**Rule.** Default both dashboards to newest first. Keep verdict as a dropdown option.

**Outcome protected.** The person reading the queue every day sees recency first.

**Argument.**

This was asked for directly and it overrides the earlier note.

That note argued that flagged-first is what the page is for, and that a reader who touches nothing must see what they saw before.

The reasoning was sound and was still outranked. The person reading the queue every day wanted recency.

Verdict survives as an option in the NetSuite dropdown, so nothing is lost. Only the default changed.

Do not quietly restore the old default.

**Evidence.**

- Asked for 2026-08-20.
- Shipping it needed a new view key. See D‹new-default-new-view-key›, a new default needs a new key.
- The toolbar came from Procore. See F‹netsuite-view-controls-port›, NetSuite got the Procore toolbar.
- Procore newest is a deadline proxy. See F‹procore-newest-is-deadline-proxy›, Procore newest is a proxy.
- The ordering key must not be clamped. See F‹age-clamp-wrong-in-comparator›, never clamp an ordering key.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
