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
list, and the claims in `docs/onboarding.html` about reading spreadsheets sheet by
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
at two scroll offsets. Those are established, and a future session need not redo
them.

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

## The two dashboards had drifted, and it cost seven defects

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
| 1 | Browser mode could not publish (see gap 7) | A complete review died at Step 7 |
| 2 | No verdict allowlist | A typo'd verdict fell through the pill logic to **"Clear"** — fail-open on the field that decides what gets approved. Procore has aborted on this since it shipped |
| 3 | `var live=null` never assigned | ~45 lines unreachable: the gone/changed states, `newRow`, the bin, and a permanently-`0` "Unreviewed" card |
| 4 | Marks never pruned | A mark for a since-approved bill stayed in `ns_marks_v1` forever and would reappear if NetSuite reused the id. Procore sweeps them |
| 5 | Money card had no rollover | A $2.7m queue rendered `$2702k` |
| 6 | Abort message named `_review_log.json` | The pre-migration name — both copies, so the rename fix reached neither string |
| 7 | Aborted on two unused config keys | `me` and `tool` were injected and read by the page and then never used; only `account` is |

**The drift check that came out of it.** `plugins/_shared/` now holds the canonical copy of
nine blocks, fenced in both plugins by name-matched markers, with `scripts/shared_blocks.py`
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

**Coverage, after the SKILL.md pass:** 13 blocks across 26 sites — 9 in the assets (90 lines)
and 4 in the two `SKILL.md` files (34 lines) — plus a cdnjs version-pin check that needs no
registration. Mutation-tested at every step, including a one-sided pdf.js bump and a reworded
Step 0 paragraph.

**And the honest limit, which is the finding worth keeping from that pass.** The `SKILL.md`
duplication is mostly *near*-identical rather than identical: the same paragraph with the
plugin's own name and workspace folder substituted. Only **72 of ~1,500 lines** sit in
contiguous byte-identical runs, and only ~34 of those have clean paragraph boundaries — a
Markdown comment mid-paragraph splits it, and one inside a fence corrupts code the test
harness evaluates. So the block mechanism can never cover most of that surface as written.
The gap is not laziness; closing it would mean designing the per-plugin names out of the
prose, which is a bigger and separate decision. The blocks that differ by one token
(`ns_marks_v1` vs `pc_marks_v1`, the two log filenames) are the same story in miniature.

**Not fixed, because it is a product decision and not a port:** `widget.html`. Procore
writes a slim copy and its `SKILL.md` says to render *that* as the primary; NetSuite
writes no such file. But `CLAUDE.md` says widget.html is "a fallback … **not the
default**, because folding rows costs their response buttons", and separately says to
render the full thing and never pre-judge the size. Procore's shipped behaviour
contradicts that note. Also, the note's stated cost may be wrong: Procore folds only
`skipped` and `ungated` rows, which have no response buttons to lose. Three sources
disagree; somebody has to decide which is right before either side changes.

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
