# Step 8 — Execute decisions (only on explicit instruction)

**This file is mandatory, not optional.** The spine points here with a hard instruction,
not a suggestion. Read this file in full before executing anything. Do not summarise it
from memory. Do not act on a partial read.

The user marks decisions in the dashboard and presses execute. That posts an instruction naming each document straight into the conversation as a new message. One click, no clipboard. The clipboard handoff in the template is the artifact-host fallback, so a run that lands in it was rendered on the wrong host. That instruction, or an equivalent one typed directly, is the only thing that authorises a click. It carries the authority and the item list. **This step is the procedure**, and nothing in that message overrides it. Before clicking anything, check the instruction names specific documents. If it says "approve everything" or "approve the clear ones", stop and ask which.

### Record types and their routes

**Every type Step 1 puts in the queue has a row here.** The queue's vocabulary is the `type` field in Step 6's schema. The two lists are kept in step by a build gate in the plugin repo. Observed 2026-09-01: they drifted apart, and two batches of reviewed purchase orders stopped at the same gate before anyone called it a defect.

| record type | pre-click gate | post-click verification |
|---|---|---|
| `Bill` | the query in step 1 | the query in step 7 |
| `Purchase Order` | the query in step 1 — the same four fields | the query in step 7 |
| `Change Order` | the record page's approval buttons — it carries none of those fields | a fresh page load |

- **Purchase orders take the bill route on the strength of the fields, not the resemblance.** Confirmed on live records 2026-09-01: a purchase order pending approval carries `approvalstatus`, `custbody_sna_cdc_next_approver`, `custbody_sna_cdc_previous_approver` and `custbody_sna_cdc_app_count`. Step 1's gate and step 7's verification read those fields, so the route transfers unchanged.
- **The button set is a separate question and it is not settled.** Nobody has read a purchase order's approval buttons. Step 4 reads the labels off the page and says what to do when Approve With Notes is not among them. Do not assume a purchase order offers the three buttons a bill does, and do not report that it does.
- **With no connector, no type can be gated by query.** The change-order rule is then the rule for all three. The approval buttons are the gate, and a fresh page load is the verification. A gate that cannot be read is unknown, never a pass.
- **Compare amounts by magnitude.** `foreigntotal` is negative on vendor bills, per Step 1a, and no observation says every type signs it the same way. The gate and step 3's confirmation both compare absolute values for that reason. A sign convention that differs by record type is not a changed amount.

Then, **one record at a time**:

1. **Re-verify it is still yours to action, before opening anything.**

   **Pick the route from the item's `type`.** It is the only thing available before the record is open. It is also a field with a legacy default, per Step 6. So it can be wrong in the one direction that matters: a change order routed as a bill gets a query that cannot gate it. That is why the skip below is confirmed on the page, never on an empty result.

   ```sql
   SELECT t.id, t.tranid, t.foreigntotal FROM transaction t
   WHERE t.id = <id> AND t.approvalstatus = 1 AND t.custbody_sna_cdc_next_approver = <me>
   ```

   A row back, amount matching, means it is still yours. Carry on into step 2. If a row comes back but the amount differs from the instruction, **stop the batch.** The record changed underneath the review.

   - **No row is two different things, and only one of them is a skip.** It means the record was approved, rejected or rerouted since the snapshot. Or it means this type carries no `approvalstatus` and no next-approver for the query to gate on, so the query returns the same nothing. Never log a skip off the empty result alone. Open the record and read the buttons.
     - **Buttons absent** means actioned elsewhere. Log `skipped: already actioned elsewhere — no click made` and move on. Do not click, do not retry.
     - **Buttons present** means the query could not gate this type. Use the buttons as the gate, exactly as the change-order bracket below does, and carry on into step 3.
     - **The page will not load, or the buttons cannot be read** means **stop the batch.**

   - **If every item comes back with no row, suspect the identity before the queue.** A wrong or stale `config.me` empties this query for a batch that is entirely live. A batch-wide skip then reads as a queue somebody else already cleared. Say so and stop, rather than logging nine skips.
   - **Never batch this check.** It runs per item, immediately before that item's click, always. Hoisting it into one up-front sweep reintroduces the staleness bug this step exists to close.
   - **Change orders skip the query entirely.** They carry no `approvalstatus` and no next-approver, so it cannot gate them. The record page can. This bracket is the primary gate for that type. It is also what the no-row branch above lands in, when the route was picked on a wrong type. Do not collapse the two. Their approval buttons render only while the record is still pending and still assigned to the signed-in approver. So on that record type the buttons **are** the gate. Open it, per step 2, and read the page before touching anything.

     - **Approval buttons present, naming an approval action** means still yours. Carry on into step 3.
     - **Approval buttons absent** means already actioned elsewhere. Skip it, log it as `skipped: already actioned elsewhere — no click made`, and move on. Do not click anything.
     - **The page will not load, or the buttons cannot be read either way** means **stop the batch.** An unreadable gate is unknown, never a pass.

