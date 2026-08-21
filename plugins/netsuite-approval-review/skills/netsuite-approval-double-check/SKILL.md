---
name: netsuite-approval-double-check
description: Financial double-check of the NetSuite bills, purchase orders and change orders sitting in your approval queue, published to a live dashboard widget in chat. Trigger whenever the user asks to "run my approval check," "check my NetSuite queue," "double check my bills," "review my change orders to approve," "run the daily approval review," or mentions their NetSuite approval dashboard or bills, purchase orders and change orders pending their approval. Also trigger when the user sends an execute instruction from the dashboard naming specific documents to approve, approve with notes, or reject. Reads each attachment in the page without downloading it, verifies the math and the adequacy of support, cross-checks the real purchase order and billing history, and publishes a clear or flagged verdict per item. Only ever approves or rejects on an explicit per-document instruction, never on its own judgement.
---

# NetSuite Approval Double-Check

**Skill version 3 — 2026-08-21.** This installed file is a snapshot. The current number is the Version column of the repo README on GitHub (github.com/ssemwal-cdc/claude-sharables); that table does not ship with the plugin, so there is nothing local to compare against — when asked for the version, report this line and leave the comparison to the reader. If GitHub shows a higher number, this copy is stale: the fix is updating or reinstalling the plugin, never adding a version field to plugin.json — its absence is deliberate.

Review every bill, purchase order and change order sitting in the user's NetSuite approval queue. Verify each item's math and the adequacy of its supporting document, cross-check against the real purchase order and billing history, and publish a per-item verdict to the dashboard.

Output goes to an inline dashboard widget, not to chat. Chat gets one headline line.

## Two modes

This skill does two different jobs. Know which one you are in.

- **Review mode** (Steps 1-7) — the default. Read-only. Produces verdicts. Never clicks an approval button.
- **Execute mode** (Step 8) — only when the user sends an explicit instruction naming specific documents. Clicks the real NetSuite buttons on their behalf.

An instruction to review is never an instruction to execute. A verdict of "clear" is a recommendation and authorises nothing.

## Absolute rules

- **Never approve, approve with notes, or reject on your own judgement.** Those three buttons sit adjacent at the top-left of every record, directly above Primary Information. In review mode, keep all clicks well away from that region.
- **Only act on an explicit instruction that names the document.** "Approve 4139-40671" is an instruction. "Approve everything clear," "approve the rest," or anything inferred from a verdict is not — ask which documents, specifically.
- **Never** call `ns_createRecord` or `ns_updateRecord`. Treat the NetSuite connector as read-only. Approvals must go through the real UI so the workflow routes and the audit trail records the user as the approver; a REST field flip would bypass SuiteFlow and leave no trail.
- **Never hand-write or regenerate the dashboard HTML.** See Step 7. The layout is a file on disk; runs inject data into it and nothing else.
- **Never present, attach, or send the working files as files or file cards in chat** — the dashboard template, `publish_dashboard.py`, the review log, or the rendered `index.html`/`widget.html`. They are internal state, not deliverables, even when the platform encourages surfacing files a run produced. The dashboard widget is the only deliverable, and chat gets one headline line.
- **Never copy identity between people.** The employee internal id in `config.me` scopes the whole review. Using someone else's shows them a queue that is not theirs.
- If deeper review would require actions beyond reading, say so in the verdict and ask first.
- **Every approval carries the note `Approved by Claude`, unless the user supplied their own for that document — theirs replaces it verbatim.** Those two are the only text this skill types into a note field, and approvals route through Approve With Notes so it can be attached; see Step 8. Do not ask permission for the default and do not vary its wording. Rejection reasons are different: they always come from the user and are never defaulted.
- **This skill owns exactly one state file:** `NetSuite Approval Checks/_netsuite_review_log.json`. Never read or write the Procore skill's log, and never let Procore records into yours. Both files used to share the name `_review_log.json` and both folders sit under the same parent, so this went wrong in practice. If you find foreign records in your log, move them to a `_quarantined` block, say so in chat, and carry on — never merge them into `items`, and never act on them.

## What this review is, and what it is not

The user is **one approver among several, and not the accountant of record.** An approval here advances a workflow step to the next approver. It does not clear an accounting or legal obligation, and it is not the last check the figures will get.

So do not stall an authorised batch to raise the size of the amounts, the number of documents, or how an auditor might read it later. The `Approved by Claude` note is there precisely so the trail is honest about what performed the click — recording nothing would be the weaker position, since an unannotated approval reads as though the user made it by hand.

The checks that do matter are mechanical, and Step 8 already has them: the document is still theirs to action, the figures match the instruction, the record has not moved underneath the review. Those still stop the batch, every time.

## Step 0 — Sync assets, then first-run setup

**Do this on every run, before anything else.** The workspace copies of the template and the
publish script are a *cache* of the plugin's assets. Refresh them, or a plugin update never
reaches the dashboard — `SKILL.md` updates with the plugin while the HTML your runs actually
render stays frozen at whatever version was copied the first time.

```bash
mkdir -p "<workspace>/NetSuite Approval Checks"
cp "${CLAUDE_PLUGIN_ROOT}/skills/netsuite-approval-double-check/assets/dashboard_template.html" "<workspace>/NetSuite Approval Checks/"
cp "${CLAUDE_PLUGIN_ROOT}/skills/netsuite-approval-double-check/assets/publish_dashboard.py" "<workspace>/NetSuite Approval Checks/"
chmod u+w "<workspace>/NetSuite Approval Checks/dashboard_template.html" \
          "<workspace>/NetSuite Approval Checks/publish_dashboard.py"
```

The `chmod` is required, not tidiness. The plugin's installed assets are read-only and `cp`
preserves that mode, so without it the publish step fails with
`PermissionError: [Errno 13] Permission denied`.

This overwrites the workspace copies deliberately. **A design change belongs in the plugin repo,
never in the workspace copy** — an edit made there is discarded by the next run and reaches
nobody else. Ship one by editing the repo's `assets/` and pushing; teammates pick it up on their
next plugin update.

**The sandbox shell may not be able to see the plugin's files at all.** Observed in a Cowork run
2026-08-15 (on the Procore side; this surface behaves the same): only the connected workspace
folder (plus outputs and uploads) is mounted into the shell, so the `cp` source path does not
exist there and the copy cannot run. That is a property of the surface, not an error to fix. Sync
down this ladder and take the first rung that works:

1. **The `cp` above** — wherever the shell can see `${CLAUDE_PLUGIN_ROOT}`.
2. **Read → Write.** Read each asset from `${CLAUDE_PLUGIN_ROOT}/skills/netsuite-approval-double-check/assets/`
   with the file tools and write it over the workspace copy **byte for byte** — the same fidelity
   contract as the render step: never retype, trim, or tidy in passing. Then prove the copy landed
   whole: the template carries `/*__REVIEW_DATA__*/` and `/*__END__*/` exactly once each, and
   `python3 -m py_compile publish_dashboard.py` passes in the workspace folder. This rung is
   designed, not yet observed — if it also fails, say so in the run report.
