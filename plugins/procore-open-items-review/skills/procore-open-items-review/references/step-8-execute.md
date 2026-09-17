# Step 8 — Execute responses, only on explicit instruction

**This file is mandatory, not optional.** The spine points here with a hard instruction,
not a suggestion. Read this file in full before executing anything. Do not summarise it
from memory. Do not act on a partial read.

The user marks responses on the dashboard and presses execute. That copies an instruction naming each item and shows it for them to paste into chat. That pasted instruction, or an equivalent typed directly, is the only thing that authorises a click. **The dashboard is a snapshot.** The user may have actioned an item in Procore directly since the last run. So for **each** item, in this order:

1. **Verify it is still theirs to action, before touching any UI.** Re-query the Step 2 endpoint. Skip the item if it returns no instance, or `can_respond` is false, or the named response is not in `available_responses`. Log it as "already actioned elsewhere — no click made" and continue. Do not open it, do not click, do not retry. **Never batch this check.** Its whole value is running in the moment before that item's click.
2. **Only if `can_respond` is still true, open the record in a record tab.** Confirm the item number, campus and building, and amount against the instruction. **Any mismatch stops the whole batch.** That record tab stays open through the post-click verification in item 4 and closes in Step 9.
3. **Open the workflow side panel, click Respond, select only the named response, fill the comment box, submit.**
   - A comment the user gave for this item is **pasted verbatim.**
   - No comment and an affirmative response gets exactly `Approved by Claude`.
   - A rejection missing its required reason **stops the run. Ask.** Never default a rejection reason.
   - Those are the only two strings this skill types into a comment box. Compose nothing else.
4. **Confirm through the API, not the click.** Re-query and confirm `can_respond` is now false, or that the step advanced.
   - **A first re-query still reading `can_respond` true is `unconfirmed`, not failed.**
   - Log it, do not retry, do not stop the batch, name it in the counts.
5. **If a submit fails or the step does not advance, stop the batch there.** Never retry the same item.
6. Append each outcome to `actions`.

When the batch finishes, re-run Step 7 so the dashboard is current. Step 9 runs after that re-render, before the counts are reported. Report the counts in chat: actioned, skipped as already done, `unconfirmed`, departed from the queue, and whatever stopped the batch.