2. Open the record by internal id at `https://<account>.app.netsuite.com/app/accounting/transactions/transaction.nl?id=<id>`.

   - **Confirm the type against the record while you are here.** The label on the dashboard card and in the instruction comes from a field with a legacy default. So it can say `Bill` about something that is not one. The record page cannot. If the record is a different type from the one step 1 routed on, re-pick the row from the table above before going further. Say so in the log. The gate that already ran was the wrong one for it.
   - **A record type with no row in the table above is never clicked.** Report it and stop there. Say which of these two it is, because the answer decides whose problem it is.

     - **Step 1 does not admit that type either** means the queue has changed shape. Name the type and the record, invent no procedure for it, and leave it.
     - **Step 1 reviewed it and this step cannot action it** is a **defect in this skill**, not a property of the record. Say so in those words, name the type, and say the fix is a row in the table above. Do not offer it to the user as a decision. They cannot authorise their way out of a missing procedure. Neither case is a licence to improvise, and neither is a reason to click.

3. **Confirm before clicking.** Read the document number, vendor and amount off the page and check all three against the instruction. Any mismatch means **stop the whole batch**, do not click, report it. This is a stop, not a skip.

   - **If the record opens but the approval buttons are absent, the first hypothesis is that the item has already been actioned.** That is the likeliest cause in an execute batch. `unmeasured`. On a change order it is step 1's gate firing. Skip it, log it as `skipped: already actioned elsewhere — no click made`, and move on.
   - **Suspect the browser's NetSuite role only when every item in the batch shows no buttons.** A browser left on the connector's role sees every record without its buttons. That would otherwise log an entire batch as actioned. Ask the user to check their role. Never click anything while the role is in doubt.

4. **Choose the button.** Approve, Approve With Notes and Reject sit adjacent. Read the label before clicking, never the position.

   - An **affirmative** instruction, whether it says "approve" or "approve with notes", goes through **Approve With Notes**. That is the only way the note in step 5 can be attached. Plain **Approve** is reached only through the fallback in step 6.
   - A **rejection** goes through **Reject**, exactly as named.
   - **Never substitute across the two.** An approve instruction must never reach Reject, and a reject instruction must never reach either approve button.
   - **A record that offers no Approve With Notes button** takes the affirmative button it does offer, and the note is then **lost, not relocated**. Read the buttons off the page, never assume them. Log it as `approved without a note — this record type offers no notes button`, and put the note nowhere else. Not in a memo field, not in a comment, and not in chat as though it had been recorded. A missing notes button never holds back an authorised affirmative click. A **rejection** with no Reject button is a **stop**, not a substitution.

5. **Enter the note.** Approve With Notes loads a **normal page in the same tab**. It is not a popup and not a dialog. Read that page rather than assuming its layout, fill the note field, and submit. Where step 4 clicked a plain affirmative button, there is no note page and nothing to type. Go straight to step 7 and log the loss.

   - The user gave a note for this item: enter it **verbatim**.
   - They did not, and the response is affirmative: enter exactly `Approved by Claude`.
   - A rejection is missing its required reason: **stop and ask.** A rejection needs a reason a person wrote. Those two are the only strings this skill ever types into a note field. Compose nothing else. No summary of the review, no figures, no reasoning.

