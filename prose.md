# Prose

Notes that are not rules. `CLAUDE.md` holds the things a session must follow;
this file holds findings, retrospectives, and the standing list of what has and
has not actually been observed.

---

## What has not been verified yet

The repo's convention is *proven, not guessed*. Everything below is currently
**guessed** — reasonable, tested against mocks or fixtures, and shipped. None of
it has been watched working on real data. A future session should not cite any of
it as established.

`python3 scripts/test_skill_code.py` covers the logic against mocks. It cannot
cover any of this, because all of it is about the real systems.

**The nine numbered gaps are below, after the open-decisions section.** They belong to this
heading, not to that one — a section inserted between the two on 2026-08-24 left them reading
as deferred work under a heading that opens *"none of this is a commitment"*, which is the
opposite of what they are.

---

## Open decisions, and what was deliberately deferred

Written 2026-08-24 at the end of the modularity work, because the reasoning behind these
lived in one conversation and would otherwise be lost. **None of this is a commitment.**
It is a record of what was considered, decided against *for now*, and why — so the next
session neither re-derives it nor treats it as a mandate.

### Decisions waiting on a person

1. **Extending shared-block coverage.** Cheap and mechanical for anything byte-identical. The
   named blockers are not laziness: most remaining `SKILL.md` duplication is *near*-identical,
   differing only by the plugin's own name and workspace folder, and closing that would mean
   designing those names out of the prose. Same for blocks differing by one token
   (`ns_marks_v1` vs `pc_marks_v1`, the two log filenames).

### Work considered and deferred, in the order it was judged worth doing

