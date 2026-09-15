---
id: pending
slug: persona-plugins
kind: decision
status: abandoned
date: 2026-08-24
---
# Persona plugins and concierge

**Rule.** Never fork a skill per persona.

**Outcome protected.** One artifact serves every reviewer, so one push fixes everyone's copy.

**Argument.** The question was how the catalog should serve someone who is not a financial analyst.
One answer was a plugin per persona, plus a concierge plugin to route people to them.

**Reason abandoned.** The work went into modularity inside the two existing plugins instead.
See D‹check-packs-next-phase›, packs written from role research.
Nothing about the prerequisite test changed.
A genuinely new prerequisite such as M365 or Teams is still a new plugin.
Name that plugin for the prerequisite rather than for its first task.
If a second persona needs different checks over the same queue, that is a config-selectable lens.
It is not a second copy to drift.

**What is actually true about a non-finance user today.** The plumbing serves them and the judgment
does not.
Both queues are scoped by the system of record itself.
Procore's endpoint and permission gate by the signed-in session.
NetSuite's queue is scoped by `next_approver`.
So a supply-chain teammate installing either plugin today would see their own queue.
But every check encodes a financial analyst's questions.
Those are the G702 identities, contract math and the PO cross-check.
Receipt against purchase order quantities appears nowhere.
Delivery dates against need dates and lead-time slippage appear nowhere.
Such a teammate would get a correctly scoped queue reviewed against questions that are not theirs.

**Two questions gate any future attempt.** First, whether a supply-chain teammate will sit for an
interview and let one run be watched.
Nothing here should be designed from imagination, by this repo's own standard.
Second, whether a NetSuite-only supply-chain skill would be split out of the NetSuite bucket by the
audience rule, or given to everyone.
See D‹prerequisite-bucket›, a plugin is a prerequisite bucket.

**Evidence.** Declined 2026-08-24.
The pre-decision write-up in `proposals/` was deleted rather than marked superseded.
Most of it restated the repo's own rules back at itself, which is a drift source.
The rest argued for a path that was declined.
No teammate has yet sat for the supply-chain interview. `unmeasured`.

**Checks.** none.
