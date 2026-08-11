---
name: netsuite-approval-double-check
description: Financial double-check of the NetSuite bills and change orders sitting in your approval queue, published to a live dashboard artifact. Trigger whenever the user asks to "run my approval check," "check my NetSuite queue," "double check my bills," "review my change orders to approve," "run the daily approval review," or mentions their NetSuite approval dashboard or bills and change orders pending their approval. Also trigger when the user sends an execute instruction from the dashboard naming specific documents to approve, approve with notes, or reject. Downloads each attachment, verifies the math and the adequacy of support, cross-checks the real purchase order and billing history, and publishes a clear or flagged verdict per item. Only ever approves or rejects on an explicit per-document instruction, never on its own judgement.
---

# NetSuite Approval Double-Check

Review every bill and change order sitting in the user's NetSuite approval queue. Verify each item's math and the adequacy of its supporting document, cross-check against the real purchase order and billing history, and publish a per-item verdict to the dashboard.

Output goes to the `netsuite-approval-queue` artifact, not to chat. Chat gets one headline line.

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
- **Never copy identity between people.** The employee internal id in `config.me` scopes the whole review. Using someone else's shows them a queue that is not theirs.
- If deeper review would require actions beyond reading, say so in the verdict and ask first.

## Step 0 — First-run setup

Read `NetSuite Approval Checks/_review_log.json` in the connected workspace folder. If it exists and has a `config` block with `me`, `tool` and `account`, skip this step entirely.

Otherwise set up, once:

1. **Find the employee internal id.** Query by the user's own email address:

   ```sql
   SELECT id, entityid, email, isinactive, title FROM employee
   WHERE email = '<the user's email>' AND isinactive = 'F'
   ```

   **Employee records can share an email address** — a colleague with the same surname, or a former employee. Always report the name found and ask the user to confirm it is them before writing it. If the query returns zero or more than one active row, list the candidates with their titles and ask which is theirs. Never pick one silently.

2. **Record the connector tool name.** Use the fully-qualified name of the NetSuite SuiteQL tool you are actually calling in this session (it looks like `mcp__<server id>__ns_runCustomSuiteQL`). The server id differs per connection, so never copy it from documentation or another install — read it from the tool you just used.

3. **Find the account id** from the NetSuite URL the user's browser is on, or from the connector. It appears in record URLs as `https://<account>.app.netsuite.com/`.

4. **Ask which dashboard portlet holds their bills.** Portlet names are per-user saved searches and are frequently non-obvious. Have the user confirm the exact name rather than guessing.

5. **Copy the assets** into the state folder so the publish step can find them:

   ```bash
   mkdir -p "<workspace>/NetSuite Approval Checks"
   cp "${CLAUDE_PLUGIN_ROOT}/skills/netsuite-approval-double-check/assets/dashboard_template.html" "<workspace>/NetSuite Approval Checks/"
   cp "${CLAUDE_PLUGIN_ROOT}/skills/netsuite-approval-double-check/assets/publish_dashboard.py" "<workspace>/NetSuite Approval Checks/"
   ```

6. **Write the config** into `_review_log.json`:

   ```json
   {
     "config": {
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

7. **Create the artifact** on the first publish: call `create_artifact` with id `netsuite-approval-queue` instead of `update_artifact`.

## Step 1 — Build the queue

Pull the queue two ways and reconcile them.

**1a. Connector (fast, reliable, gets bills):**

```sql
SELECT t.id, t.type, t.tranid, t.trandate, t.foreigntotal,
       e.entityid AS vendor,
       t.custbody3 AS po_ref,
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

Two data quirks that will bite:
- **`foreigntotal` is negative on vendor bills** (e.g. `-12800`). Take the absolute value everywhere.
- **`trandate` comes back as `"7/19/2026"`**, not ISO. Parse month/day/year explicitly.

**1b. Dashboard (authoritative, and the only place change orders appear):**

Navigate to the NetSuite dashboard and scroll to the bottom. Three kinds of portlet matter: one holding change orders, one holding purchase orders (frequently empty), and one holding vendor bills — named in `config.billPortlet`.

Portlet names are user-specific saved searches and can be arbitrary, so do not assume a name is a placeholder. If a portlet has been renamed since setup, report it rather than guessing.

Use `get_page_text` on the dashboard tab rather than screenshots — the portlet tables extract cleanly as text. Then open each row's **date link** with a **ctrl+click** to put every record in its own tab. Ctrl+click may silently fail on the very first attempt; verify with `tabs_context_mcp` and retry once if no new tab appeared.

Review **every** item regardless of dollar amount. There is no threshold.

**Change orders are not queryable for pending status.** They live in `transaction` under a recordtype like `custompurchase_r_pci_change_order_po`, but the records carry `approvalstatus = null` and no next-approver value, so no SuiteQL filter can identify the ones awaiting the user. The dashboard portlet is the only source. This is why the dashboard labels change orders "as of last review" rather than live — do not remove that label.

