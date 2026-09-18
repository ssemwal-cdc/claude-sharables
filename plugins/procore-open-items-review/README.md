# Procore open items review

Reviews the Procore items genuinely waiting on your workflow response.
Publishes the results to a read-only dashboard.

The hard part is not the review. It is working out which of your open items
actually need you. Procore's My Open Items list mixes things awaiting your
response with things you are merely on the distribution list for. This plugin
separates them.

## What it does

For every item in your queue it checks `user_permissions.can_respond` on the
live workflow. Items you cannot action are counted and suppressed, not shown.
It narrows the queue to the items that need a person to decide.
It drops the rest with a clear paper trail for why.

For the ones that remain:

**Subcontractor invoices.** It re-derives all six AIA G702 identities from the
record rather than reading the summary back. It foots every G703 line. It
checks retainage consistency and application sequence against the previous
requisition. It then locates each headline figure in the attached pay
application.

**Internal change risks.** It ties Cost Impact to the accepted cost, and the
accepted cost to the total on the attached proposal. It foots the proposal's
own phase lines. This catches placeholder values that pass a naive
has-a-value check.

**Commitment change orders.** It foots line items to the package grand total
and ties each attached PCI to a line.

**Commitments.** These are the purchase order and work order contracts
themselves. They come to you for approval before execution. The
plugin foots the schedule of values to the contract total. It finds that total
in the attached agreement or bid tab. It names duplicated and unpriced lines
and reports the retainage. It also points out anything else in the same queue
drawing on the same contract.

Commitments get the mechanical checks only. A change order or an invoice
arrives with the contract already agreed. The review is then arithmetic
against a fixed baseline. A commitment out for approval is the baseline itself. Whether
the scope, the rate and the counterparty are the right ones is left to you.

Each item lands as clear, flagged, skipped or gate-unknown. Skipped is a real
verdict. An item with no support attached is not ready for review. So it is not
approved, not rejected, and not given a verdict it has not earned.

## Support is read without downloading anything

Procore attachments sit behind a presigned S3 link, timed by Procore, not by
this plugin. `unmeasured`. See D24, do not overrun the window. The browser's PDF
viewer exposes no text and cannot be scripted. The storage host blocks
cross-origin reads. The plugin routes around all three and reads the file
in-browser, so nothing lands in your downloads folder.

It checks what the file actually is before reading it, rather than assuming:

- **PDFs** are parsed for text.
- **Spreadsheets** are read sheet by sheet, hidden sheets included. The formats
  are `.xlsx`, `.xls` and `.csv`. A superseded figure is exactly the thing that
  gets hidden rather than deleted.
- **Images**, and PDFs that turn out to be scans, are looked at rather than run
  through text extraction. Extraction returns nothing useful for them.

A file it cannot read is named, not silently skipped. That distinction is the
point. Anything that was not a PDF used to be reported as "support present but
unreadable". That phrase reads identically whether the file was a scan, a
spreadsheet or a link that timed out. Entire formats went unreviewed with
nothing in the log to show it. The reason is now specific enough to act on.

Execute mode was retired on 2026-09-18. Its prose and code sit in
`actionable-retired/` at the repo root.

## The dashboard

Verdicts render as an inline dashboard widget in the conversation. It carries
summary cards, a fact strip per item you can judge without expanding anything,
and sort and filter controls. The filter axes are campus, then building, then
type, plus search.

The dashboard is a read-only page. It shows the row, the details and the
verdict pill per item. It does not carry buttons or send anything to Procore.
You act on an item in Procore itself.

The controls and the floating header were measured in a browser. Nobody has
seen them in the widget host. See G12, widget host
unseen.

## Requirements

- **Claude in Chrome, signed in to Procore.** That is the requirement.
- **A connected workspace folder is recommended, not required.** It holds the
  review state between runs. A run without the folder works. See
  F76, folderless runs work.
- **No connector.** Procore has no MCP connector. The dashboard is therefore a
  snapshot, with a prominent re-check control rather than a live view. It says
  so plainly and ages its own timestamp.
- **The machine on and Chrome open whenever it runs.** Everything here goes
  through your real browser session. A scheduled run needs the computer awake,
  Chrome running, and you still signed in to Procore. A missed window does not
  queue up and run later. A maintainer report confirmed this
  (F147, missed window confirmed). That is why
  the schedule is worth more than one fire time.

## First run

Say "run my Procore review". Setup happens once. It asks you to confirm your
company id. Then, for each custom tool your queue draws change items from, it
asks for that tool's id. It also asks for its cost custom field mapping. All of
those differ per company, and the field mapping differs per tool as well.

More than one custom tool is normal. Every run reconciles the tools it finds in
the queue against the ones it has been told about. A tool it has not seen
before is set up then and there, and named in the run report. A tool it cannot
resolve is still reviewed and still shown. That tool's items carry no
record link and cannot come back `clear`. The cost fields those checks
read are mapped per tool.

There is no user id to configure. Procore's queue endpoint and permission gate
are both scoped to the signed-in session, so the review is automatically yours.

## Safety

The plugin is read-only. A verdict is a recommendation, not an action.

## Versioning

The skill's version is the `**Skill version N — date.**` line at the top of its
`SKILL.md`. That line is the first thing shown when you open the skill. See
the Version column of the
[repo README on GitHub](https://github.com/ssemwal-cdc/claude-sharables) for
the authoritative current number. That table does not ship with the plugin.
Compare there, never against an installed file.

`plugin.json` carries no `version` field. Do not add one, and do not suggest
adding one. See D9, no version field.

## Known limits

- **Change order packages are read before they are gated.** The workflows
  endpoint returns a 400 for `ChangeOrderPackage`. The workflow belongs to the
  underlying commitment change order rather than to the package. That record
  has its own id, carried on the package payload at `line_items[].holder.id`.
  Change orders therefore gate and respond like anything else. It only means
  the package is fetched before the gate runs rather than after it. Observed
  2026-08-14 against 5 packages. See F18, CCO holder id
  route.
- **The gate fan-out has not been observed against real Procore.** See
  G9, gate fan-out unobserved.
- If the change order id cannot be resolved, the item is shown with its
  arithmetic verified. It has no response buttons. It gets a button to go
  resolve the gate. The same applies when the package spans several change
  orders, because then no single id can stand for it.
- The open items grid is virtualised and cannot be scraped. Everything comes
  from the REST API.
