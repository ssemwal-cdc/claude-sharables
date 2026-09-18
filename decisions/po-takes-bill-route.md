---
id: D76
slug: po-takes-bill-route
kind: decision
status: superseded
date: 2026-09-01
---
# Purchase orders take bill route

**Superseded by** D91, review-only plugins, on 2026-09-18. Execute mode was retired. The rule returns with it, and the text lives on in `actionable-retired/`.

**Rule.** Action a purchase order by the bill route. Log a lost note when Approve With Notes is absent.

**Outcome protected.** A reviewed purchase order can be approved in the same run.

**Argument.**

Purchase orders take the bill route on the strength of the fields, not the resemblance.

A pending purchase order carries the approval status. It also carries the three approver custom fields that the pre-click gate and the post-click verification read. So the route transfers unchanged.

The button set is a separate question and is still unread. Nobody has looked at the approval buttons of a purchase order.

So the step reads the labels, as it always did. It now also says what happens when Approve With Notes is not among them.

The affirmative button is still clicked, and the note is logged as lost. It is never written somewhere else.

That is the existing frozen-tab fallback rule reused, not a new invention.

**Evidence.**

- The fields were confirmed live 2026-09-01 on a pending purchase order.
- The button set is `unmeasured`. See G16, the purchase order route is unfired.

**Checks.** `check_execute_type_coverage()` in `scripts/shared_blocks.py`.
