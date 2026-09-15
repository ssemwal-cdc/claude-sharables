---
id: pending
slug: netsuite-notes-page
kind: gap
status: unobserved
date: 2026-08-15
---
# NetSuite notes page unseen

**Outcome protected.** An approval note lands where the auditor will look for it.

**Argument.** `Approve With Notes` loads a page nobody has seen.
The one attempt froze the tab.
The skill says to read that page rather than assume its field names or button labels.
Inventing those names would be worse than staying vague.
Nobody has read that button's handler either.
So "there is no popup" is inference from the UI, not observation of the code.

To clear it: approve one low-value bill and watch where the note lands.
Then tighten Step 8.6 with the real labels.

**Evidence.** This claim is guessed, not proven.
It is tested against mocks or fixtures and shipped.
Nobody has watched the notes page at all.
Do not cite it as established.
`python3 scripts/test_skill_code.py` covers the logic against mocks.
It cannot cover this gap, because this gap is about a real system.
The step number moved: this gap said Step 5 under the old numbering.
Step 5 is now the PO cross-check.
G‹no-end-to-end-run›, no watched run, records that no approval has carried a note yet.

**Checks.** none.
