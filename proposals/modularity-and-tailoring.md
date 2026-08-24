# Modularity and per-user tailoring

*Proposal, 2026-08-24. Nothing here is shipped. This document answers one
question: the catalog serves financial analysts well — how should it serve
everyone else? Build persona plugins (supply chain on Office 365 + Teams)?
Or build a skill that interviews the user, reads their connectors, and molds
itself to them? The answer proposed below is: neither, exactly — tailor the
**selection and configuration**, keep the **workflows** curated.*

---

## How far the repo already goes

More than it looks like, and in a specific shape worth naming before adding
anything.

**1. Modularity already exists, and it is capability-shaped, not
persona-shaped.** The prerequisite test in `CLAUDE.md` is a complete
modularity doctrine: a plugin is the unit a teammate can switch off, so
plugins split on *what you must have set up* (connectors, browser sessions,
credentials), never on topic or department — those are explicitly rejected
split reasons. The one persona-shaped rule it carries is audience (rule 4: a
different subset of the team should be able to have it), and that rule is
what a supply-chain plugin would ride in on.

**2. Per-user tailoring already exists, and it is identity-shaped.** Both
skills interview the user on first run and store the answers in a `config`
block: NetSuite confirms the employee id *by name* (never silently), the
account, the portlet names; Procore takes the company and tool ids. Both
abort publishing rather than guess a missing identity. That is real
tailoring — the same skill produces a different review for each person — but
it molds the workflow to *who you are*, not to *what your job is*.

**3. Capability adaptation already exists, for exactly one connector.** The
NetSuite skill re-detects the MCP connector on every run and degrades to the
browser route with one sentence said once — someone provisioned later is
lifted automatically, someone whose session lapses keeps working. That is
"see the user's connectors and adapt", in miniature, proven in production.
It is the pattern to generalize, not a new idea.

**4. What does not exist:** anything that discovers a user's role or
connector inventory globally, recommends from the catalog, or configures a
plugin the user hasn't already installed. Distribution is announce + install
by hand, and `CLAUDE.md` already documents the cost of that (it is what the
future bundle plugin exists to remove).

## How the catalog serves a supply-chain person today

Honestly: the plumbing serves them; the judgment doesn't.

Both systems of record scope their own queues. Procore's items endpoint and
permission gate are scoped to the signed-in session; NetSuite's queue is
scoped to `next_approver`. So a supply-chain teammate who installed either
plugin today would see **their own queue** — the machinery is
persona-agnostic wherever the system of record's own scoping does the work.

But the checks encode a financial analyst's review: G702/G703 tie-outs,
contract math, the PO/billing-history cross-check, quantity × rate. A
supply-chain reviewer's questions — receipt vs. PO quantities, delivery
dates against need dates, lead-time slippage, expediting threads — appear
nowhere, and their communication surface (Outlook, Teams) isn't touched by
either plugin. They'd get a financially-reviewed version of their queue:
correct, scoped to them, and answering questions that are not theirs.

## Option A — build the supply-chain plugin now

The prerequisite test already pre-decides the mechanics:

- A skill needing the **M365/Teams connector** → new plugin, named for its
  prerequisite (`m365-tools`, not `supply-chain-review`), new marketplace
  entry.
- A supply-chain skill that is **NetSuite-only** (receipt status, PO aging)
  has *identical* prerequisites to the existing NetSuite plugin and would,
  by rules 1–3, join that bucket — unless audience (rule 4) says only
  supply chain should be able to have it, in which case new plugin. That
  call is the maintainer's, per skill, and should be recorded when made.

What the test cannot pre-decide is **what the skill should do**, and here
the repo's own epistemics rule: *proven, not guessed*. Every durable thing
in this catalog came from watching a real workflow fail in a specific way
— the CCO id trap, the connector lag, the no-op Approve button. A
supply-chain plugin designed by a financial analyst and an agent imagining
supply-chain work would be the opposite: a stack of plausible guesses
shipped with live-system authority. **Do not build Option A from
imagination.** Build it from one interview with one supply-chain teammate
and one watched run of how they actually work a day.

## Option B — the "mold yourself" meta-skill

The ambitious version: a skill that enumerates the user's connectors,
interviews their role and scope, and *generates* a bespoke review skill in
their image.

