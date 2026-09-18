---
id: D37
slug: execute-bar-always-rendered
kind: decision
status: superseded
date: 2026-08-20
---
# Render the execute bar always

**Superseded by** D91, review-only plugins, on 2026-09-18. Execute mode was retired. The rule returns with it, and the text lives on in `actionable-retired/`.

**Rule.** Render the execute bar in every state, including zero marks. Keep the header mirror as well.

**Outcome protected.** A first-time reader can see step 2 before they have done step 1.

**Argument.**

The bar used to collapse to one line of grey text below the queue until something was marked.

So step 2 was invisible until you had already worked out step 1 unaided. That is backwards for the one thing the page has to teach.

The two steps are numbered in the markup.

A second execute button is mirrored in the page header once something is marked.

Both exist because the widget frame never scrolls. F82, the widget frame never scrolls, settled this on 2026-08-26: the bar sat 3,874px down a 4,114px document. Do not delete one as redundant.

The header mirror renders a blocked chip instead of vanishing. Gating it on readiness alone left the top of the page silent. That happened at exactly the moment something was in the way.

**Evidence.**

- Changed 2026-08-20.
- Neither control is reachable mid-queue in the real host. See F82, the widget frame does not scroll.
- The disabled style served two meanings. See F57, one disabled style, two meanings.
- The tick must not re-render. See F72, the tick must not render.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
