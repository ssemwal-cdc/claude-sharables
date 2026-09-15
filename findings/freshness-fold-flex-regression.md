---
id: pending
slug: freshness-fold-flex-regression
kind: finding
status: observed
date: 2026-08-24
---
# A fold restored the height

**Outcome protected.** The chrome above the first item is smaller, measurably.

**Argument.**

The freshness card was a bordered box restating what the header pill already says. A pending tile restated the subtitle directly above it. Both are gone.

The first attempt moved the freshness line inside the header block, whose left column is a flex item sized to its own content.

So a long line made that column wide, wrapped the right-hand group onto a second row, and grew the header block instead of shrinking it.

The line is a sibling of the header block now. The left column carries a flex basis and a zero minimum width, so a long subtitle wraps inside its own column.

**Evidence.**

- Measured 2026-08-24. The first attempt grew the header block from 54px to 148px for a net saving of 6px.
- The landed version cut the chrome above the first item from 454px to 380px on NetSuite and from 467px to 401px on Procore.

**Checks.** `scripts/measure_float.js` by hand.