The enumeration and interview halves are genuinely solvable today. A
running session can see which connector tools resolve (the NetSuite skill
already proves the probe-and-adapt pattern), and the first-run-setup
pattern is an interview — it just stops at identity.

The generation half is the wrong bet for this repo, for reasons that are
structural rather than technical:

- **Generated skills start at zero on everything these notes paid for.**
  Three-state error handling, never-collapse-empty-and-failed,
  verify-the-record-not-the-queue, the output-filter redactions — a
  bespoke skill re-earns each lesson in production, on systems where the
  failure mode is a silent wrong approval.
- **Generation forks the distribution model.** Push-to-`main`-is-the-release
  works because everyone runs the same artifact. A per-user generated skill
  has no shared version, receives no fixes, and is invisible to
  `scripts/validate.py` and `test_skill_code.py`. The 2026-08-20 PO
  cross-check fix reached every installed copy in one push; it would have
  reached zero generated ones.
- **It inverts the house safety convention.** "Neither plugin acts on its
  own judgement" is load-bearing. A skill that designed itself is judgment
  all the way down, with no reviewable text for a maintainer to have vetted.

## Recommendation — tailor the selection, curate the workflow

Layered, in order of when to build:

**Layer 1 (exists, keep):** curated workflow plugins, prerequisite-bucketed.
This is where correctness lives, and nothing below touches it.

**Layer 2 (build next): a concierge skill.** One new plugin with **zero
prerequisites** — installable by anyone on day one — holding one skill that
does the interview Option B wants, and stops before generation:

1. **Discover** — probe which connectors actually resolve in this session
   (the NetSuite skill's re-detect pattern, generalized), and ask about the
   browser sessions it cannot probe (Procore, NetSuite sign-in).
2. **Interview** — role, systems touched daily, what they review or approve,
   what they chase by email/Teams. Short, concrete, stored.
3. **Map** — recommend from the catalog: which plugins fit, which
   prerequisite each needs, in the onboarding sheet's install terms. Walk
   the first-run setup of anything installed.
4. **Report the gap** — when the interview finds work the catalog doesn't
   cover, write a structured gap report (role, systems, prerequisites, the
   workflow in the user's own words, one watched example) for the
   maintainer. Interview → curate, not interview → generate. The gap
   report is the requirements document a new curated skill starts from.

This lands the user's tailoring instinct where it is safe and cheap: the
*selection and configuration* mold to the person; the *workflow text* stays
reviewed, versioned, and fixed-for-everyone-in-one-push. It also converts
every new-persona conversation from an imagined design into a recorded
requirement.

**Layer 3 (build from the first gap report): the supply-chain plugin(s).**
Recruit one supply-chain teammate, run the concierge interview on them, and
let their actual day decide the shape — likely an M365-prerequisite plugin
(Teams/email-driven expediting and delivery reconciliation) and possibly a
NetSuite-bucket skill, per the prerequisite test. Reuse the proven bones:
first-run identity setup, three-state reads, dashboard + explicit per-item
instruction, idempotency log with a **skill-unique** state filename.

**Layer 4 (already documented, unchanged):** persona bundles once the
catalog passes ~4 plugins — a finance bundle, a supply-chain bundle — after
the validator carve-out for dependency-only manifests that `CLAUDE.md`
already flags as required-first.

## What this deliberately does not do

- **No persona forks of existing skills.** A "supply-chain variant" of the
  Procore skill would be a second copy to drift. If a second persona ever
  needs different *checks* over the same queue, that is a config-selectable
  review lens inside the one skill — and it should not be built until a
  real second persona asks, with a watched run.
- **No self-modifying or self-generating skills**, for the three structural
  reasons above.
- **No speculative M365 plugin before an interview.** The connector's tools
  (mail, calendar, SharePoint, Teams chat search) make several workflows
  *plausible*; plausible is exactly the standard this repo rejects.

## Open questions for the maintainer

1. Does a supply-chain teammate exist who will sit for the interview and
   let one run be watched? The whole of Layer 3 gates on this.
2. Should the concierge's gap reports land as GitHub issues on this repo
   (public — so no company ids, no real document contents) or in a private
   channel? The repo's no-sensitive-content rule suggests the latter, with
   only the sanitized requirement committed here.
3. Audience call to pre-record: if a NetSuite-only supply-chain skill
   arrives, does rule 4 (audience) split it out of the NetSuite bucket, or
   does everyone get it? Deciding now avoids deciding under deadline.