## Step 2 — Read each record

`get_page_text` on each record tab returns the full field set. Capture:

- Reference no. / document no., vendor, date, **AMOUNT**, internal id
- MEMO, subsidiary, approval group, requestor
- The attachment filename (AP INVOICE or CHANGE ORDER ATTACHMENT field)
- Every **line** in the Items sublist: quantity, rate, amount, description
- For change orders: **CHANGE ORDER AMOUNT** and **PREVIOUSLY APPROVED AMOUNT**

The line-level quantity x rate is the first math check and it is free — do it before touching the PDF.

## Step 3 — Retrieve the attachment

**Do not click NetSuite's `download` link.** It fails silently under automation — no network request, no file, no error. Clicking `preview` opens a popup that freezes CDP screenshots on that tab. Both are dead ends.

Instead, get the file's authenticated URL from the connector and save it as a blob from inside the page:

```sql
SELECT id, name, filetype, filesize, url FROM file WHERE id IN (<ap_file ids>)
```

The `url` column returns a path like `/core/media/media.nl?id=<id>&c=<account>&h=<hash>&_xt=.pdf`. Then, in any authenticated NetSuite tab, define the helper once:

```javascript
window.__dl = async function(u, fn){
  const r = await fetch(u, {credentials:'include'});
  const bl = await r.blob();
  const a = document.createElement('a');
  a.href = URL.createObjectURL(bl); a.download = fn;
  document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 60000);
  return 'triggered ' + fn + ' ' + bl.size;
};
'ready'
```

Then call `await window.__dl('<path>', 'NS_<docno>_<vendor>.pdf')` per file, with ~1.5s between calls. Files land in the connected downloads folder within about 10 seconds. Verify with a directory listing before parsing; if the folder is cloud-synced, allow a little lag.

Notes:
- Use a `NS_` filename prefix so the run's artifacts are easy to spot and re-use.
- If a file with that name already exists from an earlier run, reuse it instead of re-downloading.
- **No attachment at all → flag the item.** Non-PDF attachments are unusual; handle them the same way and note the type.
- Multiple attachments → check the one referenced by the AP INVOICE / CHANGE ORDER ATTACHMENT field, and mention the others.

Extract text with `pdftotext -layout <file> -`. The layout flag preserves the column alignment that invoice tables depend on.

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
- **PO linkage:** bills routinely cite a PO on the invoice while the NetSuite record has no PO linked and WITHOUT PURCHASE ORDER unchecked. **Record the PO number for traceability, do not flag it.**
- **Skipped approvers:** ignore. Not a finding.

## Step 5 — Cross-check against the real PO and history

This is where the review earns its keep. Always do it.

**Pull the real PO** referenced on the invoice or in `custbody3`:

```sql
SELECT t.id, t.tranid, t.trandate, t.foreigntotal, e.entityid AS vendor, t.memo, t.status,
       t.custbody_r_it_original_contract_amount AS orig_contract,
       t.custbody_r_it_revised_contract_amount AS revised_contract,
       t.custbody_r_it_net_change_orders_amount AS net_cos
FROM transaction t LEFT JOIN vendor e ON e.id = t.entity
WHERE t.tranid IN ('PO____')
```

Then reconcile: a professional-services invoice's "billed previously" plus its remaining contract phases should tie to the PO's contract value. A change order's PREVIOUSLY APPROVED AMOUNT should tie to the PO total. Residual differences usually correspond to a specific already-approved change order — identify it rather than reporting a bare variance.

Caution: `custbody_r_it_total_amount_invoiced` and `..._remaining` are frequently stale (often 0). Do not rely on them; derive from actual bills instead.

Keep the PO figures — they become the `poContext` line on the dashboard row: contract value, billed to date, remaining, and what this item takes it to.

**Pull the billing history** for the same engagement to catch duplicates, sequence gaps, and to establish proration precedent:

```sql
SELECT t.id, t.tranid, t.trandate, t.foreigntotal, t.memo, t.approvalstatus, t.custbody3 AS po_ref
FROM transaction t LEFT JOIN vendor e ON e.id = t.entity
WHERE t.type = 'VendBill' AND e.entityid = '<vendor>'
  AND UPPER(t.memo) LIKE '%<person or engagement keyword>%'
ORDER BY t.trandate
```

The memo field is the reliable engagement key — staffing POs are often **pooled**, carrying many people at once, so a PO memo naming a different person is not a mismatch. Query by memo, not by PO alone.

Three checks that have found real issues:

