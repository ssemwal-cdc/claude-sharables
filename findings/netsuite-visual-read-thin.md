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
A mention count is a snapshot, not a durable fact, and it has already drifted once.
See Evidence for the count as of this record's last check.
Both files name all six attachment outcomes.
So the doctrine holds formally.

NetSuite still has less written down about the image and `scanned` branches than Procore.
That gap is no longer left alone on purpose.
Amended 2026-09-24 by the maintainer.
The old argument said to wait for a NetSuite observation before any NetSuite fix.
The maintainer ruled that argument bad.
A visual-read rule found on one skill now goes to both, unless the rule is per-domain.
The first-page rule is the first case. It sits in the `skill-first-page-read` shared block.

**Evidence.** Mention counts are a snapshot from the command in Checks below, not a durable fact.
No script holds them current, so re-run the command before citing a figure.
Measured 2026-08-26: Procore `image` 11 times, `scanned` 10 times, NetSuite `image` 2 times, `scanned` 3 times.
Re-measured 2026-09-24: Procore `image` 12 times, `scanned` 11 times, NetSuite `image` 2 times, `scanned` 4 times.
The `scanned` counts drift on a wording change alone, not on a run.
G6, two branches still unfired, carries the unfired branches.

**Checks.** `check_check_registry()` asserts both capability tables stay declared.
`check_visual_read_mentions()` in `scripts/check_records.py` counts image and
scanned mentions in every `SKILL.md` and fails on drift from the Evidence figures.
