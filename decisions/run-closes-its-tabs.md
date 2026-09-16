---
id: pending
slug: run-closes-its-tabs
kind: decision
status: settled
date: 2026-09-16
---
# A run closes every tab it opened

**Rule.** Every tab a run opens is closed by that run, before the report. The keep list is empty. A tab the user opened is never closed.

**Outcome protected.** A finished run leaves the browser as it found it. The dashboard is the route to a record.

**Argument.**

A review of both skills found three defects in how they handled tabs.

First, the word "scratch" was undefined. The improvised fetch tab and the pdf.js tab were neither a record tab nor a named scratch tab. No rule reached them.

Second, the only cleanup line sat in the wrong place. In Procore it was a clause inside an unrelated Step 4 bullet. In NetSuite it followed unrelated Step 7 prose about template edits.

Third, nothing checked tab state before the report. A run could report done with every tab it opened still open.

The rule chosen is an empty keep list. Each skill now names every tab type it opens and the trigger that closes it. A shared Step 9 calls `tabs_context_mcp`, closes every tab the run opened, and leaves every other tab alone.

Two alternatives were rejected. "Keep flagged records open" and "keep every reviewed record open" both make the browser a second deliverable. Every dashboard card links to its record, so a kept tab adds nothing. `D44`, the widget is the deliverable.

**Evidence.**

- `F‹fetch-tab-state-lost›`, fetch tab navigated, is the run that showed the cost.
- The three defects were found by reading both `SKILL.md` files on 2026-09-16.

**Checks.** `python3 scripts/shared_blocks.py --check` proves the Step 9 block matches canonical in both skills.
