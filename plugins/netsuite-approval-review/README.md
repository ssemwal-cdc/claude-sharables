# NetSuite approval review

Reviews everything sitting in your NetSuite approval queue. Publishes the
results to a dashboard you can act from. Approvals stop meaning a trip through
the NetSuite UI.

## What it does

It takes every bill, purchase order and change order awaiting your approval,
and for each one it:

- ties the PDF total and every line to the NetSuite record
- re-derives the arithmetic on AIA-style pay applications and on phased
  professional-services invoices
- judges whether the support identifies what was done, for what period, at
  what rate
- pulls the real funding purchase order and the engagement's billing history,
  where a NetSuite connector is available, to catch duplicates, missing
  intermediate applications and over-commitment
- publishes a clear or flagged verdict per item to a dashboard, with the
  figures visible without clicking into anything

Purchase orders are reviewed. Their execute route has never fired against a
real purchase order. See G‹po-execute-route-unfired›, PO execute route
unfired.

The dashboard is a snapshot and shows its own age. It warns once the snapshot
passes 3 hours. A re-run button refreshes it in one click.

Every record is re-verified at execute time, immediately before the click. An
item actioned since the review is skipped rather than clicked twice. The skip
is written to the review log and named in the run report. Bills and purchase
orders are re-checked by query. Change orders carry no approval-status field,
so they are re-checked by reading the record page. The approval buttons appear
there only while the item is still pending and still yours.

You mark approve, approve with notes, or reject per item. Then you execute them
together. Execute sends the instruction straight into the conversation in one
click. Nothing reaches NetSuite from the dashboard itself. The approvals run
from that message. Execution drives the real NetSuite buttons through your own
authenticated browser session. The approval workflow therefore routes normally,
and the audit trail records you as the approver.

## Support is read without downloading anything

NetSuite's own `download` link does nothing under automation. That is observed.
`preview` opens a popup, and the tab froze once after it. The recovery for a
frozen tab has never fired. See G‹freeze-fallback-unfired›, freeze fallback
unfired.

The plugin fetches the attachment from inside your authenticated NetSuite tab
and extracts the text there. Nothing lands in your downloads folder. No stale
files survive between runs.

Invoice tables keep their column alignment. The text is rebuilt from the PDF's
own geometry rather than flattened into a single line. That alignment is what
the quantity x rate and line-tie checks read. Verified against fixtures and one
live bill. See G‹pdf-geometry-mock-verified›, PDF geometry fixture-verified.

Support that is not a PDF is handled as what it is. It is not forced through
the PDF reader. Spreadsheets are read sheet by sheet, hidden sheets included.
Images and scanned pages are looked at rather than text-extracted, because
extraction returns nothing useful for them.

A file that cannot be read is named rather than filed as "unreadable". That one
word covered a scan, a workbook and an expired link equally well. Whole formats
went unreviewed and nobody noticed.

## Every approval it makes says so

An approval the plugin executes carries the note **"Approved by Claude"**,
recorded in NetSuite against that document. Your own note for an item replaces
it verbatim. Rejection reasons are never defaulted, and the plugin stops and
asks if one is missing.

An approval recorded with no note reads as though you clicked it by hand. See
D‹approved-by-claude-comment›, Approved by Claude comment.

## Requirements

- **Claude in Chrome, signed in to NetSuite.** That is the requirement.
- **A connected workspace folder is recommended, not required.** The run
  records what it reviewed there, and reads it back to know a day is already
  done. A run without the folder works. See F‹folderless-run-works›,
  folderless runs work.
- **A NetSuite MCP connector is optional.** It makes the review faster and
  broader. With it, the queue and every record's lines come back in two bulk
  queries instead of a tab per record. Each item is also cross-checked against
  its funding purchase order and the engagement's billing history, to catch
  duplicates, sequence gaps and over-commitment. Without it the review runs
  from the dashboard portlets and the record pages. Every arithmetic check,
  every attachment read and every approval is identical, because none of those
  ever used the connector.
- **The connector runs on a separate, Claude-enabled NetSuite account.** It is
  a second account issued on top of your usual one. A normal NetSuite login is
  not connector access. If you were never given a second account, you do not
  have this. Check your email for a Compass invitation to add the NetSuite MCP
  connector. Contact IT if there is no invitation. It is worth doing, but do
  not wait on it to start using the plugin.
- The plugin only ever reads through the connector. Approvals go through the
  real NetSuite buttons in your browser, so the workflow routes normally and
  the audit trail records you.
- **Keep the browser on your normal account when approving.** The
  Claude-enabled account is for reading. The queue and the approve buttons are
  both role-scoped. In the wrong account you see a queue that is not yours, or
  a record with no buttons on it.
- **The machine on and Chrome open whenever it runs.** Claude works through
  your real browser session. A scheduled run needs the computer awake, Chrome
  running, and you still signed in. A missed window does not queue up and run
  later. That is why the schedule is worth more than one fire time.

## First run

Say "run my approval check". Setup happens once, automatically:

1. Checks whether a NetSuite connector is available, and records which one
2. Asks which dashboard portlet holds your bills
3. Looks up your NetSuite employee internal id from your email, where a
   connector is available, and asks you to confirm the name it found. Without a
   connector this step is skipped. The portlets are saved searches already
   scoped to whoever is signed in, so the queue is yours with no id to
   configure
4. Copies its template and publish script into your workspace folder

The connector check runs on every review, not just the first. Getting
provisioned later therefore needs no reconfiguration. A connector that stops
resolving does not stop the review.

An expired connector session is noticed. The review then runs without the
connector and tells you once, so you can reconnect. A stale session takes
seconds to fix, unlike never having been provisioned.

The review never reports an empty approval queue because a query failed to
answer. A call that errors is treated as no connector, never as "nothing
pending".

Nothing is shared between people. Your employee id, your connector and your
state stay local to your install.

## Safety

The plugin never approves or rejects on its own judgement. A verdict is a
recommendation. It clicks an approval button only when you name specific
documents. It confirms the document number, the vendor and the amount on the
record before clicking. If any item in a batch cannot be confirmed, it stops
rather than continuing.

It never writes to NetSuite through the connector.

## Versioning

The skill's version is the `**Skill version N — date.**` line at the top of its
`SKILL.md`. That line is the first thing shown when you open the skill. The
authoritative current number is the Version column of the
[repo README on GitHub](https://github.com/ssemwal-cdc/claude-sharables). That
table does not ship with the plugin, so compare there, never against an
installed file.

`plugin.json` carries no `version` field. Do not add one, and do not suggest
adding one. See D‹no-version-field›, no version field.

## Known limits

- **Change orders cannot be live-checked.** Their records carry no approval
  status and no next-approver field, so no query can identify the ones awaiting
  you. They come from the dashboard portlet, labelled "as of last review".
- Employee records can share an email address. Setup therefore confirms the
  name rather than trusting the lookup.
