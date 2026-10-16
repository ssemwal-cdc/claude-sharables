---
id: pending
slug: execute-rules-retired
kind: decision
status: settled
date: 2026-10-16
---
# Execute-mode rules are retired

**Rule.** The eleven execute-mode rules below ended with execute mode. No plugin clicks, approves or responds, so none of them governs any code.

**Outcome protected.** A reader finds one record for the execute rules. No live rule governs a mode that is gone.

**Argument.**

The owner ruled this on 2026-10-16. Execute mode was retired under D91, review-only plugins. The rules for it had separate records. Each record kept its own retired text. The records check refuses that text. The eleven records are folded into this one. Git keeps the old files. Their prose and code sit in `actionable-retired/`.

The retired rules, each with its old id:

- Old id 14, never pre-write an action: log an outcome only after it is seen.
- Old id 18, never batch the click checks: stop the batch on a wrong record state.
- Old id 20, default the approval comment: fill the comment field without a prompt.
- Old id 28, Approve With Notes stays primary: every approval carries its note.
- Old id 37, render the execute bar always: show step 2 before step 1 is done.
- Old id 45, keep reference text out: the bar holds only commit controls.
- Old id 46, the bar ignores filters: an earlier decision still runs after a filter.
- Old id 48, the message authorises only: the gates sit in text a test reads.
- Old id 75, gate the two type lists: a reviewed type with no action fails the build.
- Old id 76, purchase orders take the bill route: a reviewed PO is approved in the same run.
- Old id 78, an unmapped subtype keeps buttons: a reviewer keeps live items while a link is fixed.

Process-only ruling.

**Evidence.**

- Ruled by the owner on 2026-10-16.
- Execute mode ended on 2026-09-18. See D91, review-only plugins.

**Checks.** none
