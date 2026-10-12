---
id: F79
slug: netsuite-visual-read-thin
kind: finding
status: settled
date: 2026-08-26
---
# NetSuite visual read prose thin

**Outcome protected.** A rule for reading an image or a scan reaches both skills in the same change.

**Argument.** The 2026-08-26 parity audit noticed this and recorded it rather than acting on it.
Both files name all six attachment outcomes.
So the doctrine holds formally.

NetSuite still has less written down about the image and `scanned` branches than Procore.
That gap is no longer left alone on purpose.
Amended 2026-09-24 by the maintainer.
The old argument said to wait for a NetSuite observation before any NetSuite fix.
The maintainer ruled that argument bad.
A visual-read rule found on one skill now goes to both, unless the rule is per-domain.
The first-page rule is the first case. It sits in the `skill-first-page-read` shared block.

Amended 2026-10-12 by the owner.
The word count of `image` and `scanned` is retired.
A count of words says nothing about whether a rule reached both skills.

**Evidence.** G6, two branches still unfired, carries the unfired branches.

**Checks.** `check_check_registry()` asserts both capability tables stay declared.
