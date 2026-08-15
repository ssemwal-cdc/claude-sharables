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

### 1. No end-to-end run, either plugin

The single biggest gap. Every change from 2026-08-13/14 — in-page pdf.js
extraction, the fan-out gate, the bulk `transactionline` query, the size-budgeted
page reads, the attribution note — is verified only against mocks and one live
chat test of pdf.js on bill 2532506.

**To clear it:** run a full review on each plugin, then execute against **one
low-value item**. Compare the verdicts against a previous run's — same figures,
same clear/flagged calls. A difference is a regression until explained.

### 2. The NetSuite notes page

`Approve With Notes` loads a page **nobody has seen**. The one attempt froze the
tab. The skill deliberately says to read that page rather than assume its field
names or button labels, because inventing them would be worse than vague.

**To clear it:** approve one low-value bill and watch where the note lands.
Then tighten Step 5 with the real labels.

### 3. The freeze fallback

The recovery path — abandon the tab, re-read from a fresh page load, fall back to
plain `Approve` only if still pending — has never fired. It cannot easily be
forced.

**To clear it:** you probably can't on purpose. Just know it is untested, and if
a freeze happens, watch what the run does rather than assuming it handled it.

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

### 6. The attachment sniff, on real non-PDF support

Added 2026-08-15 after a report that Excel and image support came back
unreviewed. The classifier and the workbook reader are covered by
`scripts/test_skill_code.py` — 13 magic-number cases, and `__sheets` against a
stubbed workbook. Two things that testing cannot reach:

- **No real Procore `.xlsx` has been read.** The round-trip proved SheetJS on a
  workbook *this code wrote itself*, in the scratch tab, via a live `import()`
  from cdnjs. A vendor's actual bid schedule is a different thing: merged cells,
  multiple sheets, formulas whose cached values may be absent.
- **No real image or scanned PDF has been read visually.** `computer` is
  confirmed to exist and to return a rendered view, but no review has yet gone
  through the navigate-then-look path, and the `scanned` → rasterise → look
  branch has never fired at all.

**To clear it:** run a review over an item with Excel support and one with image
support — the $25.6M B3 NRC package, six attachments over fourteen scope groups,
is the natural candidate. Confirm the verdict names the format when it skips,
and that a workbook's figures actually reach the tie-out.

**The specific regression to watch for:** a skip whose reason is vague. The bug
this replaced said "support present but unreadable", which reads the same whether
the file was a scan, a workbook, or a link that timed out — which is exactly how
whole formats went unread for weeks with nothing in the log to show it. If a skip
cannot name which of the six outcomes caused it, that is the same bug returning.

### 7. Small unknowns

- Whether the desktop app's plugin list shows a commit-hash version. The
  onboarding sheet says "both plugins appear in your installed list" because
  that is definitely visible; the hash check is only documented for the CLI.
- Whether Cowork sessions need the per-conversation connector toggle
  (**+ → Connectors**). Anthropic's docs say connectors are per-conversation;
  the step was removed from the sheet as not matching observed behaviour.

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