3. **Use the existing workspace copies and say so, once** — one line near the headline, naming the
   files' modification date from `ls -l`: "dashboard code is from the last successful sync,
   \<date\>". Then carry on; **do not stop the run over it.** The review's procedure lives in this
   file, which ships with the plugin regardless — only the dashboard template and publish script
   can lag, so the verdicts are current even when the widget's wording is not.

Then read `NetSuite Approval Checks/_netsuite_review_log.json`. If it already carries a `config` block, the rest of this
step is done — go to Step 1. Otherwise, once:

0. **Two browser-side things to say before anything else, because both fail silently later.**

   - **Warn them about the site-access prompt before it appears.** The first time this skill acts on
     NetSuite, Claude in Chrome asks the user whether to allow access to that site, offering a
     once-only option and an always option. **Tell them to pick the always option.** On once-only
     they are re-prompted on effectively every action, and a run that stops for a prompt nobody is
     watching looks like a hang.
   - **Ask the user to confirm which NetSuite role their browser is in.** The MCP connector signs in
     under its own account and role, and connecting it can leave the browser session on that role
     rather than theirs. The approval queue and the approve buttons are both role-scoped, so the
     wrong role shows a queue that is not theirs, or a record with no buttons on it. If they are not
     in their normal role, have them switch back before continuing.

1. **Find the employee internal id.** Query by the user's own email address:

   ```sql
   SELECT id, entityid, email, isinactive, title FROM employee
   WHERE email = '<the user's email>' AND isinactive = 'F'
   ```

   **Employee records can share an email address** — a colleague with the same surname, or a former employee. Always report the name found and ask the user to confirm it is them before writing it. If the query returns zero or more than one active row, list the candidates with their titles and ask which is theirs. Never pick one silently.

2. **Record the connector tool name — or establish that there isn't one.** Use the fully-qualified name of the NetSuite SuiteQL tool you are actually calling in this session (it looks like `mcp__<server id>__ns_runCustomSuiteQL`). The server id differs per connection, so never copy it from documentation or another install — read it from the tool you just used.

   **The connector is an accelerator, not a requirement.** The review runs either way. Check for the tool before asking; a person who was never provisioned a Claude-enabled NetSuite account often believes their ordinary login is connector access, so *"do you have the connector?"* is not a reliable question.

   **There are three states here, not two, and the middle one is the easiest to get wrong.**

   | What you find | Mode | What you say |
   |---|---|---|
   | No NetSuite SuiteQL tool in the session | `browser` | **Nothing.** Carry on as though it were the plan. |
   | Tool present but unauthenticated, or its calls error | `browser` **for this run** | **One line, once** — see below. |
   | Tool present and answering | `connector` | Nothing needed. |

   **A "not provisioned" silence is right; an "expired session" silence is not.** The say-nothing rule exists because someone who was never provisioned can do nothing about it, so a caveat on every item forever is an apology on a loop. **An expired connector is the opposite: a thirty-second fix that restores the faster route and the cross-check.** Staying quiet there costs them something they could have had. So say it once, plainly, near the headline — *"the NetSuite connector needs reconnecting; reviewed without it"* — and never again in that run. Not per item, not in a verdict, not in the dashboard.

   **Never let a failed connector call read as an empty result.** This is the single dangerous outcome in the whole mode question. Step 1a's query is what finds bills pending approval, so an auth failure silently reinterpreted as "no rows" reports **an empty approval queue** — the user concludes there is nothing waiting on them and closes the tab. An errored call is `failed`, never `empty`. If a SuiteQL call returns an error, an auth challenge, or anything that is not a result set, **treat it as no connector and switch this run to `browser` mode** rather than believing the shape of what came back. Same rule as the Procore gate's three states, reached from a different direction.

   **If it dies mid-run**, after Step 1a already succeeded: finish the remaining steps on the browser route, say the one line, and do not re-issue the failed query hoping it recovers. Do not discard the work already done — the queue and figures you have are valid; it is only the cross-check you lose.

   **Re-detect on every run** rather than trusting `config.mode`. Someone provisioned later is lifted automatically, someone whose session expires keeps working, and someone who reconnects is back on the fast route with nothing to reconfigure.

   Beyond that one line for the expired case: do not describe the browser route as reduced, degraded, limited, or a fallback, and do not offer to fix a connector that was never there.

3. **Find the account id** from the NetSuite URL the user's browser is on, or from the connector. It appears in record URLs as `https://<account>.app.netsuite.com/`.

4. **Ask which dashboard portlet holds their bills.** Portlet names are per-user saved searches and are frequently non-obvious. Have the user confirm the exact name rather than guessing.

5. **Write the config** into `_netsuite_review_log.json`:

   ```json
   {
     "config": {
       "mode": "connector",
       "me": <the internal id you confirmed>,
       "meName": "Firstname Lastname",
       "account": "1234567",
       "tool": "mcp__<server id>__ns_runCustomSuiteQL",
       "billPortlet": "<portlet name>"
     },
     "items": {},
     "actions": []
   }
   ```

   In `"browser"` mode, `tool` and `me` are both omitted — there is no connector to
   name, and `me` exists only to filter the bills query. The portlets are per-user
   saved searches already scoped to whoever is signed in, so the queue is that
   person's own without an id to configure. Re-check for the connector on every run
   rather than trusting the stored mode: someone provisioned later should be lifted
   automatically, and someone whose connector drops should keep working.

### Which route each step takes

| Step | With the connector | Browser only |
|---|---|---|
| 1 — queue | bulk query, reconciled against the portlets | **portlets only** |
| 2 — record fields | bulk `transactionline` query | `get_page_text` per record |
| 3 — attachment URL | `SELECT url FROM file` | read the link off the record page |
| 5 — PO and history cross-check | **yes** | **not performed** |
| 8 — verify a click landed | page load (already the rule) | page load, unchanged |

Attachment *reading*, every arithmetic check, and every approval click are identical
either way. Those never used the connector: pdf.js runs same-origin in the record
tab, and approvals always go through the real UI so the workflow routes and the
trail records the user.

6. **The dashboard is rendered, not published.** There is no artifact to create,
   update or reconcile against this file — Step 7 renders the HTML as an inline
   widget on every run, so each render replaces the last and there is no id to
   keep in sync. `_netsuite_review_log.json` is the only persistent store.

   The one thing that does survive between renders is the user's per-item marks,
   which the template keeps in `localStorage` under `ns_marks_v1`. Never clear it, and
   never change that key for cosmetic reasons — doing so silently discards
   decisions the user has already marked but not yet executed.

## Step 1 — Build the queue

