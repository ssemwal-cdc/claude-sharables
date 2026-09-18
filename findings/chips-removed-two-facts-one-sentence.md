---
id: pending
slug: chips-removed-two-facts-one-sentence
kind: finding
status: observed
date: 2026-08-24
---
# Onboarding time now reads as one sentence

**Outcome protected.** A teammate starts the setup today instead of deferring it.

**Argument.** A time figure read as booked sitting-and-watching time.
That is a much bigger ask than the thing is. It is the sort of number
that defers the step to a day that never comes.

The first pass fixed one step opener, which was the wrong scope.
The claim is true of the whole document, and someone deciding whether to start
has not reached that step yet.

The header carried two chips, after two rounds of them, and now carries none.
The two chips invited adding the halves and reading the total as booked time.
Nothing was lost by removing them.
Both facts now live in one lead sentence. So each gets its own assertion
rather than one a half-edit could satisfy.

The general rule worth keeping: delete a fact from the prose once it earns a
chip or a marker.
Do not leave the prose as the authority too.

**Evidence.** Reworked 2026-08-24 in two passes.
The figure landed at about 45 minutes with a stop after step three.
The introductory paragraph was 76 words against 48 for all three
prerequisites.
It came down to 41 words.
Whether readers start sooner is `unmeasured`.

**Checks.** `check_onboarding_page()` in `scripts/shared_blocks.py` checks
structure only, not placement.