- **Capability-gated, config-selectable check packs.** The answer to *"how does this serve
  someone who is not a financial analyst"* without any new plugin: each check declares the
  capability it needs and the lens it belongs to; `config.lenses` selects; **absent config
  means exactly today's behaviour**, which is what makes it additive. A check whose capability
  is missing does not run and **is named as not run** — generalising the connector re-detect
  the NetSuite skill already does well. A skipped check may never produce a `clear` verdict
  (the existing OCR-cap rule reused). Precondition, and it is the whole risk: the judgment
  layer is currently pure static prose with zero parameters, so *extracting* checks is
  behaviour-neutral while *parameterising* them is not — separate phases. And the second pack
  must not be written from imagination; see "Directions considered and not taken".

  **Phase 1 of this shipped 2026-08-26 (NS v12, PC v13).** Each verify step now opens with a
  check registry declaring every check's id, lens and capability, gated by
  `check_check_registry()`. It is **descriptive only** — `core` is the whole table, so
  behaviour is unchanged — and it was added **purely additively**, with no existing check prose
  moved or reworded. What remains deferred is Phase 2 (`config.lenses` actually selecting) and
  Phase 3 (a second pack's content).

  **One correction to the framing above, and it is the reason the rest got cheaper.** *"The
  judgment layer is pure static prose with zero parameters"* is true, but it was being read as
  though the **data** were the constraint too. It is not. Probed live 2026-08-26 rather than
  inferred:

  - **`itemreceipt` exists — 565 fields, 225 standard** — carrying `createdFrom`, `orderId`,
    `orderType`, `tranDate`, `item`, and `class`/`department`/`location`/`subsidiary`. So a
    **three-way match is constructible today.** Step 2 already queries
    `previoustransactionlinelink` and discards the `ShipRcpt` rows with
    `linktype = 'OrdBill'` — correct for summing dollars, and one filter away from receipts.
    This had been filed as "genuine new work". It is not.
  - **`purchaseorder` carries `dueDate`, `shipDate`, `orderStatus`** among 616 fields, so
    lead-time slippage is constructible too (PO `dueDate` against receipt `tranDate`).
    **Caveat, and it is the honest standing: schema existence is not population.** Whether
    those fields are actually filled in at Compass is a *data* probe nobody has run. Do not
    cite this as a working check.
  - **The SuiteQL metadata catalog 500s on `transactionline`** for this tenant —
    `Field match custcol_r_it_total_retainage_balance not found on record type
    <Transaction>:<TransactionLine>`. Schema discovery for that table must go through
    `ns_getRecordTypeMetadata` or a probe query. It will cost someone an afternoon otherwise.

  **And the interview precondition was over-read.** *"The second pack must not be written from
  imagination"* bars inventing personas and check content; it does **not** mean waiting for a
  scheduled interview before building the mechanism. **Step 0 already interviews** — which
  portlet, which employee id, confirm your role. Asking a corporate-accounting user which
  accounts should never appear on a construction bill is that same mechanism, and it supplies
  the policy source whose absence had been treated as a wall.

  **The distinction that actually governs the risk here** — and which was being applied one
  level too conservatively — is **review depth versus execute authority.** Deepening what is
  read and reported does not touch the per-item instruction, the pre-click re-verify or the
  post-click page-load verify. The reader is a domain expert; *surfacing* coding to someone who
  knows the coding policy is the product, and the inability to *validate* it is much less of a
  blocker than it was being treated as. The real constraint is narrower and checkable: **do not
  break for anybody** — absent config is byte-identical, an errored query is `failed` and never
  `empty`, a permission-denied field degrades to "not checked" without aborting, and nothing new
  widens the execute path.

  **Phase 2's blocker is resolved — decided by interview with the maintainer, 2026-08-26.**
  The conflict was that Phase 2 wanted a check whose capability is missing to be *named as not
  run*, while Step 5 emphatically bans exactly that for the connector — no caveat in the
  verdict, the warning line, the detail paragraph, the dashboard **or the chat headline**,
  because it would print "on every item of every run, forever" for someone who "cannot get a
  connector and can do nothing about it".

  The resolution, in four parts:

  1. **Silence stays the default.** With no lens chosen, nothing is ever said about a check that
     did not run. Step 5's rule is untouched and existing users see no change at all. This is
     the part that keeps Phase 2 additive.
  2. **A lens the user deliberately picked, whose checks cannot run, gets one line at the start
     of the chat reply** — naming the lens and what is missing. Once per run. Never on
     individual items, never in a verdict, warning line or detail paragraph. So the repetition
     clause of Step 5's objection is answered by *frequency*, not by an exception to it.
  3. **The verdict is untouched.** Reporting only — a lens changes review depth, not the gate,
     so the `VERDICTS` allowlist and Procore's `affirmSkipped` caution path are unaffected. The
     OCR-style cap (a not-run check forcing a non-`clear` verdict) was considered and declined:
     it would change behaviour for browser-mode users who legitimately get `clear` today.
  4. **Never present the missing capability's functionality as though it happened.** The
     maintainer's words on the edge case — someone picking a lens needing a connector they can
     never have — were that it "should plainly say they don't have it and don't hallucinate that
     functionality."

  **Why this is consistent rather than an exception.** Step 0 already carves out the
  expired-connector case: one line, once, near the headline. The chat reply's opening line is
  therefore the surface this repo *already* uses for run-level capability status, and the new
  rule reuses it rather than opening a new one. The distinction that governs both: **a
  capability the user chose is informative; one they were never given is an apology.**

  **One consequence, recorded rather than buried:** the earlier Phase 2 sketch had a "which
  packs ran" panel on the dashboard. The decision puts the message in **chat**, so that panel is
  **dropped**. Do not reinstate it as a tidy-up — the dashboard is where the queue is read, and
  a permanent status panel there is closer to the per-item caveat Step 5 rejects than to the
  once-per-run line that replaced it.

  **Phase 2 and the first pack shipped 2026-08-26 (NS v13, PC v14).** `config.focus` carries two
  layers, decided by interview:

  - **`focus.lenses`** — hardcoded packs, because a pack is real checks with real queries and
    invented ones would be judgment nobody vetted. Today: `supply-chain` on NetSuite. Procore
    carries the key and ships no lens.
  - **`focus.emphasis`** — free text, works **with or without a pack**. The maintainer's
    requirement was that someone whose function has no pack "should still be able to have some
    individualized characteristics allowed for them, probably a lot less without the pack, but
    still." So emphasis reorders and rewords `head`/`facts`/`detail` and never touches a verdict,
    a figure, or any Absolute rule. Without a lens it is all the tailoring there is; that is the
    point, not a shortfall.

  Both default to empty, and empty is exactly today's behaviour. Proven rather than asserted:
  publishing the same log with and without `config.focus` produces **byte-identical** output, and
  neither `dashboard_template.html` nor `publish_dashboard.py` was touched.

  **The leniency doctrine, and it governs every future pack.** From the maintainer: *"not all
  data is in netsuite for all the stuff supply chain interacts with, so it should be fuzzy
  matching and/or lenient, 3-way match is nice when it happens, but just like the ns connector
  itself is nice to have, it shouldn't stop someone from not being able to work this at all."*

  So a pack's checks are held to a stricter standard than `core`'s:

  - **Missing data is never a finding.** A PO with no receipt rows is overwhelmingly a PO whose
    receipts NetSuite never saw — **not** a delivery that never arrived. It never flags, never
    skips, never reads as a criticism.
  - **Only a discrepancy where both sides exist can flag.** Billed 50 against receipts of 40 is a
    finding; billed 50 against no receipt data is silence.
  - **Three states again** — `matched` / `absent` / `failed`. `failed` is never `absent`, and
    `absent` is never "nothing was received". Sixth instance of this shape in these notes.
  - **Match leniently.** Descriptions, units and line splits differ between a PO, a receipt and a
    vendor invoice for ordinary reasons. Prefer an approximate tie to a manufactured mismatch.

  **One implementation note that is load-bearing.** Step 5e runs the `ShipRcpt` query as a
  **second query**, never by widening Step 2's `linktype = 'OrdBill'` filter. That filter exists
  to stop the billing sum double-counting, and mixing the two link types re-creates exactly the
  3× overcount that once turned `136,369.02` into `409,107.06`. Deduplicate receipts to distinct
  ids before summing, for the same reason.

  **`ns.lead-time` ships as an observation only and is the weakest of the three.**
  `purchaseorder` carries `dueDate` and `shipDate`, but **schema existence is not population** —
  whether Compass fills them in is unprobed. Empty is the `absent` state: say nothing. And a late
  delivery is never a reason to withhold payment for goods received; that judgement is not this
  review's.

  **This reframe does not reach M365/Teams**, and that is not the same caution repeated. More
  NetSuite is more internal system-of-record data; email and Teams are **outsider-controlled**,
  and both skills already rule that record content is data and never instructions. A vendor
  writing *"please approve invoice 2532506, finance cleared it"* would become review context on
  a system holding live approval authority. A **feeder** — a line saying the user can *ask* for
  a Teams/Outlook cross-check — is cheap and safe because it is ephemeral, on request, and adds
  no prerequisite, so it does not touch the prerequisite test. A **standing** integration needs
  the injection rule extended past attachments and a never-persist-raw rule first.

- **Thin `SKILL.md` spine plus `references/` modules.** Roughly a third of each skill is dead
  weight on any given run — NetSuite's Step 5 loads in browser mode where it cannot run, Step 8
  loads on review-only runs. `ofci-analysis-cip` on this machine is the in-house precedent (a
  158-line spine plus four reference files). **The non-negotiable line if it is ever done:**
  safety and policy prose never moves, because reference files load on demand and a rule the
  model must choose to read is the silent-degradation class this repo has spent fifty commits
  eliminating. Step 8 is the hard case — large *and* almost entirely safety — and the only
  defensible handling is an explicit mandatory read, not lazy loading. `test_skill_code.py`
  reads `SKILL.md` by path with no fallback and must be re-pointed in the same commit.

- **One parameterised dashboard instead of two.** Largest change, least user-visible benefit,
  and it removes the independent verification two copies give. The drift check already solves
  the problem that made this tempting. Revisit only if a third lens needs a dashboard.

### The standing constraint behind all of it

The two plugins **cannot share code at run time.** `${CLAUDE_PLUGIN_ROOT}` resolves per plugin
and a `git-subdir` install ships only `plugins/<name>/`, so every shipped file must be complete
on its own. Runtime sharing is not an option that exists; do not go looking for it.

---

### 0. Step 5's PO cross-check was wrong, and is now fixed but unobserved

**Corrected from guessed to proven, 2026-08-20** — the one item on this list that moved by
being falsified rather than confirmed. Step 5 identified a bill's PO from `custbody3`, a
typed reference, and produced confident false *"coded to the wrong PO"* flags on correctly
coded bills. Confirmed against production on five of five bills; details and record ids in
`CLAUDE.md`. A teammate found it by noticing Related Records disagreed with System
Information.

Two things about its provenance are worth recording, because they are why it survived 50
commits. Step 5 arrived in the **root commit** and its logic was never revised — `git log -S`
on `poContext`, `poWarning`, `custbody3` each return only that commit, and **no commit
message ever explained the design**. And its own text described its three checks as ones that
*"have found real issues"*, with no run, record or date attached — unlike every other verified
thing here, which names one. That unsourced claim is now marked as designed in `SKILL.md`.

**What is fixed:** PO identity from `previoustransactionlinelink` with
`linktype = 'OrdBill'`; three states kept distinct; billed-to-date derived through the link
and split from pending; a zero no longer readable as a finding; a typed mismatch demoted to a
data-entry note. Guarded by `scripts/test_skill_code.py`, mutation-tested (10/10 caught).

**What is still unobserved:** the corrected Step 5 has never run inside an actual review. The
queries themselves are live-verified — every one in this fix was executed against production
— but the *skill following them end to end* has not been watched, and Step 5 runs only in
connector mode, so it inherits gap 1 below.

**To clear it:** run one connector-mode review over a queue containing at least one bill whose
typed reference disagrees with its linkage. Required outcome: not flagged for PO coding, and a
`poWarning` naming the disagreement. Bills `2325026-07` and `182743734-0004` are the known
cases.

### 1. No end-to-end run, either plugin

The single biggest gap. Every change from 2026-08-13/14 — in-page pdf.js
extraction, the fan-out gate, the bulk `transactionline` query, the size-budgeted
page reads, the attribution note — is verified only against mocks and one live
chat test of pdf.js on bill 2532506.

**To clear it:** run a full review on each plugin, then execute against **one
low-value item**. Compare the verdicts against a previous run's — same figures,
same clear/flagged calls. A difference is a regression until explained.

*Partially observed, 2026-08-15 (Procore):* a live run gated two previously-
`ungated` Align change orders as actionable at Financial Analyst Review with
Approve / Revise and Resubmit, through the `CommitmentChangeOrder` join — the
first real-data confirmation of the CCO recipe, and of the step-not-subject verb
pairing. The ids came from `wfId`s already recorded in the log, so the
`line_items[].holder.id` read is still unobserved, and execute mode still has
not been walked.

*Partially observed, 2026-08-15 (NetSuite):* one approval completed live —
record 2534442, executed by navigating the Approve button's own URL after the
button no-opped five times (Step 8.6). It routed and recorded normally, which
confirms the URL recovery but not the ordinary path: **Approve With Notes
remains unwalked** (item 2), so no approval has yet gone through the primary
route with a note attached. The same run also surfaced the Step 0 mount gap (see the sync
ladder), so its dashboard was rendered from workspace copies synced a day
earlier — the gate results stand regardless, since the gate runs from `SKILL.md`,
which ships with the plugin.

### 2. The NetSuite notes page

`Approve With Notes` loads a page **nobody has seen**. The one attempt froze the
tab. The skill deliberately says to read that page rather than assume its field
names or button labels, because inventing them would be worse than vague.

**To clear it:** approve one low-value bill and watch where the note lands.
Then tighten **Step 8.6** with the real labels. (This said "Step 5" under the old
numbering, where that was the notes page; Step 5 is now the PO cross-check.)

### 3. The freeze fallback

The recovery path — abandon the tab, re-read from a fresh page load, fall back to
plain `Approve` only if still pending — has never fired. It cannot easily be
forced.

**To clear it:** you probably can't on purpose. Just know it is untested, and if
a freeze happens, watch what the run does rather than assuming it handled it.

*Update, 2026-08-15:* the fallback's terminal action — plain `Approve` — has
since shown a silent no-op mode of its own (its handler async-loads a script,
then calls `win.open` after the click's activation expired), so the ladder now
ends in navigating the button's own URL (Step 8.6) rather than in a click. The
URL leg is live-confirmed on record 2534442; the freeze fallback as a whole has
still never fired.

### 4. The Procore scheduled prompt

Derived from the NetSuite one and checked against the skill (state filename,
report format, the GET-only rule). Never actually fired.

**To clear it:** trigger the scheduled task manually once and confirm the
idempotency gate reports "already completed today" on a second fire.

### 5. The Procore gate fan-out against real Procore

The three-state rule is mock-tested and mutation-tested. It has never issued 70+
concurrent requests at the live API.

**To clear it:** on the first real run, check the reported counts add up —
actionable + suppressed + failed should equal the queue length. Any `failed`
items should be **named**, never folded into the suppressed count.

### 6. The attachment sniff — CLEARED for workbooks and images

**Reported working on real support, 2026-08-20**, by the person running the
plugins. Real vendor workbooks are read and real images are looked at; both paths
have now been exercised outside the mocks. This item moves out of the unverified
list, and the claims in the two plugin READMEs about reading spreadsheets sheet by
sheet and looking at images rather than extracting them are therefore accurate
rather than aspirational.

**Provenance, stated exactly.** This is a user report, not something a session
observed and wrote down from a transcript — which is a weaker standard than the
CCO gate (record ids, dates) though a stronger one than a mock. Nobody has posted
the figures a workbook produced, so *that workbook's numbers reached the tie-out
correctly* is assumed rather than shown.

**Two narrower branches are still unfired**, and must not be read as covered by
the above:

- **`scanned` → rasterise → look.** A PDF that parses but yields almost nothing,
  then gets rendered and looked at. Distinct from an image attachment, which
  Chrome displays directly.
- **The OCR fallback**, and with it the rule that an OCR-derived figure never
  produces a `clear` verdict. Never exercised, so the cap has never been tested.

**The specific regression to watch for:** a skip whose reason is vague. The bug
this replaced said "support present but unreadable", which reads the same whether
the file was a scan, a workbook, or a link that timed out — which is exactly how
whole formats went unread for weeks with nothing in the log to show it. If a skip
cannot name which of the six outcomes caused it, that is the same bug returning.

### 7. NetSuite browser mode

Added 2026-08-15. The skill now runs without the MCP connector: queue from the
dashboard portlets, record fields via `get_page_text`, the attachment URL read off
the record page, and Step 5's PO/billing-history cross-check simply not performed.
None of it has been run.

**One consequence of that surfaced on 2026-08-24: browser mode could not publish at
all.** `publish_dashboard.py` hard-aborted when `config.me` or `config.tool` was
missing — and Step 0 omits both in browser mode *by design*, because the portlets are
per-user saved searches already scoped to whoever is signed in. So a browser-mode run
completed the whole review and then died at Step 7, telling the user to run a
first-time setup they had done correctly. Reproduced from a fixture, then fixed:
`account` is required on both routes, `me` and `tool` only in connector mode. The
identity guard is unchanged for connector runs — a connector-mode config still aborts
without `me`.

Worth keeping for the method rather than the bug: this is the second defect found by
*reading the two plugins against each other* rather than by running either. It had
survived since browser mode shipped because nothing had exercised the path, which is
exactly what this gap says. A gap on this list is not inert — it is where the next bug
is.

The queue and record-page halves are reverts to methods that worked before the
bulk queries replaced them, so they are the low-risk part. **The unobserved piece
is the attachment URL DOM read** — whether the AP INVOICE / CHANGE ORDER
ATTACHMENT field actually renders as an `a[href*="media.nl"]` on every record type,
or as something else on some of them.

**To clear it:** open one bill and one change order with the connector switched off
and confirm the selector returns the four parameters, then that the fetch and
pdf.js path is byte-identical to the connector route from there on.

**The thing to check is a silence, not an error.** Step 5 is skipped with nothing
said about it, deliberately — a caveat would print on every item of every run for
someone who cannot get provisioned. So confirm the verdicts read as complete
statements of what *was* checked rather than as connector-mode verdicts with a hole
in them.

### 8. Small unknowns

- Whether the desktop app's plugin list shows a commit-hash version. The
  onboarding sheet says "both plugins appear in your installed list" because
  that is definitely visible; the hash check is only documented for the CLI.
- Whether Cowork sessions need the per-conversation connector toggle
  (**+ → Connectors**). Anthropic's docs say connectors are per-conversation;
  the step was removed from the sheet as not matching observed behaviour.
- Whether the file tools can read `${CLAUDE_PLUGIN_ROOT}` from a Cowork
  sandbox — rung 2 of Step 0's sync ladder. Observed so far: the *shell*
  cannot see it there (2026-08-15). Read is expected to, since assets resolve
  at run time and the skill panel lists them, but nobody has walked that rung.
  If it fails too, rung 3 keeps runs alive and Cowork workspaces only ever
  refresh from a surface whose shell mounts the plugin directory.
- Whether **Approve With Notes** shares plain Approve's handler shape (async
  script load, then `win.open`). If it does, its failure presents as the
  already-documented "notes page never arrives" case, and the same page-read
  gate catches it — but nobody has read that button's handler to check, and
  there is no note-carrying equivalent of the URL recovery.

### 9. The dashboard UI change — measured in a browser, unseen in the widget host

The 2026-08-20 change (newest-first default, sticky execute bar, numbered steps,
header mirror) is unusual for this list in that most of it **was** observed, just
not where it will actually run. Both dashboards were published from fixtures and
driven in headless Chromium: the default sort, the view-key migration for a
returning user, the ordering itself, the `ageDays` clamp fix, the both-null
comparator guard, light and dark, and the sticky bar's viewport position measured
at two scroll offsets. Those were established **on 2026-08-20 fixtures that were never
committed**, so a future session cannot re-run them and cannot audit them either — it can only
take this paragraph's word for it. Treat them as reported rather than reproducible, and if any
of it matters again, re-measure. The pattern across this whole corpus is worth the reminder:
every number a command regenerates has verified correct on demand; almost every number a human
typed into prose has since moved.

**What is not established is the one thing that cannot be checked from here:
whether `position:sticky` does anything in the widget host.** The measurement was
taken at `file://`, where the document itself scrolls. The dashboard renders inside
an iframe on `*.claudemcpcontent.com`, and whether that iframe scrolls internally
or auto-sizes while the *conversation* scrolls is not knowable from the agent side
— the same wall the note in `CLAUDE.md` describes about `show_widget` returning
"Content rendered" whatever it rendered. If it auto-sizes, there is no scroll
container, and sticky degrades silently to an ordinary block. No error, no
console output; it simply sits in flow.

That is why the header mirror exists and why it must not be deleted as redundant:
it is the half that works on either host. `docs/onboarding.html` is worded to be
true either way — it says a button sits at the bottom and a second appears in the
header, and deliberately does **not** promise the bottom one follows you down the
page. An earlier draft did promise that and it was removed unshipped, because it
would have been a claim about a host nobody has observed.

**One question settles it, and it needs a person at the keyboard:** on the next
real run, scroll the queue inside the conversation and say whether the dark
Execute bar stays pinned near the bottom edge or scrolls away with the rows. If it
scrolls away, sticky is inert on that host — which is not a bug to fix so much as a
fact to record here, and the header mirror is then carrying the feature alone.

**Also unseen at real scale.** The fixtures were 6 NetSuite bills and 8 Procore
items. A real Procore queue has run to 43–73. A sticky bar overlays the rows
beneath it, and 153px of overlay against a six-row fixture is not the same
experience as against seventy — nobody has watched that. The step headings and the
restyled marked rows are likewise cosmetic-only and unseen by anyone but the
person who wrote them.

---

## The two dashboards had drifted, and it cost six defects

2026-08-24. An audit of the two plugins' assets against each other, prompted by a
question about making them more modular. The finding worth keeping is not any single
bug but the shape: **every one of these is a case where one copy learned something and
the other never did.**

Measured duplication at the time of the audit: `dashboard_template.html` 528 vs 603
lines with **308 identical** (54.5% Dice); `publish_dashboard.py` 148 vs 238 with
**106 identical**. The CSS blocks alone were 92.5% identical. Across the two
`SKILL.md` files, ~250–300 of 1,495 lines were duplicated or near-duplicated, and
**10 of the 22 commits that ever touched a `SKILL.md` touched both in the same
commit** — every one of those ten a mechanics or convention change, not one a change
to a financial check.

Fixed in that commit, NetSuite side unless noted:

| | Defect | Consequence |
|---|---|---|
| 1 | Browser mode could not publish (see gap 7) | A complete review died at Step 7. Same root cause as the unused-config-keys item below — one over-broad `required` list — which is why this is six defects and not seven |
| 2 | No verdict allowlist | A typo'd verdict fell through the pill logic to **"Clear"** — fail-open on the field that decides what gets approved. Procore has aborted on this since it shipped |
| 3 | `var live=null` never assigned | ~45 lines unreachable: the gone/changed states, `newRow`, the bin, and a permanently-`0` "Unreviewed" card |
| 4 | Marks never pruned | A mark for a since-approved bill stayed in `ns_marks_v1` forever and would reappear if NetSuite reused the id. Procore sweeps them |
| 5 | Money card had no rollover | A $2.7m queue rendered `$2702k` |
| 6 | Abort message named `_review_log.json` | The pre-migration name — both copies, so the rename fix reached neither string |
| 6b | Aborted on two unused config keys | The other face of defect 1: `me` and `tool` were injected and read by the page and then never used; only `account` is |

**The drift check that came out of it.** `plugins/_shared/` holds the canonical copy of each
shared block, fenced in both plugins by name-matched markers, with `scripts/shared_blocks.py`
enforcing that every shipped copy matches — run by `validate.py`, so drift is a failed build.

What is **established** about it, by construction and by test: adding the markers changed no
content at all (the whole diff was 36 marker lines, zero deletions, verified by grepping every
changed line); the check catches a one-sided edit, a reworded comment, a missing canonical file
and an orphaned one, each naming the file and the differing line; editing one canonical file and
running `--sync` reaches both plugins; and both dashboards still render in headless Chromium, in
both themes, with markers embedded in their JS and Python — Procore's `index.html` and
`widget.html` both.

What is **not** established: nobody has yet had to use it in anger, i.e. fix a real shared bug
by editing the canonical file mid-review.

**Coverage was 13 blocks across 26 sites on 2026-08-24** — 9 in the assets (90 lines) and 4 in
the two `SKILL.md` files (34 lines) — plus a cdnjs version-pin check that needs no registration.
Mutation-tested at every step, including a one-sided pdf.js bump and a reworded Step 0 paragraph.
**Do not trust that figure once it is old**; `python3 scripts/shared_blocks.py --check` prints the
live count, which is the only number that cannot be stale.

**And the honest limit, which is the finding worth keeping from that pass.** The `SKILL.md`
duplication is mostly *near*-identical rather than identical: the same paragraph with the
plugin's own name and workspace folder substituted. Only **72 of ~1,500 lines** sit in
contiguous byte-identical runs, and only ~34 of those have clean paragraph boundaries — a
Markdown comment mid-paragraph splits it, and one inside a fence corrupts code the test
harness evaluates. So the block mechanism can never cover most of that surface as written.
The gap is not laziness; closing it would mean designing the per-plugin names out of the
prose, which is a bigger and separate decision. The blocks that differ by one token
(`ns_marks_v1` vs `pc_marks_v1`, the two log filenames) are the same story in miniature.

**`widget.html` — resolved 2026-08-24, and the measurement decided it.** Procore rendered
the slim copy as its primary dashboard on the grounds it was "roughly a fifth smaller".
Measured across five fixture queue mixes, it is **0% to 12%** smaller — 0% with nothing
skipped or ungated, 2–6% on a realistic mix, and 113 KB → 101 KB at the large end, which
crosses no observed threshold. Only `skipped` and `ungated` rows fold, and a live queue is
mostly neither, so the saving was always going to be small.

The cost is not small. Folded rows drop `resp`, `head`, `facts` and `detail`, so on the slim
render a `skipped` item — one whose support never arrived — **cannot be sent back**, which is
the response it most often needs. My earlier note here guessed the cost was nil because
folded rows "have no response buttons to lose"; that is true of `ungated` and false of
`skipped`, and the publish script's own `no_resp` warning covers `skipped` precisely because
those items normally do carry verbs.

So Procore now renders `index.html`, matching NetSuite, and the slim copy is reached only
when the integrity banner fires — which is what `CLAUDE.md` had said all along. The note was
right and the shipped behaviour was wrong.

**NetSuite is not getting a matching slim build, and the reason is structural.** Its verdicts
are exactly `("clear", "flagged")`, which is the slim build's *actionable* set, and the fold
branch is the `else` — so nothing would ever fold and the output would be a byte-for-byte
duplicate of `index.html` on every run. NetSuite has no `skipped` concept by design: a
missing attachment flags an item rather than skipping it. It could not be a shared block
either, since the folded keep-list is per-domain. Asked for on grounds of symmetry and
declined on grounds of vacuousness — worth recording, because "make the two match" is
usually the right instinct in this repo and here it is not.

**What made this findable, and it is the repo's own device:** two independent sources
saying different things. Neither copy could detect its own miss, exactly as the CCO
gate and the PO cross-check could not. The difference here is that the second source
was *the other plugin*, sitting in the same repo the whole time.

---

## The staleness check could not detect staleness

2026-08-24, found by a question rather than a failure: *"shouldn't we just write the dashboard
copies every time instead of caching them?"*

**The copy cannot be removed, and that part of the design is right.** `publish_dashboard.py`
resolves its log, its template and its output from `__file__`, and the Cowork sandbox does not
mount the plugin directory into the shell — so code that must run in that shell has to live
inside the workspace. The every-run overwrite the question was reaching for already exists:
Step 0 says *"Do this on every run"* and *"This overwrites the workspace copies deliberately."*

**But the question landed on a real hole.** `check_template_version()` compares the workspace
*template's* marker to the workspace *script's* constant — and Step 0 copies those two files
**together**. So they disagree only when a sync tears halfway. A workspace that is uniformly
three versions old has both files agreeing with each other and publishes in silence. Reproduced:
template `v4` + script `v4` against a plugin shipping `v6` produced no warning at all.

So the marker caught a torn sync, never a stale one — which is the failure it was added for, and
`CLAUDE.md` claimed outright that *"a stale copy names itself"*. It does not. That line is now
corrected rather than left as a claim nobody had tested.

**The fix has to live somewhere that always ships.** Any check comparing two workspace files is
blind here, because staleness moves them in lockstep. `SKILL.md` is the only fixed point: it
ships with the plugin, so it is current by construction even on the surface where the plugin
directory cannot be reached at all. Step 0 now states the expected `layout template vN` and reads
the workspace copy back, reporting a mismatch once and carrying on — the same fail-open posture as
rung 3, because a stale layout still renders correct verdicts.

That makes a **third** site for the template version per plugin, so `validate.py` now fails if
`SKILL.md`, the template marker and the script constant disagree. Adding a synced site without
adding its enforcement is the exact mistake this session spent two commits cleaning up.

**The general shape, which has now appeared often enough to name:** *a check whose two inputs
fail together cannot detect that failure.* Same family as the connector-lag rule (verify the
record, not the queue, because the queue lags with it) and the CCO wrong-id case (a 200-empty
looks like no-instance). Any freshness check needs one input that cannot go stale.

---

## The actioned bin never worked in either plugin

2026-08-24, found by a documentation sweep rather than a run — which is the point worth
keeping, since neither plugin would ever have reported it.

Both skills' carry-forward rules said: *"no longer in the queue → keep the entry for one
run so the dashboard can show it in the actioned bin, then drop it."* Neither bin could
render.

**NetSuite's was collateral from the same day.** Its bin was fed by the `gone` state of
the dead `live` machinery, removed earlier that day as unreachable — and the instruction
that fed it was not updated with it. Self-inflicted drift, caught within hours only
because the sweep went looking.

**Procore's has never worked, and the guard that blocks it is one I added.** Its template
still filters `bin` on `verdict === "gone"`, but `gone` is not in Step 6's vocabulary and
the publish script's `VERDICTS` allowlist would abort on it. So the bin has never rendered
in any run, and could not without a fourth verdict nobody defined.

The harm was mild and real either way: a departed item lingered as an apparently-pending
row for one extra run, inflating the queue count. Execute would have skipped it — it
re-verifies before every click — so this could never have caused a wrong click, only a
wrong number. Both rules now say drop it.

**Both bins are now gone.** Procore's markup, CSS and filter were removed once it was
mechanically confirmed that no run could reach them — it had never rendered in any run and
finishing it would have meant inventing a fifth verdict nobody had asked for.

**And this part of it turned out to be automatable after all**, which the first version of
this note said was "not obvious that it can be". `check_verdict_vocabulary()` in
`shared_blocks.py` asserts that every verdict a template branches on is one its own publish
script can emit. It reproduces the Procore bin exactly, and it is mutation-tested — the
first attempt at that test passed silently because the injecting `sed` had not applied, so
the check looked verified when nothing had been checked. Re-run properly, it fires with the
file, the verdict and the allowlist named. **A check that passes because the mutation never
landed is worse than no check**, because it also certifies itself.

**What is still not automated, and is the honest residue:** removing dead code leaves live
*prose* pointing at it, and nothing catches that. `validate.py` checks that docs mention
every *plugin*, never that they describe behaviour the code still has. The NetSuite
instruction that survived its own bin's deletion by a few hours was found by reading the
docs against the code deliberately. The verdict check covers one narrow, machine-settleable
slice of that; the rest is still a person reading.

---

## The nine-agent prose audit, and what the interview corrected

2026-08-24. Five auditors read the whole prose corpus cold — deliberately given none of the
session's conclusions and told not to read git history — then three debaters contested the pooled
findings from defence, prosecution and adjudicating positions. 122 raw findings, 29 surviving
contest. What follows is only what changed something.

**The headline was a place nobody had looked: the composed execute message.** It is the text
closest to a real approve click, and it is the least-governed text in either plugin — a JavaScript
string inside an HTML template, covered by no shared block, read by no test. Both copies had
independently drifted into carrying procedure, and both had got it wrong in the same week.
NetSuite's said *"click the named button only, then re-query the pending queue to confirm the item
left it"* — the button rule that Approve With Notes exists to override, and the retired
verification that `CLAUDE.md` records as inviting a re-run that would approve twice. Procore's
carried its whole five-step ladder but omitted `per_page=100`, which its own Step 2 records as
converting a live workflow into an empty response that Step 8 then reads as *already actioned,
skip it*. `grep per_page plugins/` returned three hits, all in `SKILL.md`, none in the template.

**Also a gap in that morning's own fix.** The verdict allowlist added to close a fail-open caught a
*wrong* verdict but not a *missing* one: `it.get("verdict", "clear")` defaulted an absent key to
`clear` and sailed straight through the check. Procore's sibling defaults to `skipped`. Fixed by
removing the default entirely and letting the allowlist abort.

**And the staleness check added the previous turn was itself stale.** Procore's Step 0 stated it
ships `v5` and then tested *"if that does not say `v4`"* — so the check written specifically to
detect a stale workspace would have called a current one stale and passed a genuinely stale one.
`check_template_versions()` missed it because `re.search` stops at the first match and there were
two sites. It compares every site now. **Third instance of the same shape**: a check whose inputs
fail together, and a checker that only looked at one of them.

**Four things the interview corrected, and this is why the interview existed.** Auditors reason
from the documents; the documents are not the system. (1) The panel asked whether NetSuite change
orders should be executable at all — the maintainer replied *"I thought we resolved change
orders?"*, conflating Procore's CCO gate, which was resolved, with NetSuite's change orders, which
carry no approval status or next-approver and so cannot be gated or confirmed. Different systems,
same word; the docs now distinguish them. (2) Browser-mode execute: the maintainer reports it works
through Claude in Chrome, which is a user report rather than an observed run, and answers a
narrower question than the panel asked — *the clicks land* is not *the gate ran*. (3) On the public
repo, the maintainer believed it was enterprise-private. The GitHub API says `"private": false`,
`"visibility": "public"`, forkable, personal account. The judgment about sensitivity is theirs; the
premise was checkable and wrong. (4) The precedence question resolved on two facts no auditor could
have known: execute is always pressed in the session that ran the review, and the run is not
watched.

**The generalisable lesson.** Every number a command regenerates was verified correct today. Almost
every string a human retyped had drifted. The corpus's defects cluster almost perfectly on
hand-maintained text that no command reads — which is an argument for extending mechanical checks
into prose wherever a claim names an identifier, and for treating any un-checked string near a
click as suspect by default.

---

## Working the audit list

2026-08-24, immediately after the nine-agent audit. 38 items needed no decision; this is what
happened to them and what is left.

**Two answers came from the maintainer mid-pass and changed the work.** NetSuite change orders
*should* be executable, so they now have a real bracket instead of a documented gap: their records
carry no `approvalstatus` and no next-approver, but their approval buttons render only while the
item is still pending **and** still assigned to the signed-in approver — so on that record type the
buttons *are* the gate. Step 8 reads the page before the click and re-reads it after. That also
reorders the buttons-absent diagnosis: already-actioned is now the first hypothesis for a single
item, and the browser-role theory is reserved for when *every* item in the batch shows no buttons,
because the old ordering would have logged a whole batch as actioned on a role mistake.

And the examples are sanitised. Every live value a teammate could copy — company id, tool id, three
custom-field ids, a named subcontractor, a project label, a commitment balance, real bill and PO
numbers — is now a placeholder, and `README.md` no longer claims the plugins carry no customer data
while carrying some. **Defect provenance is deliberately exempt and stays**: *"bill `2325026-07` was
flagged as coded to `PO11120` while applied to `PO16093`"* is the evidence a documented bug was
real, and this repo's epistemics rest on findings being traceable to a record and a date. `CLAUDE.md`
now states that distinction instead of banning both and doing neither.

**Three fixes were to things this session had itself just built**, which is the part worth
remembering:

- Procore's dashboard still filtered on `verdict !== "gone"` after the bin was removed — a filter
  that can exclude nothing — and `prose.md` certified the filter deleted. The reachability check
  missed it because its regex matched only `==`/`===`. Widened to `[!=]==?`, which catches the
  inequality form.
- `check_template_versions()` read only the first version mention per file. Procore's Step 0 stated
  `v5` and tested for `v4` two lines below, so the check written to detect a stale workspace would
  have called a current one stale. It compares every site now.
- The verdict allowlist caught a wrong verdict but not a missing one.

**One thing about the shared-block mechanism is now demonstrated rather than argued.** A wording fix
belonging to `pub-render-archive` was made in `plugins/_shared/`; `--check` failed both plugins for
being out of step, `--sync` pushed it into both, and the build went green. That is the loop working
in anger for the first time, which `prose.md` had listed as unestablished.

**Newly enforced, where a claim used to stand in for a check:** `test_skill_code.py` now runs in CI
(it never did, while `README.md` told contributors it would); `check_onboarding_page()` checks the
four properties `CLAUDE.md` asserted tests for and no file read; `check_execute_prompt_purity()`
keeps procedure out of the authorising message; and an unrecognised Procore response verb now fails
conservatively on both axes — it requires a reason **and** counts as affirmative for the no-support
caution, where it previously answered false to both.

**Not done, and why.** Committing the 2026-08-20 dashboard fixtures: the measurements behind them
were never reproducible and the honest fix was to withdraw the *"a future session need not redo
them"* certification rather than fabricate fixtures after the fact. The `zip`-versus-`xl/` sniff
distinction is documented as a rule rather than implemented in the snippet, because the sniff reads
four bytes and cannot see inside the container — SheetJS yielding no sheets is the real signal, and
that is what the rule now says.

---

## Directions considered and not taken

2026-08-24, from the question of how the catalog should serve someone who is not a
financial analyst. Kept only so they are not re-proposed from scratch. The full
pre-decision write-up that used to sit in `proposals/` was **deleted rather than marked
superseded**: most of it restated `CLAUDE.md` back at itself, which is a drift source,
and the rest argued for a path that was declined.

**Persona plugins, plus a concierge plugin to route people to them — declined.** The work
went into modularity *inside* the two existing plugins instead. Nothing about the
prerequisite test changed, so a genuinely new prerequisite (M365/Teams) is still a new
plugin named for the prerequisite rather than for its first task.

**A skill that interviews the user and then *generates* a bespoke skill — declined, and
this is the one whose reasoning is worth keeping.** The interview and connector-probe
halves are both solvable today. The generation half is the wrong bet here for reasons
that are structural rather than technical:

- A generated skill starts at zero on everything these notes paid for — three-state
  reads, verify-the-record-not-the-queue, the output-filter redactions — and re-earns
  each lesson in production, on systems where the failure mode is a silent wrong
  approval.
- It forks the distribution model. Push-to-`main`-is-the-release works because everyone
  runs the same artifact. A per-user generated skill has no shared version, receives no
  fixes, and is invisible to `validate.py`. The Step 5 PO fix reached every installed
  copy in one push; it would have reached zero generated ones.
- It inverts the house safety convention. *"Neither plugin acts on its own judgement"* is
  load-bearing, and a skill that designed itself is judgment all the way down, with no
  reviewable text a maintainer ever vetted.

**Never fork a skill per persona.** If a second persona ever needs different *checks* over
the same queue, that is a config-selectable review lens inside the one skill, not a
second copy to drift.

**What is actually true about a non-finance user today**, and worth knowing before anyone
designs for one: the plumbing already serves them and the judgment does not. Both queues
are scoped by the system of record itself — Procore's endpoint and permission gate by the
signed-in session, NetSuite's by `next_approver` — so a supply-chain teammate installing
either plugin today would see *their own* queue. But every check encodes a financial
analyst's questions (the G702 identities, contract math, the PO cross-check), while
receipt-against-PO quantities, delivery dates against need dates and lead-time slippage
appear nowhere. They would get a correctly-scoped queue reviewed against questions that
are not theirs.

**Two questions gate any future attempt.** Whether a supply-chain teammate exists who
will sit for an interview and let one run be watched — nothing here should be designed
from imagination, by this repo's own standard. And whether a NetSuite-only supply-chain
skill would be split out of the NetSuite bucket by the audience rule, or given to
everyone.

---

## Retrospective: four rounds spent on a bug that did not exist

2026-08-15. A `javascript_tool` call was reported blocked. Four rounds of probes
followed, two wrong versions of a CLAUDE.md note, and an onboarding section
written and then deleted unshipped. The actual answer: the run had been in
skip-all rather than auto. Nothing was ever wrong.

Three things made it expensive, and only the first is about permissions.

**The mode was reported from memory, and no tool can check it.** An agent cannot
read its own permission mode — there is no tool that returns it. So the single
fact the whole investigation turned on was unverifiable by anyone except the
person at the keyboard, in the moment, and it was misremembered. Everything
converged within one run of pinning it down, and nothing converged before.

**A diagnostic was treated as evidence about the workflow.** The denied probe
fetched five URLs across four CDNs; both skills only ever fetch cdnjs. Two
successive theories — "auto blocks the fetch", then "the classifier objects to
the host list" — were built by generalising from a shape the real thing never
takes.

**A confounded comparison looked like a result.** The before/after runs differed
in the settings *and* in the host list, and the "after" was read as proof the
settings fixed it. The user's own instinct to re-run the control is what caught
it. Change one variable, or the comparison says nothing.

What went right is worth keeping too: the onboarding section reached the branch
and never `main`, because the commit that added it carried the unresolved
confound in its own message. Writing the doubt down at the moment of committing
is what stopped a fabricated troubleshooting step from shipping to teammates.

---

## Retrospective: fewer, larger tool calls

From a review of this session's own inefficiency. Generic technique rather than
repo knowledge, kept here because it was measured on real work.

**The dominant cost is the number of round trips, not the size of any response.**
Each one is a full model inference pass — seconds — while the `grep` itself
returns in milliseconds. Prompt caching discounts re-sent context, so trimming
output matters far less than removing turns.

What actually went wrong, in rough order of cost:

- **Reading one file in eight slices.** `SKILL.md` is ~450 lines and got hit with
  eight separate `sed`/`grep` ranges. Reading it once would have cost fewer
  tokens than the slices summed *and* surfaced every stale reference in one pass,
  instead of discovering them one at a time after editing had started.
- **Serial independent reads.** Git state, the NetSuite step, and the Procore
  recipe were mutually independent and went out as three messages. Batched, the
  tools run concurrently *and* cost one inference pass.
- **Running before reading.** A fixture run failed because `publish_dashboard.py`
  resolves paths from `__file__` and ignored the flags passed to it; five lines
  read first would have prevented two wasted turns. Same for `node --check`
  against a process substitution.
- **Mechanical edits as separate calls.** Renumbering a list 6→7→8→9 was three
  `Edit` calls incrementing a digit. Worth using `Edit` for semantic changes —
  the exact-match guard earns its keep there — but not for pure mechanics.

**The counter-rule:** whole-file reads are right for a 450-line skill and wrong
for a large source file, because those tokens then sit in context for every later
turn. The heuristic is file size, not a principle. Slicing discipline appropriate
to a big codebase backfired on files small enough to just read.
