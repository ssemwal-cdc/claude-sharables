---
id: pending
slug: onboarding-copy-buttons
kind: finding
status: settled
date: 2026-08-28
---
# Onboarding copy buttons work

**Outcome protected.** A teammate pastes the whole schedule prompt on one click.

**Argument.** The sheet was rendered and driven in Chromium during a pre-share freshness audit.
Nothing about this page had ever been checked in a browser before.
`check_onboarding_page()` reads the file as text.
The repo's one browser check is about the dashboards.
Three things the code reasons about in comments are now observed rather than argued.

- **Copy from a closed `<details>` returns the whole prompt.**
  This is the case the handler's comment is written for.
  `innerText` is layout-dependent, and a `<pre>` with no layout returns an empty string.
  Without the `textContent` fallback the button would copy nothing and still report success.
- **Copy does not toggle the block.** The button sits inside `<summary>`.
  A click there would ordinarily open the `<details>`.
  `preventDefault` and `stopPropagation` hold.
- **`<n>` arrives literal.** The source must stay escaped as `&lt;n&gt;`.
  What lands on the clipboard is the placeholder the chat should actually receive.
  No escaped entity survives.

**What this does not cover is whether it looks right.**
Layout metrics are not typography, spacing or hierarchy.
Anything genuinely visual still has to be eyeballed by a person.

**Evidence.** Rendered and driven in Chromium 2026-08-28.
Closed-block copy measured 2,272 characters for the NetSuite block and 2,224 for the Procore one.
`open` was `false` before and after the click on both blocks.
Measured at 1600px, 1200px and 390px, in both colour schemes.
No horizontal scroll, no element wider than the viewport, no console or page errors.
The nav rail is correctly absent below 1300px.
The page is 5,926px tall on desktop and 9,191px tall on mobile.
Two dead tokens turned up: `--accent-soft` and `--danger` are defined in both themes and referenced nowhere.
They are left alone as harmless.
Appearance is `unmeasured`, because only a person can judge it.

**Checks.** `check_onboarding_page()` in `scripts/shared_blocks.py`, text only.