- **Cumulative reasonableness.** Sum all bills for the engagement including the pending one and compare to what the contract period implies. A partial-month factor that looks inflated in isolation is often exactly right, or even under, once the whole engagement is footed.
- **Application sequence.** If a pay application says "less previous certificates $X," confirm bills totalling $X actually exist in NetSuite for that engagement. A missing intermediate application means the audit trail is broken and must be flagged before approval.
- **Duplicates.** Same vendor, same reference number, or same period billed twice. Also watch for two POs with identical memo and amount, which double-commits the spend.

## Step 6 — State file

Maintain `NetSuite Approval Checks/_review_log.json`:

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
      "poContext": "PO15039 - contract $216,000 - billed to date $76,500 - remaining $139,500",
      "poWarning": "optional, e.g. a duplicate PO worth naming",
      "detail": "the full paragraph of reasoning",
      "attachmentFile": "NS_....pdf",
      "poRef": "PO15039"
    }
  },
  "actions": [
    {"id": "...", "docNo": "...", "action": "approve|approve with notes|reject",
     "text": "note or reason as the user gave it", "at": "2026-08-11 14:22",
     "result": "confirmed left queue|failed: <why>"}
  ]
}
```

These field names are the contract with `publish_dashboard.py`. Do not rename them.

`head`, `facts`, `poContext` and `detail` are what the dashboard renders, so write them for a reader who is skimming. `facts` should be the two or three lines that carry the specific figures — a reader should be able to judge the item without expanding anything.

On each run:
- Items already logged as **clear** and unchanged (same amount): do not re-download or re-analyze. Carry the entry forward.
- Items previously **flagged**: re-check in full. The vendor may have replaced the attachment.
- Items whose amount changed since last review: treat as new.
- Brand-new items: full review.
- Items no longer in the queue: keep the entry for one run so the dashboard can show them in the actioned bin, then drop them.

## Step 7 — Publish to the dashboard

The deliverable is the `netsuite-approval-queue` artifact.

**Do not write HTML.** The layout lives in `dashboard_template.html` and is the single source of truth for how the dashboard looks and behaves. Every run publishes by injecting data into it:

```bash
cd "<workspace>/NetSuite Approval Checks" && python3 publish_dashboard.py <scratch>/index.html
```

Then call `update_artifact` with id `netsuite-approval-queue` and that file as `html_path`. The script prints the headline line to use in chat.

Why it works this way: the artifact is regenerated on every run, and a page rewritten from prose instructions drifts — a card lost, a colour changed, a behaviour forgotten. Injecting into a fixed template makes the chrome invariant by construction. If the script aborts because the sentinels are missing, **restore the template from `${CLAUDE_PLUGIN_ROOT}/skills/netsuite-approval-double-check/assets/` — do not rebuild it from memory.**

The script also aborts if the identity config is incomplete. Do not work around that by supplying a default; run Step 0.

The template already handles, on every open:
- re-querying the live pending queue via the configured connector tool and diffing against the published verdicts
- dropping actioned items into the bin, surfacing new items as unreviewed, flagging amount changes
- per-item decision marking with local-storage persistence and the batched execute bar
- refusing to query at all if identity is missing, rather than guessing an approver

Only change the template when the user asks for a design change. Then edit the file in place, keep the sentinels intact, and republish.

Then close scratch tabs and leave each record tab open so the user can act if they want to.

**Report in chat with one line only**, no per-item blocks:

```
6 pending · 1 flagged · dashboard updated
```

Add a second line only if something blocked the run — a login redirect, a missing attachment that prevented review, a portlet that has been renamed. Never put the verdicts in chat; that is what the dashboard is for.

## Step 8 — Execute decisions (only on explicit instruction)

The user marks decisions in the dashboard and presses execute, which sends an instruction naming each document. That instruction, or an equivalent one typed directly, is the only thing that authorises a click.

Before clicking anything, check the instruction names specific documents. If it says "approve everything" or "approve the clear ones," stop and ask which.

Then, **one record at a time**:

1. Open the record by internal id at `https://<account>.app.netsuite.com/app/accounting/transactions/transaction.nl?id=<id>`.
2. **Confirm before clicking.** Read the document number, vendor and amount off the page and check all three against the instruction. Any mismatch → stop, do not click, report it.
3. Click **only** the button named in the instruction. Approve, Approve With Notes, and Reject sit adjacent — read the button label before clicking, not the position.
4. Notes and reasons come from the user verbatim. Never compose either. If the instruction is missing a required reason for a rejection, stop and ask.
5. Verify it landed: re-query the pending queue and confirm the item no longer returns. Do not treat the button click as success on its own.
6. Append the outcome to `actions` in the state file.

**A failure stops the batch.** If any item cannot be confirmed, does not match, or does not leave the queue, stop there. Report what was actioned, what failed and why, and what remains untouched. Never continue past a failure or retry blind.

When the batch finishes, re-run Step 7 so actioned items move to the bin, and report in chat: how many were actioned, how many confirmed out of the queue, and anything that failed.