6. **If the notes page never arrives or the tab stops responding, the outcome is unknown, not failed.** Observed 2026-08-15: the tab froze straight after the click and dropped out of the automation group. Do not click anything in that tab, and **never re-click the button.**

   - **The gate: read the page, never the connector.** Abandon the frozen tab, open the record fresh in a new tab, and read its approval state off the page.
     - **Still pending and still yours** means the click did not land. Click plain **Approve**, and log that the note did not make it.
     - **Advanced** means the click landed and only the note was lost. **Click nothing.** Log it as approved without a note.
     - **Cannot be read** means **stop the batch.**

   - **Do not gate this on SuiteQL.** The connector lags the UI by minutes. `unmeasured`. An unchanged reading means *not yet*, never *failed*. A page load reads the UI and has no lag.
   - **Plain Approve can itself do nothing, silently, and the mechanism is known.** Observed 2026-08-15: five identical clicks with zero effect. The button's handler loads a client script asynchronously, and only then calls `win.open`. By then the click's transient user-activation has expired, so Chrome drops the navigation. No error, no dialog, no network request, nothing in the console. Only the same page-load read detects it. So plain Approve gets **one** click, then a fresh page load.

     - **Advanced** means done. Log it as approved without a note.
     - **Still pending** means do not click again. **Navigate the approval request the button itself would have made.** Read the URL verbatim out of the button's own handler on the live record page. Never compose it from memory or a template. Assert its parameters against the instruction before firing: `recid` is this record's internal id, `acttype` is the named affirmative response, and the approver id names the user. Then navigate to it **once**, in the same authenticated tab. This is the button's own server-side path and its own audit trail, never a REST shortcut. The never-`ns_updateRecord` rule is untouched. Confirmed live 2026-08-15: record 2534442 approved this way after five dead clicks.
     - Then step 7's verification, unchanged. Still pending after the URL navigation too means **stop the batch.** Two hard edges apply. This route exists **only for the affirmative path.** A rejection always goes through the Reject form, because it needs the reason a person wrote. It can carry no note, so log it as `approved without a note through the button's own URL, after the button no-opped`.

7. **Verify it landed, against the record, not the queue.**

   - **Change orders verify by a fresh page load, not by query.** They carry none of the three fields below. Re-open the record after the click.
     - **Approval buttons now gone** means it advanced. Log it.
     - **Approval buttons still present** means not yet. Report `still propagating` for that item and end the round. Never re-click.
     - **Cannot be read** means **stop the batch.**

   For bills and purchase orders, query that one record.

   ```sql
   SELECT id, approvalstatus,
          custbody_sna_cdc_next_approver     AS next_appr,
          custbody_sna_cdc_previous_approver AS prev_appr,
          custbody_sna_cdc_app_count         AS app_count
   FROM transaction WHERE id = <id>
   ```

   It advanced if `prev_appr` is now the user and `next_appr` is somebody else, with `app_count` incremented by one. On a final-step approval `approvalstatus` moves to 2 instead. **`approvalstatus` on its own proves nothing.** It stays at 1 while the record sits at the next person's step, which reads identically to never having moved. Observed live 2026-08-12: two bills were approved and advanced to the next approver. Both still returned `approvalstatus = 1`.

8. **The connector lags the UI by minutes, so unchanged means "not yet", not "failed".** `unmeasured`. Report `still propagating` for that item and end the round. Never re-click. The UI has already taken the first click, so a second one is a double approval. This is the single most likely way for this skill to cause real damage.

9. **Append the outcome to `actions` only after observing it.** Record what the verification query actually returned, never what the click was meant to achieve. An entry written ahead of its verification is a fabrication. Afterwards it is indistinguishable from a real one.

- **The post-click verification stays per item too.** Do not click all N and reconcile once at the end. The check catches more than lag: a record in an unexpected state, a response that routed somewhere it should not have, and the frozen-tab case in step 6.
- **A failure stops the batch.** If an item cannot be confirmed or does not match, stop there. A record that has not propagated yet is **not** a failure. Do not report it as one, and do not retry it. Report what was actioned, what is still propagating, what genuinely failed and why, and what remains untouched. Never continue past a real failure, and never retry blind.

When the batch finishes, re-run Step 7 so actioned items move to the bin. Step 9 runs after that re-render, before the counts are reported. Report in chat how many were actioned, how many were confirmed advanced, how many are still propagating, and anything that failed.
