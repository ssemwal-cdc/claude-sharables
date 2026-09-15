---
id: pending
slug: execute-bar-always-rendered
kind: decision
status: settled
date: 2026-08-20
---
# Render the execute bar always

**Rule.** Render the execute bar in every state, including zero marks. Keep the header mirror as well.

**Outcome protected.** A first-time reader can see step 2 before they have done step 1.

**Argument.**

The bar used to collapse to one line of grey text below the queue until something was marked.

So step 2 was invisible until you had already worked out step 1 unaided. That is backwards for the one thing the page has to teach.

The two steps are numbered in the markup.

A second execute button is mirrored in the page header once something is marked.

Both exist because whether the widget frame scrolls internally is not knowable from the agent side. Do not delete one as redundant.

The header mirror renders a blocked chip instead of vanishing. Gating it on readiness alone left the top of the page silent at exactly the moment something was in the way.

**Evidence.**

- Changed 2026-08-20.
- Neither control is reachable mid-queue in the real host. See F‹widget-iframe-does-not-scroll›, the widget frame does not scroll.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
