---
id: F123
slug: slim-fold-saves-0-to-12-percent
kind: finding
status: settled
date: 2026-08-24
---
# Slim build is no fallback

**Outcome protected.** The reviewer reads every row of a large queue in one render.

**Argument.** Procore once rendered a slim copy as its primary dashboard.
The justification was that it is roughly a fifth smaller.
Measured across five fixture queue mixes, the real figure is 0% to 12%.
Only `skipped` and `ungated` rows fold, and a live queue is mostly neither.
So the saving was always small.

The slim copy also dropped `resp`, `head`, `facts` and `detail` from folded rows.
It was never a fallback. It was a second file to keep in step.

Owner ruling, 2026-10-07: delete the slim build.
Two cheaper cuts replace it.
The publish script strips comments from the page.
A `skipped` row publishes compact in `index.html` itself.
The first reason for the slim copy was one-click execute on a skipped item.
D91, review-only plugins, retired that outcome.

**Evidence.** Measured 2026-08-24 across five fixture queue mixes.
0% when nothing is skipped or ungated.
2% to 6% on a realistic mix.
113 KB became 101 KB at the large end, which crosses no observed threshold.
A deliberately even 62-item fixture came down from 174 KB to 129 KB on
2026-09-01.
G15, nothing has rendered at 161 KB, carries the render ceiling.

**Checks.** `test_field_run` in `scripts/test_skill_code.py` asserts that no `widget.html` is written.
