---
id: pending
slug: github-io-egress-blocked
kind: finding
status: observed
date: 2026-08-17
---
# The live page is unfetchable

**Outcome protected.** A blocked fetch is not read as a broken site.

**Argument.**

The sandbox egress proxy blocks the Pages host, so a web fetch of the live URL returns a blocked marker.

Do not read that as the site being broken.

Do not conclude from a green Pages deploy that the page renders. The deploy proves GitHub built the file, nothing more.

Editing the sheet works normally. Only fetching the published page does not.

What is checkable locally is worth checking after any edit. The file decodes as UTF-8, the markup has no unclosed tags, the character-set meta tag is present, the body sets its own background from a token, and every custom property used is defined on a bare root selector.

That last one is what stops the page rendering one theme text on the other theme ground for anyone on the system setting.

Anything genuinely visual has to be eyeballed by the user. Ask rather than assume.

**Evidence.**

- Observed 2026-08-17. The proxy also blocks the Anthropic marketing and support hosts and the Chrome web store.
- The Procore developer host is blocked the same way. See F‹commitment-payload-three-of-four›, three borrowed names in four.

**Checks.** `check_onboarding_page()` in `scripts/shared_blocks.py`.
