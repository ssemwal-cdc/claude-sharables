---
id: pending
slug: age-clamp-wrong-in-comparator
kind: finding
status: observed
date: 2026-08-20
---
# Never clamp an ordering key

**Outcome protected.** A future-dated row sorts correctly and reads sensibly.

**Argument.**

The NetSuite age helper clamped at zero, and that clamp was wrong in a comparator.

Every future-dated bill collapsed to zero and tied with every other one.

That was invisible while verdict was the default sort. It is wrong at the top of a newest-first list, which is exactly where future-dated rows now land.

There are two helpers now. One is unclamped for ordering. One is clamped for display, because a negative day count is nonsense to read.

Procore had the mirror image. Its day count was correctly unsigned-free, and the display was the broken half, rendering a negative day count for a deadline still ahead.

A phrasing helper fixes the display there, and the comparator still gets the sign.

Never clamp the ordering key, and never sign the display.

**Evidence.**

- Found 2026-08-20 with the newest-first default.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
