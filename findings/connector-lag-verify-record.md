---
id: F10
slug: connector-lag-verify-record
kind: finding
status: observed
date: 2026-08-12
---
# Verify the record not queue

**Outcome protected.** A successful approval is never logged as a failure and never clicked twice.

**Argument.**

The NetSuite connector lags the user interface by minutes after an approval. The obvious success check reads that lag as failure.

The execute step used to verify by re-querying the pending queue and checking that the item no longer returned.

Two things break that. The approval status stays at the pending value after a successful approval. That happens because the record is now pending the next approver.

And the connector takes minutes to catch up, so even a correct query returns stale rows straight after the click.

Together they produce a false failure on work that succeeded. That stops the batch, logs a failure that did not happen, and invites a re-run that would approve twice.

So verify the record. Select the approval status, the next approver, the previous approver and the approval count for that record id.

Advanced means the previous approver is now the user, and the next approver is someone else. It also means the count went up by one.

Unchanged means not yet, never failed. Report `still propagating` once and end the round. Never re-click on it, and never write a waiter loop around it.

**Evidence.**

- Found in production 2026-08-12. Two bills were approved and routed onward, and both still read the pending approval status.
- The lag is described in minutes. No timing was recorded, so the exact interval is `unmeasured`.
- This is why the freeze recovery is gated on a page load. See F27, the notes click is a navigation.

**Checks.** none
