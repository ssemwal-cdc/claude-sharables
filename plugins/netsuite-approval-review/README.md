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

## Requirements

- A NetSuite MCP connector connected in Cowork (read-only is sufficient and
  preferred — the plugin never writes through the connector)
- Claude in Chrome, signed in to NetSuite
- A connected workspace folder for state and downloaded attachments

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
