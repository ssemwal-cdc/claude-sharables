---
id: F112
slug: netsuite-verdict-vocabulary-blocks-fold
kind: finding
status: settled
date: 2026-08-24
---
# NetSuite cannot fold rows

**Outcome protected.** Nobody adds a feature to NetSuite that would copy a file byte for
byte.

**Argument.** NetSuite is not getting a slim build to match Procore's, and the reason is
structural.
Its verdicts are exactly `clear` and `flagged`, which is the slim build's
actionable set.
The fold branch is the `else`.
So nothing would ever fold.
The output would be a byte-for-byte duplicate of `index.html` on every run.

NetSuite has no `skipped` concept by design, because a missing attachment
flags an item.
It could not be a shared block either, because the folded keep-list is
per-domain.
The Procore keep-list names project, due, project id, contract id, kind,
workflow and key.
NetSuite's equivalent field is the transaction date.

It was asked for on grounds of symmetry and declined on grounds of
vacuousness.
"Make the two match" is usually the right instinct in this repo, and here it
is not.

**Evidence.** Recorded 2026-08-24, alongside
`F123`, the fold's own size measurement.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py` pins the
NetSuite vocabulary.
