---
id: pending
slug: netsuite-verdict-words-fold
kind: finding
status: settled
date: 2026-08-24
---
# NetSuite cannot fold rows

**Outcome protected.** Nobody adds a feature to NetSuite that would copy a file byte for
byte.

**Argument.** NetSuite has no slim build, and nothing in it would fold.
Procore's slim build folds the verdicts that need no action.
NetSuite's three verdicts, `clear`, `history-open` and `flagged`, all need a read before approval.
NetSuite has no `skipped` verdict, because a missing attachment flags an item.
So there is no verdict to fold.
A fold would copy `index.html` byte for byte on every run.

The fold could not be a shared block either, because the folded keep-list is
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
Rewritten 2026-10-12 for the third verdict (D109, a third NetSuite verdict).
The earlier premise, that the verdicts were exactly `clear` and `flagged`, no longer holds.
The conclusion does.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py` pins the
NetSuite vocabulary.
