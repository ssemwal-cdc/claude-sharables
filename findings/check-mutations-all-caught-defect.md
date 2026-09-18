---
id: pending
slug: check-mutations-all-caught-defect
kind: finding
status: observed
date: 2026-09-15
---
# Every record check caught its mutation

**Outcome protected.** A check is trusted only after it fails on the defect it guards.

**Argument.** A green check proves only its platform and its fixture.
So each check in `scripts/check_records.py` was mutation-tested before it was
wired into `scripts/validate.py`.
Each mutation was made in place, with a `.bak` copy as the undo.
No checkout-wide git write ran, because the checkout is shared.

Every row in the table below went red on its mutation, and green again once
the file was restored.
One mutation found a real defect in the checker instead of only proving the
check.
See `F‹citation-regex-was-blind-once›`, the check that was blind once, for that
row.

**Evidence.** Measured on 2026-09-15, on this branch over `3a63144`.
Ids and paths are described, never written, so this record stays inside the
citation rule it reports on.

| Check | Mutation | What the check said |
|---|---|---|
| `check_frontmatter` | a status outside the allowed six | the status is not one of the six |
| `check_frontmatter` | a decision takes an id another decision holds | the id is reused, and the holder is named |
| `check_frontmatter` | the outcome marker is renamed | the outcome line is missing |
| `check_frontmatter` | the slug stops matching the filename | the slug must equal the filename stem |
| `check_frontmatter` | a finding takes a decision letter | a finding takes the letter F |
| `check_frontmatter` | a date written as a day, a month name and a year | write the date as YYYY-MM-DD |
| `check_citations` | a cited number that no record holds | no record carries that id |
| `check_citations` | the gloss after a cited id is deleted | the citation carries no gloss |
| `check_citations` | the removed prose file is named in the index | the line cites a path |
| `check_citations` | a step ordinal is cited from a record | the line cites a path |
| `check_citations` | a slug citation that names no pending record | no record in that folder has the slug with id pending |
| `check_index_fresh` | a record title is reworded | the index is stale, with the first differing line |
| `check_index_fresh` | an index row is edited by hand | the index is stale, with the first differing line |
| `check_index_size` | 8 filler lines appended to the index | the index is 154 lines, and the rule is 150 |
| `check_index_size` | a plugin name misspelled in the index | the registered plugin is not named |
| `check_sentence_length` | a 40-word sentence appended to a record | a 40-word sentence, over the 30-word ceiling |
| `check_sentence_length` | the same sentence appended to the index | a 40-word sentence, over the 30-word ceiling |

**Checks.** `python3 scripts/validate.py`, which calls the five checks.
