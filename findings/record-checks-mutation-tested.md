---
id: pending
slug: record-checks-mutation-tested
kind: finding
status: observed
date: 2026-09-15
---
# Record checks went red first

**Outcome protected.** A check is trusted only after it fails on the defect it guards.

**Argument.** A green check proves only its platform and its fixture.
So each check in `scripts/check_records.py` was mutation-tested before it was wired into
`scripts/validate.py`.
Each mutation was made in place, with a `.bak` copy as the undo.
No checkout-wide git write ran, because the checkout is shared.
One mutation found a real defect in the checker.
That row is named below.

**Evidence.** Measured on 2026-09-15, on this branch over `3a63144`.
Each row is one mutation of one file.
Every row went red on the mutation, and green again once the file was restored.
Ids and paths are described, never written, so this record stays inside the citation
rule it reports on.

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

The slug-citation row was blind on the first run.
The pattern asked for a word boundary after the closing guillemet, which never comes.
So a slug citation matched nothing and passed.
The fix landed before the check was trusted.

The hook was proved the same way, with 13 sample payloads on stdin.
Each forbidden form exited 2 with one line on stderr.
The forbidden forms are the stash, the reset, the restore, a checkout naming a path, a
pattern kill and a pid list.
A bare branch name, a new branch and a harmless command exited 0.
A forbidden form after a separator still exited 2, so a separator hides nothing.
A quoted mention inside an `echo` exited 0.
The `sed` fallback was proved with `jq` off the path.

The id claim was proved twice.
On this tree the dry run reports nothing pending.
On a scratch copy with two pending records it assigned the next free number per kind,
rewrote one slug citation, converted one supersedes slug and regenerated the three
indexes.
No existing id moved.

**Checks.** `python3 scripts/validate.py`, which calls the five checks.
