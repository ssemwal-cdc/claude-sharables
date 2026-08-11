# Procore open items review

Reviews the Procore items that are genuinely waiting on your workflow response
and publishes the results to a dashboard you can act from.

The hard part is not the review — it is working out which of your open items
actually need you. Procore's My Open Items list mixes things awaiting your
response with things you are merely on the distribution list for. This plugin
separates them.

## What it does

For every item in your queue it checks `user_permissions.can_respond` on the
live workflow. Items you cannot action are counted and suppressed, not shown.
On a real Compass queue that took 75 items down to 32.

For the ones that remain:

**Subcontractor invoices** — re-derives all six AIA G702 identities from the
record rather than reading the summary back, foots every G703 line, checks
retainage consistency and application sequence against the previous
requisition, then locates each headline figure in the attached pay application.

**Internal change risks** — ties Cost Impact to the accepted cost and the
accepted cost to the total on the attached proposal, and foots the proposal's
own phase lines. Catches placeholder values that pass a naive has-a-value check.

**Commitment change orders** — foots line items to the package grand total and
ties each attached PCI to a line.

Each item lands as clear, flagged, skipped or gate-unknown. **Skipped is a real
verdict**: an item with no support attached is not ready for review, so it is
not approved, not rejected, and not given a verdict it hasn't earned.

## Support is read without downloading anything

Procore attachments sit behind a 60-second presigned S3 link. The browser's PDF
viewer exposes no text and cannot be scripted, and the storage host blocks
cross-origin reads. The plugin routes around all three and extracts PDF text
in-browser, so nothing lands in your downloads folder.

## The dashboard

Verdicts render as an inline dashboard widget in the conversation: summary cards, a
fact strip per item you can judge without expanding anything, and sort and
filter controls — campus, then building, then type, plus search.

Response buttons come from each item's own workflow step rather than a fixed
set, so invoices offer Approve / Revise and Resubmit while change risks at a
cost gate offer Yes / Reject. Marking an affirmative response on an item with
no support raises a warning.

You mark responses per item, then execute them together. Execute sends the
instruction straight into the conversation in one click. Nothing reaches Procore
from the dashboard itself — the responses run from that message, and each item is
re-verified as still yours to action immediately before it is clicked.

## Requirements

- Claude in Chrome, signed in to Procore
- A connected workspace folder for state
- No connector. Procore has no MCP connector, so the dashboard is a snapshot
  with a prominent re-check control rather than a live view. It says so plainly
  and ages its own timestamp.

## First run

Say "run my Procore review". Setup happens once and asks you to confirm your
company id, the tool id of your change-risk custom tool, and the cost custom
field mapping — all of which differ per company.

There is no user id to configure. Procore's queue endpoint and permission gate
are both scoped to the signed-in session, so the review is automatically yours.

## Safety

The plugin never responds on its own judgement. A verdict is a recommendation.

Because the dashboard is a snapshot, executing re-verifies every item against
the live workflow **before any click**. If you already actioned something in
Procore directly, it is skipped and logged rather than clicked or retried — so
a stale page cannot cause a double response. A changed amount stops the whole
batch instead. Success is confirmed by re-querying the API, never by the click
appearing to work.

## Known limits

- **Change order packages cannot be gate-checked.** The workflows endpoint
  returns a 400 for `ChangeOrderPackage`, so whether you can respond is unknown.
  They are shown with their arithmetic verified but no response buttons, and a
  button to go resolve the gate.
- The open items grid is virtualised and cannot be scraped; everything comes
  from the REST API.