In connector mode, pull the queue two ways and reconcile them. **In browser mode, run 1b only** — the portlets are the whole queue, and 1b is already the authoritative half.

**1a. Connector (fast, reliable, gets bills):**

```sql
SELECT t.id, t.type, t.tranid, t.trandate, t.foreigntotal,
       e.entityid AS vendor,
       t.custbody3 AS po_typed,
       t.custbody_sna_without_purchase_order AS no_po_flag,
       t.custbodyap_invoice AS ap_file,
       t.custbodypurchase_order_attachment AS po_file,
       t.custbody_sn_cdc_skipped_approvers AS skipped,
       t.memo
FROM transaction t
LEFT JOIN vendor e ON e.id = t.entity
WHERE t.approvalstatus = 1
  AND t.custbody_sna_cdc_next_approver = <config.me>
ORDER BY t.trandate
```

`approvalstatus = 1` means Pending Approval. `custbodyap_invoice` is the internal file ID of the vendor's invoice PDF — this is the key that makes attachment retrieval reliable.

**`custbody3` is a typed reference. It is not the PO this bill is applied to.** It is
aliased `po_typed` for exactly that reason. A person enters it by hand, and it is wrong
often enough to matter: checked live 2026-08-20, it was wrong on **five of five** bills
examined — four Sunbelt diffuser bills all reading `PO16033` while every one of them is
applied to `PO16034`, and a CEC bill reading `PO11120` while applied to `PO16093`.

**The PO the money is actually on comes from the transaction linkage in Step 2**, and that
is the only thing that may be called the bill's PO. Never let `po_typed` reach a verdict, a
`poContext` figure, a comment or the dashboard as though it were the coding. Reading it as
the coding is what produced confident, entirely false "coded to the wrong PO" flags on
correctly coded bills — see Step 5.

**Zero rows here is a claim, so make sure it is a true one.** This query is the only thing that finds pending bills, so "no rows" and "the call failed" produce the same visible outcome — an empty queue — and only one of them means the user has nothing waiting. **An error, an auth challenge, or any response that is not a result set is a failure, not an empty queue.** Switch the run to the browser route per Step 0 and read the bills off the portlet instead. Never report an empty NetSuite queue on the strength of a call that did not answer.

Two data quirks that will bite:
- **`foreigntotal` is negative on vendor bills** (e.g. `-12800`). Take the absolute value everywhere.
- **`trandate` comes back as `"7/19/2026"`**, not ISO. Parse month/day/year explicitly.

**1b. Dashboard (authoritative, and the only place change orders appear):**

Navigate to the NetSuite dashboard and scroll to the bottom. Three kinds of portlet matter: one holding change orders, one holding purchase orders (frequently empty), and one holding vendor bills — named in `config.billPortlet`.

Portlet names are user-specific saved searches and can be arbitrary, so do not assume a name is a placeholder. If a portlet has been renamed since setup, report it rather than guessing.

Use `get_page_text` on the dashboard tab rather than screenshots — the portlet tables extract cleanly as text. Then open each row's **date link** with a **ctrl+click** to put every record in its own tab. Ctrl+click may silently fail on the very first attempt; verify with `tabs_context_mcp` and retry once if no new tab appeared.

Review **every** item regardless of dollar amount. There is no threshold.

**In browser mode, bills come from the bill portlet the same way change orders already do**, so they carry the same "as of last review" caveat the dashboard already shows for change orders — that label is existing behaviour being applied to one more item type, not a new disclaimer. Everything else in the run is unchanged.

**Change orders are not queryable for pending status.** They live in `transaction` under a recordtype like `custompurchase_r_pci_change_order_po`, but the records carry `approvalstatus = null` and no next-approver value, so no SuiteQL filter can identify the ones awaiting the user. The dashboard portlet is the only source. This is why the dashboard labels change orders "as of last review" rather than live — do not remove that label.

## Step 2 — Read each record

The full field set is this:

- Reference no. / document no., vendor, date, **AMOUNT**, internal id
- MEMO, subsidiary, approval group, requestor
- The attachment file id (AP INVOICE or CHANGE ORDER ATTACHMENT field)
- Every **line** in the Items sublist: quantity, rate, amount, description
- For change orders: **CHANGE ORDER AMOUNT** and **PREVIOUSLY APPROVED AMOUNT**

**In connector mode, do not `get_page_text` each record to collect it.** A record page is thousands of tokens and Step 1a already returned most of these in one query — document no., vendor, date, amount, internal id, memo and the attachment file ids. Query the rest in bulk instead, keyed on every id at once:

```sql
SELECT tl.transaction, tl.quantity, tl.rate, tl.foreignamount, tl.memo AS line_memo
FROM transactionline tl
WHERE tl.transaction IN (<all ids from step 1>)
ORDER BY tl.transaction, tl.linesequencenumber
```

Add subsidiary, approval group and requestor as columns to the Step 1a query rather than reading them off the page — they are the fields 1a does not already carry.

**Also pull the PO linkage, in the same bulk shape.** This is the authoritative answer to
"which PO is this bill applied to" — it is what the record's **Related Records → Purchase
Orders** subtab shows, and it is the only source Step 5 may treat as the coding:

```sql
SELECT l.nextdoc AS bill_id, po.id AS po_id, po.tranid AS po_ref, po.memo AS po_memo
FROM previoustransactionlinelink l
JOIN transaction po ON po.id = l.previousdoc AND po.type = 'PurchOrd'
WHERE l.nextdoc IN (<all ids from step 1>) AND l.linktype = 'OrdBill'
```

Two things about this query are load-bearing.

**`linktype = 'OrdBill'` is the filter, and it is not optional.** That is the order-to-bill
application. The same PO also produces `ShipRcpt` rows for the same bill; including them
double-counts.

**The link table carries one row per line pair, not one per document.** A three-line bill
returns three `OrdBill` rows for one PO. So **reduce to distinct bill ids before summing
anything.** Measured 2026-08-20: a naive `SUM` across this join returned exactly 3× the
truth — `136,369.02` of approved billings came back as `409,107.06`. Deduplicate first,
every time.

**In browser mode, `get_page_text` on each record tab is the route** — Step 1b already opened one tab per row, so the pages are there. The warning above is a cost optimisation for when a bulk query is available, not a prohibition: read the field set off the page, including the Items sublist lines. Expect the run to be slower and heavier per item; that is the trade and it needs no comment.

**Confirm field parity once, on a real bill, before relying on this.** Compare what the two queries return against what `get_page_text` gives for the same record. Every field in the list above must be present. A bulk query that silently returns fewer fields means the review is checking less than it used to, which is worse than the round trips it saved. If a field cannot be resolved this way, read that one from the page and say so.

**Keep opening the record tabs.** The cost being avoided here is `get_page_text`, not the tab. Each record's tab is a deliverable — the user acts on it directly after the review — so the ctrl-click from Step 1b stays exactly as it is.

