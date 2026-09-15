---
id: pending
slug: onboarding-sheet-is-the-file
kind: decision
status: settled
date: 2026-08-17
---
# The page is the file

**Rule.** Edit `docs/onboarding.html` and push. Never publish the sheet as an artifact.

**Outcome protected.** Every teammate reads the current sheet.

**Argument.**

The sheet is served by GitHub Pages from the docs folder on the default branch. There is no publish step and no second copy to drift.

It replaced a published artifact because that arrangement had two silent failure modes. Editing the file changed nothing teammates saw, and republishing without passing the existing URL minted a second artifact while everyone kept reading the first.

The sheet must stay a complete HTML document, with a doctype, a head and a character-set meta tag. Pages serves the file verbatim.

It was originally written as an artifact fragment, because the artifact host wraps content in its own skeleton. Served raw without that wrapper, every dash, arrow and middot becomes mojibake.

So it can no longer be published as an artifact as is. Handing the file to a render tool would nest a second root element. Strip the wrapper first, or send the Pages link.

A redirect file makes the bare URL work, because Pages has no directory index and would otherwise return a 404 on the short link.

The sheet carries one small script and that is the only one. See F‹onboarding-copy-buttons›, copy buttons built at run time.

The sheet is written click by click for someone who has never touched any of this. Every step ends in a done-when check, which is the device that makes it followable. Keep that if you edit it.

**Evidence.**

- Moved to Pages in 2026-08. The theme blocks were removed 2026-08-17.
- The live page cannot be fetched from the sandbox. See F‹github-io-egress-blocked›, the live page is unfetchable.
- Four claimed tests over the sheet did not exist. See F‹onboarding-claims-unchecked›, four claimed tests were absent.
- The time and posture wording is settled. See F‹sheet-time-and-posture›, say how long and where.

**Checks.** `check_onboarding_page()` in `scripts/shared_blocks.py`.
