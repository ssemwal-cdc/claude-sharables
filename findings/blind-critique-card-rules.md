---
id: pending
slug: blind-critique-card-rules
kind: finding
status: observed
date: 2026-08-24
---
# Four rules from a critique

**Outcome protected.** Every row title starts at the same x, and a flagged row still reads as flagged.

**Argument.**

Eight critics were shown only screenshots, with no code, no brief and no history.

24 clustered findings came back, and each was verified against the pixels before it was acted on.

Four rules came out of it. The left rail carries the verdict, and the mark state must not touch it. Marking a flagged row used to erase the only cue that it was flagged.

Marks are the card tint and a will-do pill now.

The verdict label sits on the meta line, never before the title. A token whose width depends on its own word shifts every title it precedes.

Cap the measure on running prose only, never on the figures panel. Capping the figures too was tried and measured, and its long figure strings wrapped over more lines than the clamp saved.

A bare exclamation prefix is not a label. The warning is its own block now, with a rule above it and an uppercase heading, clamped to three lines behind a more control.

The old glyph sat at the same line pitch as the arithmetic above it, so two unrelated blocks read as one paragraph.

**Evidence.**

- Run in 2026-08 and landed 2026-08-24 in both plugins.
- The label shift measured 16px between the two NetSuite verdict words, and the Procore gate-unknown label would have set a gutter of about 118px for every row.
- Capping the figures panel measured 216px against 221px, so it cost more height than it saved.
- The prose clamp needs its control conditioned on clipping. See F‹more-button-needs-clipping›, a clamp needs real clipping.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
