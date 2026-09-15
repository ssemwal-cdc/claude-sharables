---
id: F33
slug: plain-approve-noop-user-activation
kind: finding
status: observed
date: 2026-08-15
---
# Plain Approve can no-op

**Outcome protected.** A click that did nothing is caught before the batch moves on.

**Argument.**

Five identical clicks on plain Approve had zero effect.

The handler of that button loads a client script asynchronously and only then opens a window. By then the transient user activation from the click has expired.

Chrome drops the navigation with no error, no dialog and no network request.

The post-click page read is the only thing that catches it.

Recovery is one click, a page-load check, then navigating the approval URL read verbatim out of the handler of the button.

Assert the parameters, which are the record id, the action type and the approver id of the user. Fire once.

It is the same server path and the same audit trail as the button, minus the dropped window open. It is not a REST bypass, so the rule against writing records through the connector is untouched.

Affirmative only, never Reject, and it carries no note.

Do not fix this by re-clicking harder.

**Evidence.**

- Observed 2026-08-15 with 5 dead clicks. Confirmed live on record 2534442 after those clicks.

**Checks.** none