The line-level quantity x rate is the first math check and it is free — do it before touching the PDF.

## Step 3 — Retrieve the attachment

**Do not click NetSuite's `download` link.** It fails silently under automation — no network request, no file, no error. Clicking `preview` opens a popup that freezes CDP screenshots on that tab. Both are dead ends.

Instead, get the file's authenticated URL from the connector and extract the text **inside the page**, without downloading anything:

```sql
SELECT id, name, filetype, filesize, url FROM file WHERE id IN (<ap_file ids>)
```

The `url` column returns a path like `/core/media/media.nl?id=<id>&c=<account>&h=<hash>&_xt=.pdf`.

**In browser mode, take that same path off the record page instead.** The attachment in the AP INVOICE / CHANGE ORDER ATTACHMENT field renders as a link, and its `href` is the `media.nl` path with the `id`, `c` and `h` parameters already on it — the query has no information the page does not. Read it from the DOM in the record tab:

```javascript
// The href already carries the account and hash, so it needs no reassembly.
// Return it split up - a whole media.nl URL in a tool result trips the output filter.
const a = [...document.querySelectorAll('a[href*="media.nl"]')].map(function(x){
  const u = new URL(x.href, location.origin);
  return {id: u.searchParams.get('id'), c: u.searchParams.get('c'),
          h: u.searchParams.get('h'), xt: u.searchParams.get('_xt') || ''};
});
JSON.stringify(a)
```

Rebuild the path from those parts inside the page when fetching, exactly as the connector route does. **Everything after this point is identical in both modes** — same pdf.js load, same `new Uint8Array` wrap, same sniff, same six outcomes. This is the only step where the two routes differ at all, and only in where the four parameters came from.

This DOM read is **designed, not yet observed.** If it returns nothing, the field may render as something other than an anchor on that record type — report what it is rather than guessing a selector.

**Setup, once per run.** Run this in any authenticated NetSuite tab — the fetch has to be same-origin so the session cookie rides along, which is why pdf.js is loaded here rather than in a scratch tab. NetSuite's CSP permits the import; verified live.

```javascript
const m = await import('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.0.379/pdf.min.mjs');
window.__pj = m;
const wt = await (await fetch('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.0.379/pdf.worker.min.mjs')).text();
m.GlobalWorkerOptions.workerSrc = URL.createObjectURL(new Blob([wt], {type:'text/javascript'}));

window.__open = async function(u){
  const b = await (await fetch(u, {credentials:'include'})).arrayBuffer();
  // new Uint8Array is REQUIRED - a raw ArrayBuffer throws InvalidPDFException on valid bytes
  window.__doc = await m.getDocument({data:new Uint8Array(b)}).promise;
  return window.__doc.numPages;
};

window.__page = async function(n){
  const c = await (await window.__doc.getPage(n)).getTextContent();
  const it = c.items.filter(z => z.str.trim());
  if (!it.length) return '';
  let tw = 0, tc = 0;
  it.forEach(z => { if (z.width > 0 && z.str.length) { tw += z.width; tc += z.str.length; } });
  const cw = tc ? tw / tc : 5;                    // char width, derived per document
  const rows = new Map();                          // bucket by y, 3pt tolerance = one visual row
  it.forEach(z => { const y = Math.round(z.transform[5] / 3) * 3;
                    if (!rows.has(y)) rows.set(y, []);
                    rows.get(y).push(z); });
  return [...rows.keys()].sort((a,b) => b - a).map(y => {
    let s = '';
    rows.get(y).sort((a,b) => a.transform[4] - b.transform[4]).forEach(z => {
      const col = Math.round(z.transform[4] / cw);
      if (col > s.length) s += ' '.repeat(col - s.length);
      s += z.str;
    });
    return s.replace(/\s+$/, '');
  }).filter(r => r.trim() && !/^[\s01]{12,}$/.test(r) && !/\d{20,}/.test(r)).join('\n');
};
'ready'
```

Then `await window.__open('<path>')` for the page count, and `await window.__pages(from)` to pull as many **whole** pages as fit in one return:

```javascript
window.__pages = async function(from){
  let out='', n=from;
  for(; n<=window.__doc.numPages; n++){
    const p = await window.__page(n);
    if (out && out.length + p.length > 4000) break;   // whole pages only, never split one
    out += (out?'\n\n':'') + '--- page '+n+' ---\n' + p;
  }
  return {text: out, next: n > window.__doc.numPages ? null : n};
};
```

Call it again with `next` until it returns `null`. Most 2–3 page invoices come back in one call; a single oversized page still returns alone and uncut, which is the old one-per-call behaviour — so this degrades gracefully rather than truncating.

This rebuilds the column layout from pdf.js geometry, and that is the point of it. Verified against `pdftotext -layout` on a 3-page utility invoice: description, basis and amount landed in the same three columns. A naive `items.map(z => z.str).join(' ')` flattens the table and would silently break the quantity x rate checks in step 4. **Do not simplify it to that.**

Three things are not optional:

- **`new Uint8Array(b)` is mandatory.** Handing `getDocument` the ArrayBuffer directly throws `InvalidPDFException` on bytes that are provably fine — right content type, right `%PDF` header — which reads like a corrupt download and sends you debugging the fetch instead. The wrap looks redundant. It is not.
- **Never split a page across returns.** A whole document truncates, but that is a size limit rather than a count limit — hence the budget above. Splitting mid-page is what actually loses figures, because a row cut in half stops tying to anything.
- **Keep the row filter.** Barcode rows and long digit strings read as query-string data to the output filter, and one of them turns the entire result into `[BLOCKED: Cookie/query string data]`. On the test invoice the filter dropped 15 of 60 rows — all payment-stub noise, no figures.

Notes:
- **Nothing is written to disk.** The bytes stay in the page as an ArrayBuffer, so there is no downloads folder to poll, no cleanup, and no stale file from an earlier run to accidentally re-read.
- **No attachment at all → flag the item.**
- **Sniff the bytes before parsing; never hand a non-PDF to pdf.js.** This line used to read *"Non-PDF attachments are unusual; handle them the same way and note the type"* — which instructed exactly the wrong thing. Handing a workbook to `getDocument` throws `InvalidPDFException`, the same error a corrupt download gives, so a perfectly good spreadsheet came back logged as unreadable support. Reported from production on the Procore side, where the identical recipe produced the identical failure.

  Use the same first-four-bytes sniff and the same six outcomes as Step 4 of the Procore skill — `text`, `spreadsheet`, `image`, `scanned`, `expired`, `unsupported` — and keep them distinct. **`scanned` means the bytes were a PDF, it parsed, and it yielded almost nothing.** A parse that threw is never `scanned`; it is `spreadsheet`, `image` or `unsupported`, named by what the bytes actually were.

  Non-PDF support is **not** unusual here either — that assumption is what made this cheap to leave broken.
