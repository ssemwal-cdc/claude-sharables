---
id: pending
slug: approved-by-claude-comment
kind: decision
status: settled
date: 2026-08-14
---
# Default the approval comment

**Rule.** Attach `Approved by Claude` to every affirmative response. A comment the user supplies for that item replaces it verbatim.

**Outcome protected.** An authorised batch runs without stopping to ask what to type in a comment field.

**Argument.**

A run once invented the text, then stopped a 15-item batch worth 61.2 million dollars to ask whether to keep it. The hesitation came from the wording being improvised.

An agent that made up the text has something to second-guess. Specifying the text removes the question.

Nothing else is ever typed into a comment or a note field.

This is a better default than blank. A response with no comment reads as though the user clicked it. The attribution says what actually did.

A rejection reason is still required from the user and is never defaulted. Boilerplate would be actively harmful there.

Both skills also state that the user is one reviewer among several and is not the accountant of record. So an authorised batch is not stalled over amounts or audit exposure.

The mechanical checks are unchanged and still stop the batch.

**Evidence.**

- The 15-item batch and its 61.2 million dollar total are from a live run. Both skills carry the default now.
- NetSuite routes every approval through Approve With Notes so it can attach the note. See D‹approve-with-notes-primary›, notes route is primary.

**Checks.** none
