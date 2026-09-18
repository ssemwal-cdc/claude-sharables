---
id: G8
slug: netsuite-browser-mode
kind: gap
status: unobserved
date: 2026-08-24
---
# NetSuite browser mode unrun

**Outcome protected.** A teammate with no connector still gets a complete review.

**Argument.** The skill runs without the MCP connector.
Browser mode takes the queue from the dashboard portlets.
It reads record fields with `get_page_text`.
It reads the attachment URL off the record page.
It does not perform Step 5's PO and billing-history cross-check.
None of browser mode has been run.

**One consequence surfaced on 2026-08-24: browser mode could not publish at all.**
`publish_dashboard.py` hard-aborted when `config.me` or `config.tool` was missing.
Step 0 omits both in browser mode by design.
The portlets are per-user saved searches, already scoped to whoever is signed in.
So a browser-mode run completed the whole review and then died at step seven.
It told the user to run a first-time setup they had done correctly.
The fix: `account` is required on both routes.
`me` and `tool` are required in connector mode only.
The identity guard is unchanged for connector runs.

**The method matters more than the bug.** This is the second defect found by reading the two
plugins against each other rather than by running either.
It survived since browser mode shipped, because nothing exercised the path.
A gap on this list is not inert.
It is where the next bug is.

**The unobserved piece is the attachment URL DOM read.** The queue and record-page halves are
reverts to methods that worked before the bulk queries replaced them.
Those are the low-risk part.
Nobody knows whether the attachment field renders as `a[href*="media.nl"]` on every record type.
It may render as something else on some types.

To clear it: open one bill and one change order with the connector switched off.
Confirm the selector returns the four parameters.
Then confirm the fetch and pdf.js path is byte-identical to the connector route from there on.

**The thing to check is a silence, not an error.** Step 5 is skipped with nothing said about it.
That silence is deliberate.
A caveat would print on every item of every run for someone who cannot be provisioned.
So confirm the verdicts read as complete statements of what was checked.
They must not read as connector-mode verdicts with a hole in them.
See D69, silence for a capability nobody can obtain.

**Evidence.** This claim is guessed, not proven.
It is tested against fixtures and shipped.
Nobody has watched browser mode run.
Do not cite it as established.
`python3 scripts/test_skill_code.py` covers the logic against mocks.
It cannot cover this gap, because this gap is about a real system.
Browser mode was added 2026-08-15.
The publish abort was reproduced from a fixture on 2026-08-24, then fixed.

**Checks.** `scripts/test_skill_code.py` for the publish guard. None for the DOM read.
