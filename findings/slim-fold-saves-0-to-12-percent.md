---
id: pending
slug: slim-fold-saves-0-to-12-percent
kind: finding
status: settled
date: 2026-08-24
---
# Slim build is no fallback

**Outcome protected.** A skipped item keeps the response button it most often needs.

**Argument.** Procore rendered the slim copy as its primary dashboard.
The justification was that it is roughly a fifth smaller.
Measured across five fixture queue mixes, the real figure is 0% to 12%.
Only `skipped` and `ungated` rows fold, and a live queue is mostly neither.
So the saving was always going to be small.

The cost is not small.
Folded rows drop `resp`, `head`, `facts` and `detail`.
So on the slim render a `skipped` item cannot be sent back.
That is the response such an item most often needs.
An earlier note guessed the cost was nil, because folded rows have no
response buttons to lose.
That is true of `ungated` and false of `skipped`.
The publish script's own `no_resp` warning covers `skipped` for exactly that
reason.

Procore now renders `index.html`, matching NetSuite.
The slim copy is reached only when the integrity banner fires.

**Evidence.** Measured 2026-08-24 across five fixture queue mixes.
0% when nothing is skipped or ungated.
2% to 6% on a realistic mix.
113 KB became 101 KB at the large end, which crosses no observed threshold.
A deliberately even 62-item fixture came down from 174 KB to 129 KB on
2026-09-01.
G15, nothing has rendered at 161 KB, carries the render ceiling.

**Checks.** none for the size claim. `check_verdict_vocabulary()` covers the
fold branch's verdicts.