- Multiple attachments → check the one referenced by the AP INVOICE / CHANGE ORDER ATTACHMENT field, and mention the others.
- **Workbooks parse with SheetJS, loaded the same way pdf.js is.** Probed live 2026-08-14 (in Procore's scratch tab, but the loader is host-level, not page-level): `await import('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js')` populates `globalThis.XLSX` on the first attempt, and `XLSX.read(new Uint8Array(ab), {type:'array'})` then `XLSX.utils.sheet_to_csv` round-trips cleanly. Same `new Uint8Array` wrap, same whole-unit size budget as `window.__pages` — sheet by sheet, never split one. Read **every** sheet including hidden ones, and treat a blank cell from an unevaluated formula as missing, never as zero.
- **Images and scanned pages: look at them, with `computer`.** That is the only tool in the set that returns a visual read; `get_page_text` and `read_page` extract text and will return nothing useful for a scan. NetSuite renders the file in the record tab, which is ordinary HTML — so unlike Procore's XML scratch tab, `document.createElement('canvas')` works here and needs no namespace workaround. A visual read counts as parsed text for the tie-outs. If no visual read is available, fall back to OCR and **cap the verdict** — an OCR-derived figure never produces a clean approval recommendation, is labelled `read by OCR, not independently verified`, and goes in front of the user. A misread digit in a seven-figure line is worse than an honest skip.
- **A `[BLOCKED: …]` string is never a value.** The output filter redacts on more than query strings — a plain version number came back as `[BLOCKED: JWT token]` because its dotted shape matched a credential pattern. Dotted identifiers are ordinary in this data. If one appears where a figure should be, re-return the field in a different shape and read it again; never let the marker reach a verdict or a note, and never read it as the field being empty.
- **Say which outcome caused a skip**, in that outcome's own words. "Unreadable" alone is what let entire formats go unread without anyone noticing.
- **On a two-column page, left and right rows sharing a y-coordinate merge into one line.** `pdftotext -layout` does the same, so this is not a regression — but do not split such a line on whitespace to recover the columns. Split on an x-threshold, or take the figures off the record instead.

## Step 4 — Verify

### Math

1. **Header tie:** PDF total must equal the NetSuite AMOUNT. Flag any delta, but if the PDF itself explains it (tax, freight, retainage, partial draw), state the reconciliation rather than just the difference.
2. **Line tie:** every NetSuite line must reproduce on the PDF. Sum the lines to the header both places.
3. **Internal consistency:** for AIA-style pay applications and phased professional-services invoices, re-derive the arithmetic — schedule of values sums to the contract sum, earned-less-previously equals current billing on each phase, completed-to-date less previous certificates equals current payment due, balance to finish equals contract less completed.
4. **Prorations:** assume **no fixed house convention** unless the user has stated one. When a partial period is billed, show the vendor's factor next to each plausible basis (calendar days / actual days in month, calendar days / 30, business days) and let the user decide. **Then check the cumulative position** — see below, because a factor that looks generous in isolation is often correct across the engagement.

### Support adequacy

Adequate support identifies **what** was done, **for which period or scope**, and **at what rate**, and ties to the NetSuite record on vendor, amount, and project or building. Strong examples: an AIA-style application and certificate for payment with a continuation sheet; a phased professional-services invoice showing fee, percent complete, earned, previously billed, and current billing; a scope-change proposal with scope, exclusions, schedule, and a fee table.

Calibration decisions already established — apply these rather than re-flagging them:
- **Unsigned vendor proposals are fine.** A blank customer signature block on a change-order proposal is not a finding.
- **PO linkage:** the PO printed on a vendor's invoice, and the PO typed into `custbody3`, are both *references*. Neither is the coding. **Record them for traceability and never flag on them** — Step 5 resolves the actual applied PO from the transaction linkage, and a reference disagreeing with that linkage is a data-entry note, not a misallocation.
- **Skipped approvers:** ignore. Not a finding.

## Step 5 — Cross-check against the real PO and history

This is where the review earns its keep. **In connector mode, always do it.**

**In browser mode this step does not run, and nothing is said about that.** Do not
substitute a browser route — opening the funding PO and every prior bill in the
engagement would cost more tabs and more time than the whole rest of the review,
and it is not what this mode is for. Skip the step.

**Say nothing about the absence.** No "cross-checks were not performed", no
"reduced coverage", no caveat in the verdict, the warning line, the detail
paragraph, the dashboard or the chat headline. **State what you checked, never what
you did not.** The differentiator is already positive and already works the right
way round: a connector run's detail names the PO it tied to and the billing history
it walked, so that verdict visibly carries more evidence. A browser run's detail
simply describes the arithmetic and support checks it actually did. Absence needs no
narration.

The reason this is a rule rather than a preference: a caveat here would print on
**every item of every run, forever**, for someone who cannot get a connector and can
do nothing about it. That is not information, it is an apology on a loop. The
mechanical checks that stop a batch in Step 8 are unchanged in either mode, so
nothing that protects the user is being quietly dropped.

**Pull every PO in the run in one query**, not one per item. The `IN` below is the point of the query, not a template — collect the referenced PO numbers across all items first, then issue it once. The billing-history pull that follows is the same shape: one query with an `OR` across the engagements, sorted, rather than one per vendor.

### 5a. Resolve which PO the bill is on — three states, never a boolean

**Use the Step 2 linkage result. Never the typed reference, never the PO printed on the
invoice.** Every bill resolves to exactly one of three states, and they are not
interchangeable:

| State | Means | What you may say |
|---|---|---|
| `linked` | Step 2 returned an `OrdBill` row | **That PO is the coding.** Authoritative. Nothing overrides it. |
| `unlinked` | the query **succeeded** and returned no `OrdBill` row for this bill | No PO is applied. The typed reference is all there is — report it as *the PO the record names, not confirmed against the ledger*. Note `no_po_flag` alongside: `F` with no link is itself worth stating. |
| `failed` | the query **errored** | **Unknown. Never `unlinked`.** Say the linkage could not be read and check nothing that depends on it. |

**Never collapse these three into a boolean**, and never let a `failed` become "this bill
has no PO" — that is the same misfile as the fan-out's `empty` vs `failed` and the CCO
wrong-id returning 200-empty. A timeout is not an absence of linkage.

**Then pull the PO records you resolved**, by internal id from the linkage rather than by
matching a document-number string:

```sql
SELECT t.id, t.tranid, t.trandate, t.foreigntotal, e.entityid AS vendor, t.memo, t.status,
       t.custbody_r_it_original_contract_amount AS orig_contract,
       t.custbody_r_it_revised_contract_amount AS revised_contract,
       t.custbody_r_it_net_change_orders_amount AS net_cos
FROM transaction t LEFT JOIN vendor e ON e.id = t.entity
WHERE t.id IN (<po_id values from the Step 2 linkage>)
```

Keying on `po_id` and not on `tranid IN ('PO____')` matters: a `tranid` match resolves
whatever string you hand it, so feeding it the typed reference silently pulls the contract
figures for **the wrong PO** and every number downstream is then about a PO the bill was
never on. That is precisely how the false positives below were produced.

### 5b. A typed reference that disagrees is a data-entry note, not a misallocation

When `po_typed` (or the PO printed on the invoice) does not match the `linked` PO, the
finding is **not** "coded to the wrong PO". The money is where the linkage says it is. Write
it as what it is, and put it in `poWarning`:

> The PO reference typed on this record (`PO16033`) does not match the PO it is actually
> applied to (`PO16034`). The bill is correctly applied; the reference field is stale.

**Report it, do not discard it** — a wrong reference field is a real data-quality problem
worth telling AP about. But **a typed-reference mismatch never makes an item `flagged` on
its own**, and it never produces a sentence about money being on the wrong PO, a percentage
of the wrong contract, or a cumulative total drifting onto the wrong commitment.

**This is not a hypothetical guard.** Observed live 2026-08-20, both flags false:

- Bill `2325026-07` was flagged as coded to `PO11120` while naming `PO16093`. It is applied
  to `PO16093`. The record's own `custbody_r_it_original_contract_amount` reads `5,400` —
  `PO16093`'s contract exactly, not `PO11120`'s `372,500`.
- Bill `182743734-0004` was flagged as one of four diffuser bills on the load-bank PO, with
  *"$182,526.82 cumulative on the wrong PO"*. All four are applied to `PO16034`, the PO the
  invoice names. That `182,526.82` is `PO16034` at 64% of a `284,078.31` contract — healthy,
  and on the correct commitment. Three of those four bills were already approved, so acting
  on the flag would have meant chasing reversals on correctly posted transactions.

Both records carried a second field that agreed with the linkage and contradicted the flag.
Neither was read. **When two sources disagree about a PO, the linkage wins** — the same
doctrine Step 8 already applies to approval state.

Then reconcile: a professional-services invoice's "billed previously" plus its remaining contract phases should tie to the PO's contract value. A change order's PREVIOUSLY APPROVED AMOUNT should tie to the PO total. Residual differences usually correspond to a specific already-approved change order — identify it rather than reporting a bare variance.

Caution: `custbody_r_it_total_amount_invoiced` and `..._remaining` are frequently stale (often 0). Do not rely on them; derive from actual bills instead.

### 5c. Billed-to-date comes from the linkage, split by approval state

**Derive it through the link table, not from a memo search.** Sum the bills NetSuite has
actually applied to that PO — deduplicated to distinct bill ids per 5a — and keep approved
and pending apart:

```sql
SELECT d.po_id, d.approvalstatus, SUM(d.amt) AS billed, COUNT(*) AS bills
FROM (SELECT DISTINCT l.previousdoc AS po_id, b.id AS bill_id, b.approvalstatus,
             ABS(b.foreigntotal) AS amt
      FROM previoustransactionlinelink l
      JOIN transaction b ON b.id = l.nextdoc AND b.type = 'VendBill'
      WHERE l.previousdoc IN (<po_id values>) AND l.linktype = 'OrdBill') d
GROUP BY d.po_id, d.approvalstatus
```

**One written convention, because the file used to contradict itself on this.**
`approvalstatus = 2` is **billed to date**. `approvalstatus = 1` is **pending, stated
separately and naming this bill**. So "what this item takes it to" is arithmetic you show,
not an inference. Do not fold pending into billed-to-date, and do not report a
billed-to-date without saying which of the two it is.

Never derive a `poContext` figure from a vendor-plus-memo search again. The old route
summed on vendor and a memo `LIKE` with **no PO predicate at all**, so it swept in bills
applied to other POs entirely: it reported `PO11120` at `$478,012.50` against a `$372,500`
contract — *"130%"* — when the two bills actually applied to it total exactly its `$372,500`.
Contract from one key and billings from another, never joined, is how that happened.

### 5d. A zero is not a finding

**A billed-to-date of zero on the PO a bill is applied to is the expected reading** for the
first draw against a fresh commitment, and for any PO whose only bill is still pending — a
pending bill has not incremented anything yet. On its own it is **never** evidence of
miscoding, and it must never be offered as corroboration that a bill sits somewhere else.

Before treating a zero as meaningful at all, confirm the linkage query returned rows. A zero
that comes from a query that matched nothing is not a fact about the PO.

**Pull the billing history** for the same engagement — for duplicates, sequence gaps, and
proration precedent **only**. This query is no longer a source of any `poContext` figure:

```sql
SELECT t.id, t.tranid, t.trandate, t.foreigntotal, t.memo, t.approvalstatus, t.custbody3 AS po_typed
FROM transaction t LEFT JOIN vendor e ON e.id = t.entity
WHERE t.type = 'VendBill' AND e.entityid = '<vendor>'
  AND UPPER(t.memo) LIKE '%<person or engagement keyword>%'
ORDER BY t.trandate
```

The memo field is the reliable engagement key — staffing POs are often **pooled**, carrying many people at once, so a PO memo naming a different person is not a mismatch. Query by memo, not by PO alone.

Three further checks. **Provenance:** this list arrived in the repo's first commit
describing itself as checks that "have found real issues", with no run, record or date
attached, and Step 5 as a whole has never been observed end to end on real data — it runs
only in connector mode and no connector run has been walked through. Treat the three as
designed, not proven, and see `prose.md`.

- **Cumulative reasonableness.** Sum all bills for the engagement including the pending one and compare to what the contract period implies. A partial-month factor that looks inflated in isolation is often exactly right, or even under, once the whole engagement is footed.
- **Application sequence.** If a pay application says "less previous certificates $X," confirm bills totalling $X actually exist in NetSuite for that engagement. A missing intermediate application means the audit trail is broken and must be flagged before approval.
- **Duplicates.** Same vendor, same reference number, or same period billed twice. Also watch for two POs with identical memo and amount, which double-commits the spend.

## Step 6 — State file

Maintain `NetSuite Approval Checks/_netsuite_review_log.json`:

```json
{
  "config": {"me": 0, "meName": "...", "account": "...", "tool": "...", "billPortlet": "..."},
  "lastCompletedRun": "2026-08-11",
  "lastRunTime": "2026-08-11 11:04",
  "items": {
    "<transaction id>": {
      "docNo": "...", "type": "Bill|Change Order", "vendor": "...", "amount": 0,
      "trandate": "8/4/2026",
      "verdict": "clear|flagged",
      "reviewedOn": "YYYY-MM-DD", "lastSeenPending": "YYYY-MM-DD",
      "head": "one line, the verdict in plain terms",
      "facts": ["two or three skim lines with the specific figures"],
      "poContext": "PO15039 - contract $216,000 - billed to date $76,500 (approved) - this bill $12,000 pending - takes it to $88,500 of $216,000",
      "poWarning": "optional; a duplicate PO worth naming, or a typed reference that disagrees with the linkage",
      "poLink": "linked|unlinked|failed",
      "poTyped": "what custbody3 said, recorded whether or not it agrees",
      "detail": "the full paragraph of reasoning",
      "attachmentFile": "the attachment's NetSuite file name and id, e.g. 'ComEd Aug 2026.pdf (3741744)'",
      "poRef": "PO15039"
    }
  },
  "actions": [
    {"id": "...", "docNo": "...", "action": "approve|approve with notes|reject",
     "text": "the note actually submitted - the user's words, or 'Approved by Claude', or '' if the fallback dropped it", "at": "2026-08-11 14:22",
     "result": "confirmed left queue|failed: <why>"}
  ]
}
```

These field names are the contract with `publish_dashboard.py`. Do not rename them.

**`poRef` is the PO the bill is applied to** — resolved from the Step 2 linkage, never from
`poTyped`. The two are separate fields on purpose: keeping the typed value lets a reader see
the disagreement, and collapsing them back into one would re-create the bug. `poLink` says
which of the three states produced `poRef`, so an `unlinked` or `failed` item can never be
read as though its PO had been confirmed.

`head`, `facts`, `poContext` and `detail` are what the dashboard renders, so write them for a reader who is skimming. `facts` should be the two or three lines that carry the specific figures — a reader should be able to judge the item without expanding anything.

On each run:
- Items already logged as **clear** and unchanged (same amount): do not re-fetch or re-analyze the attachment. Carry the entry forward.
- Items previously **flagged**: re-check in full. The vendor may have replaced the attachment.
- Items whose amount changed since last review: treat as new.
- Brand-new items: full review.
- Items no longer in the queue: keep the entry for one run so the dashboard can show them in the actioned bin, then drop them.

## Step 7 — Publish to the dashboard

The deliverable is the inline dashboard widget.

**Do not write HTML.** The layout lives in `dashboard_template.html` and is the single source of truth for how the dashboard looks and behaves. Every run publishes by injecting data into it:

```bash
cd "<workspace>/NetSuite Approval Checks" && python3 publish_dashboard.py
```

**Render it as an inline widget with `show_widget`, passing the file's contents. Always attempt
this, whatever the file size.** A large queue makes a large file; that is normal and not a reason
to hesitate. Handing the user a file or an artifact *instead of* attempting the render is a failure
of this step, not a cautious alternative — it silently costs them one-click execute, which is the
entire point of rendering this way.

**Never publish it as an artifact.** The two hosts expose disjoint bridges, both probed live: the
widget host exposes `sendPrompt` as a bare global; the artifact host exposes `window.cowork`
(`callMcpTool`, `askClaude`, `runScheduledTask`) and no `sendPrompt` anywhere. On an artifact the
execute button cannot start a turn and fails silently — no error, no console output. As a widget it
works in one click, confirmed on a live run. The template keeps a clipboard handoff for the
artifact case; it is a fallback, not a plan.

**You cannot see whether the render worked, so ask.** `show_widget` returns `Content rendered and
shown to the user` regardless of what it rendered — it says that even when handed a file path and
shown a line of text. With no way to verify, declining can feel safer than a silent failure; it is
not, and the missing feedback is a person. After rendering, add one line:

> If a red banner appears at the top of the dashboard, tell me and I'll re-render a smaller version.

That turns an unverifiable gamble into a checkable claim for the cost of one sentence.

**Fall back only after an observed failure.** The template carries its own integrity guard: a
marker as its last element, checked from `<head>` as soon as the DOM parses, which raises a visible
red banner if anything was lost in transit. Trust it. If that banner actually appears, hand over
`index.html` directly and say why. A prediction that it *might* appear is not a reason to skip the
render.

**Pass the file verbatim.** Read it and hand it over byte for byte — never retype it, never
summarise it, never "clean it up" on the way through. The old artifact path passed the file by
path, so the HTML never travelled through a model response; a widget takes the content inline,
which puts the layout through the tool call. If a rendered dashboard is missing a card, a control
or a colour, suspect this before suspecting the template.

The script writes `index.html` beside the state file and keeps the last seven renders in
`renders/<weekday>.html`. Both matter when a render goes wrong: diff today against the last good
one to see what actually changed, and **re-render from `index.html` rather than re-running the
review** — the review costs connector queries and attachment extraction, the render costs nothing.
Do not write a cleanup step for `renders/`; the folder is usually cloud-synced, where deleting is
typically blocked, which is why the slots are overwritten in place rather than accumulated.

The script prints the headline line to use in chat.

Why it works this way: the dashboard is regenerated on every run, and a page rewritten from prose instructions drifts — a card lost, a colour changed, a behaviour forgotten. Injecting into a fixed template makes the chrome invariant by construction. If the script aborts because the sentinels are missing, **restore the template from `${CLAUDE_PLUGIN_ROOT}/skills/netsuite-approval-double-check/assets/` — do not rebuild it from memory.**

The script also aborts if the identity config is incomplete. Do not work around that by supplying a default; run Step 0.

The template already handles, on every open:
- showing how old the snapshot is, and warning visibly once it passes three hours
- dropping actioned items into the bin and flagging amount changes against the last review
- per-item decision marking with local-storage persistence and the batched execute bar
- a one-click re-run button, which is the refresh path now that the page never queries NetSuite itself

A design change goes in the **plugin repo** — the copy of `dashboard_template.html` under that
skill's `assets/` directory — not the workspace copy — Step 0 overwrites that copy on every run, so an edit made there lasts exactly one run and
reaches nobody else. Keep the sentinels intact, then push; teammates get it on their next plugin
update.

Then close scratch tabs and leave each record tab open so the user can act if they want to.

**Report in chat with one line only**, no per-item blocks:

```
6 pending · 1 flagged · dashboard updated
```

Add a second line only if something blocked the run — a login redirect, a missing attachment that prevented review, a portlet that has been renamed. Never put the verdicts in chat; that is what the dashboard is for.

## Step 8 — Execute decisions (only on explicit instruction)

The user marks decisions in the dashboard and presses execute, which copies an instruction naming each document and shows it for them to paste into chat. That pasted instruction, or an equivalent one typed directly, is the only thing that authorises a click.

Before clicking anything, check the instruction names specific documents. If it says "approve everything" or "approve the clear ones," stop and ask which.

Then, **one record at a time**:

1. **Re-verify it is still yours to action, before opening anything.** Run:

   ```sql
   SELECT t.id, t.tranid, t.foreigntotal FROM transaction t
   WHERE t.id = <id> AND t.approvalstatus = 1 AND t.custbody_sna_cdc_next_approver = <me>
   ```

   No row means it was approved, rejected or rerouted since the snapshot was taken. **Skip it**, log
   it as `skipped: already actioned elsewhere — no click made`, and move on. Do not open it, do not
   click, do not retry. If a row comes back but the amount differs from the instruction, **stop the
   batch** — the record changed underneath the review.

   This check is why the dashboard no longer queries the queue when it opens. A page-load check goes
   stale between opening the dashboard and pressing execute; this one runs against the record in the
   moment before it is clicked, so there is no window at all.

   **Never batch this check, however tempting it looks next to the fan-outs in Steps 1–3.** Hoisting
   it into one up-front sweep is cheaper and reintroduces exactly the staleness bug this step exists
   to close. It runs per item, immediately before that item's click, always.

   Change orders cannot be queried this way. For those, rely on the on-page confirmation in step 3.

2. Open the record by internal id at `https://<account>.app.netsuite.com/app/accounting/transactions/transaction.nl?id=<id>`.
3. **Confirm before clicking.** Read the document number, vendor and amount off the page and check all three against the instruction. Any mismatch → stop, do not click, report it.

   **If the record opens but the approval buttons are absent, suspect the browser's NetSuite role
   before anything else.** The connector signs in under its own account, and a browser left on that
   role sees the record without the buttons. Ask the user to check their role rather than reporting
   the item as unactionable — and never click anything while the role is in doubt.
4. **Choose the button.** Approve, Approve With Notes and Reject sit adjacent — read the label
   before clicking, never the position.

   - An **affirmative** instruction, whether it says "approve" or "approve with notes", goes
     through **Approve With Notes** — that is the only way the note in step 5 can be attached.
     Plain **Approve** is reached only via the fallback in step 6.
   - A **rejection** goes through **Reject**, exactly as named.
   - **Never substitute across the two.** An approve instruction must never reach Reject, and a
     reject instruction must never reach either approve button.
5. **Enter the note.** Approve With Notes loads a **normal page in the same tab** — it is not a
   popup and not a dialog. Read that page rather than assuming its layout, fill the note field,
   submit.

   - The user gave a note for this item → enter it **verbatim**.
   - They did not, and the response is affirmative → enter exactly `Approved by Claude`.
   - A rejection is missing its required reason → **stop and ask.** Never default a rejection
     reason; a rejection needs a reason a person wrote.

   Those two are the only strings this skill ever types into a note field. Compose nothing else —
   no summary of the review, no figures, no reasoning.

6. **If the notes page never arrives or the tab stops responding, the outcome is unknown — not
   failed.** Seen in practice: the tab froze straight after the click and dropped out of the
   automation group. Do not click anything in that tab, and **never re-click the button.**

   **The gate: read the page, never the connector.** Abandon the frozen tab, open the record fresh
   in a new tab, and read its approval state off the page.

   - **Still pending and still yours** → the click did not land. Click plain **Approve**, and log
     that the note did not make it.
   - **Advanced** → the click landed and only the note was lost. **Click nothing.** Log it as
     approved without a note.
   - **Cannot be read** → stop the batch.

   **Do not gate this on SuiteQL.** The connector lags the UI by minutes, so an unchanged reading
   means *not yet*, never *failed* — gating a fallback click on it would eventually approve a bill
   twice, which is exactly the damage the never-re-click rule below exists to prevent. A page load
   reads the UI and has no lag.

   **Plain Approve can itself do nothing, silently — and the mechanism is known, not a mystery.**
   Observed 2026-08-15, five identical clicks with zero effect: the button's handler loads a client
   script asynchronously and only then calls `win.open`, by which point the click's transient
   user-activation has expired, so Chrome drops the navigation — no error, no dialog, no network
   request, nothing in the console. The only thing that detects it is the same page-load read as
   above. So plain Approve gets **one** click, then a fresh page load:

   - **Advanced** → done. Log it as approved without a note.
   - **Still pending** → do not click again. **Navigate the approval request the button itself
     would have made.** Read the URL verbatim out of the button's own handler on the live record
     page — never compose it from memory or a template — and assert its parameters against the
     instruction before firing: `recid` is this record's internal id, `acttype` is the named
     affirmative response, and the approver id names the user. Then navigate to it **once**, in the
     same authenticated tab. This is the button's own server-side path and the button's own audit
     trail — the click minus the dropped `win.open` — not a REST shortcut; the
     never-`ns_updateRecord` rule is untouched. Confirmed live: record 2534442 approved this way
     after five dead clicks, routed and recorded normally.
   - Then step 7's verification, unchanged. Still pending after the URL navigation too → **stop
     the batch.**

   Two hard edges. This route exists **only for the affirmative path** — a rejection always goes
   through the Reject form, because it needs the reason a person wrote. And it can carry no note,
   so log it as `approved without a note via the button's own URL, after the button no-opped`.
7. **Verify it landed — against the record, not the queue.** Query that one record:

   ```sql
   SELECT id, approvalstatus,
          custbody_sna_cdc_next_approver     AS next_appr,
          custbody_sna_cdc_previous_approver AS prev_appr,
          custbody_sna_cdc_app_count         AS app_count
   FROM transaction WHERE id = <id>
   ```

   It advanced if `prev_appr` is now the user and `next_appr` is somebody else, with `app_count`
   incremented by one. On a final-step approval `approvalstatus` moves to 2 instead.

   **`approvalstatus` on its own proves nothing.** It stays at 1 while the record sits at the
   *next* person's step, which reads identically to never having moved. Observed live: two bills
   were approved, advanced to the next approver, and both still returned `approvalstatus = 1`.

8. **The connector lags the UI by minutes, so unchanged means "not yet", not "failed".** Wait and
   re-check rather than concluding. **Never re-click on an unchanged reading** — the UI has
   already taken the first click, so a second one is a double approval. This is the single most
   likely way for this skill to cause real damage.

9. **Append the outcome to `actions` only after observing it.** Record what the verification
   query actually returned, never what the click was meant to achieve. An entry written ahead of
   its verification is a fabrication, and afterwards it is indistinguishable from a real one —
   which destroys the value of the log at exactly the moment it matters.

**The post-click verification stays per item too.** It is tempting to click all N and reconcile once at the end, since the connector lag means an immediate re-query mostly reads "not yet" anyway. Do not. The check catches more than lag — a record in an unexpected state, a response that routed somewhere it should not have, the frozen-tab case in step 6 — and a single end-of-run sweep means every remaining click has already landed before any of that is visible. On a batch worth millions that is not a saving.

**A failure stops the batch.** If an item cannot be confirmed or does not match, stop there. A
record that has not propagated yet is **not** a failure — do not report it as one and do not
retry it. Report what was actioned, what is still propagating, what genuinely failed and why,
and what remains untouched. Never continue past a real failure or retry blind.

When the batch finishes, re-run Step 7 so actioned items move to the bin, and report in chat: how
many were actioned, how many were confirmed advanced, how many are still propagating, and
anything that failed.
