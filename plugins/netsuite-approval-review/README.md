# NetSuite approval review

Reviews everything sitting in your NetSuite approval queue and publishes the
results to a dashboard you can act from, so approvals stop meaning a trip
through the NetSuite UI.

## What it does

For every bill and change order awaiting your approval:

- ties the PDF total and every line to the NetSuite record
- re-derives the arithmetic on AIA-style pay applications and phased
  professional-services invoices
- judges whether the support actually identifies what was done, for what
  period, at what rate
- pulls the real funding purchase order and the engagement's billing history
  to catch duplicates, missing intermediate applications, and over-commitment
- publishes a clear or flagged verdict per item to a dashboard, with the
  figures visible without clicking into anything

The dashboard is a snapshot and shows its own age, warning once it passes
three hours; a re-run button refreshes it in one click. Every record is
re-verified against the live queue at execute time, immediately before it is
clicked, so an item actioned since the review is skipped rather than clicked
twice.

You mark approve / approve with notes / reject per item, then execute them
together. Execute sends the instruction straight into the conversation in one
click. Nothing reaches NetSuite from the dashboard itself — the approvals run
from that message. Execution drives the real NetSuite buttons through your own
authenticated browser session, so the approval workflow routes normally and the
audit trail records you as the approver.

## Support is read without downloading anything

NetSuite's own `download` link does nothing under automation, and `preview` opens
a popup that freezes the tab. The plugin instead fetches the attachment from
inside your authenticated NetSuite tab and extracts the text there, so nothing
lands in your downloads folder and there are no stale files between runs.

Invoice tables keep their column alignment, because the text is rebuilt from the
PDF's own geometry rather than flattened into a single line — which is what the
quantity x rate and line-tie checks read.

## Every approval it makes says so

An approval executed by the plugin carries the note **"Approved by Claude"**,
recorded in NetSuite against that document. If you type your own note for an
item, yours is used instead, verbatim.

This is deliberate. An approval recorded with no note reads as though you clicked
it by hand; the attribution keeps the trail honest about what actually performed
the click. Rejection reasons are never defaulted — those always come from you,
and the plugin stops and asks if one is missing.

## Requirements

- A NetSuite MCP connector connected in Cowork. The plugin only ever reads
  through it — approvals go through the real NetSuite buttons in your browser, so
  the workflow routes normally and the audit trail records you.
- **The connector runs on a separate, Claude-enabled NetSuite account** — a second
  account issued on top of your usual one. **A normal NetSuite login is not
  connector access.** If you were never given a second account you do not have
  this yet: check your email for a Compass invitation to add the NetSuite MCP
  connector, and contact IT if there isn't one.
- **Keep the browser on your normal account when approving.** The Claude-enabled
  account is for reading. Both the queue and the approve buttons are role-scoped,
  so in the wrong account you'll see a queue that isn't yours, or a record with no
  buttons on it.
- Claude in Chrome, signed in to NetSuite
- A connected workspace folder for state (attachments are never downloaded)
- **The machine on and Chrome open whenever it runs.** Claude works through your
  real browser session, so a scheduled run needs the computer awake, Chrome
  running, and you still signed in. A missed window does not queue up and run
  later — which is why the schedule is worth giving more than one fire time.

## First run

Say "run my approval check". Setup happens once, automatically:

1. Looks up your NetSuite employee internal id from your email and asks you to
   confirm the name it found
2. Records which connector it is calling
3. Asks which dashboard portlet holds your bills
4. Copies its template and publish script into your workspace folder

Nothing is shared between people. Your employee id, connector and state stay
local to your install.

## Safety

The plugin never approves or rejects on its own judgement. A verdict is a
recommendation. It clicks an approval button only when you name specific
documents, and it confirms the document number, vendor and amount on the record
before clicking. If any item in a batch cannot be confirmed, it stops rather
than continuing.

It never writes to NetSuite through the connector.

## Known limits

- **Change orders cannot be live-checked.** Their records carry no approval
  status or next-approver field, so no query can identify the ones awaiting
  you. They come from the dashboard portlet and are labelled "as of last
  review".
- Employee records can share an email address, so setup confirms the name
  rather than trusting the lookup.
