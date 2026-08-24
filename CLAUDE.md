# CLAUDE.md

Working notes for this repo. Claude Code loads this automatically when the repo
is opened as a project.

This repo is a **Claude plugin marketplace**. It ships no application code. Its
only job is to be a catalog that `/plugin marketplace add` can resolve and
`/plugin install` can install from.

---

## If you are being asked to add a skill or plugin

That is the main job here, and it usually arrives as "here is a skill / here is
a zip, add it to the repo." Follow this exactly. Do not improvise the layout —
every rule below exists because breaking it produced a real, observed failure.

### 1. Work out what you were handed

| What arrived | What to do |
|---|---|
| A whole plugin folder or zip (has its own `.claude-plugin/plugin.json`) | Copy it into `plugins/` verbatim. Do not rewrite its files. |
| A bare skill (a `SKILL.md`, maybe with `assets/`) | New plugin, or new skill inside an existing one? Apply the [prerequisite test](#the-prerequisite-test) — it is decidable, so do not guess and do not ask unless it genuinely ties. |
| A zip with junk (`__MACOSX/`, `.DS_Store`, `._*`) | Strip it before copying. |

Copy, then prove the copy is faithful:

```bash
diff -r <source> plugins/<name>    # must print nothing
```

### 2. Required layout

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED — without it the install fails
├── README.md                # what it does, prerequisites, first-run setup
└── skills/
    └── <skill-name>/
        ├── SKILL.md         # frontmatter name MUST equal <skill-name>
        └── assets/          # optional
```

`skills/` at the plugin root is discovered automatically. `plugin.json` needs no
`skills` key. Nothing except `plugin.json` goes inside `.claude-plugin/`.

### 3. `plugin.json`

```json
{
  "name": "<plugin-name>",
  "description": "One sentence a teammate can decide from.",
  "author": { "name": "Shivam Semwal" },
  "keywords": ["..."],
  "license": "UNLICENSED"
}
```

`name` must equal the folder name **and** the `name` in the marketplace entry.

**Never add a `version` field** — not here, not in the marketplace entry. See
[Versioning](#versioning).

### 4. Register it in `.claude-plugin/marketplace.json`

```json
{
  "name": "<plugin-name>",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/ssemwal-cdc/claude-sharables.git",
    "path": "plugins/<plugin-name>"
  },
  "description": "..."
}
```

**Use `git-subdir`, not a relative path.** `path` is a bare repo-relative path
— no leading `./`. Do not pin `sha` or `version`; leaving it unpinned is what
makes every push ship.

A relative-path source (`"./plugins/<name>"`) installs fine from the CLI and
then fails everywhere else. See [Traps](#traps-proven-not-guessed).

### 5. Update the docs

Both `README.md` and this file must stay truthful. `scripts/validate.py` fails
the build if either stops mentioning a registered plugin, so this is enforced,
not merely requested. Add a row to the **Available plugins** table in
`README.md` including its prerequisite and its skill version (a new skill
starts at v1 — see [Skill version lines](#skill-version-lines)).

### 6. Verify before committing

```bash
python3 scripts/validate.py
claude plugin validate ./plugins/<plugin-name>
```

`claude plugin validate` warns `No version specified` — that warning is correct
and intended here. Ignore it.

Then prove an install actually works, which schema validation does not:

```bash
claude plugin marketplace add .                      # local copy, pre-push
claude plugin install <plugin-name>@compass-claude-plugins
claude plugin details <plugin-name>                  # confirm the skill is listed
claude plugin uninstall <plugin-name>@compass-claude-plugins
claude plugin marketplace remove compass-claude-plugins
```

Schema-valid and installable are different things. Check both.

### 7. Commit and push to `main`

Pushing to the default branch **is** the release. There is no other step.

---

## The prerequisite test

**A plugin is the unit a teammate can switch off. A skill is not.** Every
enable / disable / uninstall / scope control takes a *plugin* name, and the one
setting that can silence an individual skill does not apply here — *"Plugin
skills are not affected by `skillOverrides`. Manage those through `/plugin`
instead."* So whatever goes in a plugin, everyone who installs it takes all of,
with no way to drop the part they cannot run.

That makes the boundary a **prerequisite** boundary. Deciding where a new skill
goes:

1. **List its external prerequisites** — what a teammate must already have set
   up *outside* the plugin: MCP connectors, browser-authenticated sites, CLI
   binaries, credentials, tenant access. List prerequisites only. Not the
   topic, the department, or the data domain.
2. **Compare that set to each existing plugin's set, exactly.**
   Identical → the skill **joins** that plugin. Any difference at all → **new
   plugin**. That is the whole decision.
3. **Forcing override — always a new plugin** if the skill ships `.mcp.json`,
   `hooks/`, `bin/`, `monitors/`, `.lsp.json`, or a root `settings.json` that
   should not apply to the candidate plugin's other skills. Those activate on
   *plugin enable*, not on skill invocation, so they fire for every user of
   every other skill in that plugin.
4. **Also a new plugin** if a different subset of the team should be able to
   have it ("only Finance sees this") — prerequisites are the usual proxy, but
   audience counts on its own.

**Not reasons to split**, explicitly rejected: different topic or department;
different data domain; a different dashboard; "it feels unrelated"; the plugin
would then hold more than one skill; one-thing-per-folder tidiness.

Pre-decided, so these need no thought:

| New skill | Goes |
|---|---|
| Reads NetSuite via the MCP connector | **inside** `plugins/netsuite-approval-review/skills/<name>/` |
| Driven through Claude in Chrome against Procore | **inside** `plugins/procore-open-items-review/skills/<name>/` |
| Needs a connector neither plugin needs (Monday, M365, …) | **new plugin**, new marketplace entry |

Adding a skill to an existing plugin does **not** touch `marketplace.json` —
`skills/` is discovered automatically. Update that plugin's README and the
repo README row.

**Naming:** once a plugin is a prerequisite bucket, `netsuite-approval-review`
reads oddly as the home of a second NetSuite skill. **Do not rename** — the
name must match the folder and the marketplace entry, and teammates installed
by name, so renaming forces everyone to uninstall and reinstall. Treat the two
existing names as "the NetSuite bucket" and "the Procore bucket", and name any
*future* plugin after its prerequisite (`monday-tools`) rather than its first
task.

**When the catalog passes ~4 plugins** and teammates are running four-plus
install commands, publish a dependency-only bundle plugin — a manifest of
nothing but `{name, description, dependencies: [...]}` using **bare string**
entries, which track whatever version the marketplace provides and need no git
tags. One install command, every plugin still independently disableable. Do not
build it at two plugins.

**The reason a bundle is worth anything: auto sync does not install new
plugins.** It keeps *already-installed* plugins current, which is why a push to
`main` reaches everyone who has the plugin. A plugin nobody has installed yet
just appears in their catalog and sits there. So every new plugin is another
announcement plus another `/plugin install` for every teammate, and that cost is
what the bundle removes — not the updating, which already works.

**`scripts/validate.py` will reject the bundle as written.** Lines 146–155 fail
any plugin with no `skills/` directory or an empty one, and a dependency-only
manifest has neither. So the bundle needs a validator carve-out *before* it can
ship — check for a `dependencies` key and skip the skills requirement for that
case. Nobody has needed it yet, but the instruction above and the validator
currently disagree, and the failure lands on whoever tries it rather than on
whoever wrote the advice.

---

## Two other files worth knowing about

**`prose.md`** holds findings and retrospectives rather than rules — and, more
usefully, **the standing list of what has not actually been observed yet.** A
good deal of recent work is mock-verified and shipped but has never been watched
running on real data. Read it before citing anything recent as established.

**`scripts/shared_blocks.py`** holds the cross-plugin drift check described under
[Shared blocks](#shared-blocks-edit-pluginsshared-then-sync). `validate.py` runs it, so
it is a build gate rather than a habit.

**`scripts/test_skill_code.py`** runs the executable code the skills carry —
the pdf.js layout extractor, the size-budgeted page reads, the Procore gate's
three-state fan-out, and the CCO ungated demotion. It extracts each one **from
`SKILL.md` itself**, so it tests what an agent will actually paste rather than a
copy that can drift. Run it after touching any of that code; it is fast and needs
only `node`. It is mutation-tested — collapsing a 429 into `empty` makes it fail,
which is the whole point of it existing.

---

## Shared blocks: edit `plugins/_shared/`, then sync

The two plugins carry a lot of byte-identical machinery, and **they cannot share it at
run time.** `${CLAUDE_PLUGIN_ROOT}` resolves per plugin and a `git-subdir` install ships
only `plugins/<name>/`, so every shipped file has to be complete on its own. Runtime
sharing is not an option that exists; do not go looking for it.

What is shared instead is a **maintainer-side canonical copy plus a check**:

```
plugins/_shared/<name>.block     the canonical content
<a plugin file>                  the same content, fenced by markers naming the block
```

Markers are matched by name, not by comment syntax, so each site uses whatever comment
is valid at that point — `//` in a script block, `#` in Python, `<!-- -->` in markup:

```
  //__SHARED:dash-nav__
  ...content...
  //__END_SHARED:dash-nav__
```

**The workflow, and it is the whole point:** edit the file in `plugins/_shared/`, then run

```bash
python3 scripts/shared_blocks.py --sync     # pushes canonical into every marked site
python3 scripts/shared_blocks.py --check    # what validate.py runs
```

`scripts/validate.py` runs the check on every build, so **a fix that reaches one plugin
and not the other is now a failed build** rather than a missed diff. Editing a shipped
copy directly is not wrong, it just fails the check until you move the change into the
canonical file — which is the reminder doing its job.

**`plugins/_shared/` never ships.** `validate.py` skips directories starting with `_`, so
it is invisible to the orphan check, and it is not inside any plugin, so no install can
see it. That underscore is load-bearing.

**Why this exists, in defects rather than principle.** As of 2026-08-24 the two dashboard
templates were 54.5% line-identical and the two publish scripts 54.9%, kept in step by
hand — and **10 of the 22 commits that ever touched a `SKILL.md` had to touch both**,
every one of them a mechanics or convention change, not one a change to a financial
check. Six defects had accumulated in that gap, each one a fix that reached one plugin
and never the other: a fail-open verdict that rendered as "Clear", a mark store that was
never pruned, a money card that printed `$2702k` for $2.7m, an abort message naming a
file that no longer existed. Full list in `prose.md`.

**Adding a block:** put the content in `plugins/_shared/<name>.block`, fence the identical
region in both plugins with markers, and run `--check`. The block must already be
byte-identical in both — this mechanism enforces sameness, it does not create it, and a
block that differs by even one token (`ns_marks_v1` vs `pc_marks_v1`) is not a candidate
until that difference is designed away. A canonical file nobody references fails the
build, as does a marker naming a canonical file that does not exist.

**`SKILL.md` blocks have two extra rules, both learned the hard way.** A marker is a
line, and in Markdown a comment line dropped *inside* a paragraph splits it in two, so
every block must begin and end on a **paragraph boundary** — never mid-sentence, never
inside a numbered list item. And a marker must never land inside a fenced code block:
the ```` ```bash ```` and ```` ```javascript ```` fences are content, and
`scripts/test_skill_code.py` extracts the javascript ones and *evaluates* them.

Those two rules are why the `SKILL.md` coverage is smaller than the duplication
suggests. **Most of what the two skills share is *near*-identical, not identical** —
the same paragraph with `netsuite-approval-double-check` and `NetSuite Approval Checks`
swapped for the Procore names, or a path that differs. Measured 2026-08-24: only **72
lines** sit in contiguous byte-identical runs across the two 800-and-660-line files, and
of those only about **34** have clean paragraph boundaries. The rest — including most of
the Step 0 ladder, whose rung 2 carries a per-plugin asset path mid-list-item — is not
eligible until that difference is designed away. Do not force it by rewording one
plugin to match the other; the names are correct as they are.

**Library version pins are checked separately, not shared.** `check_pins()` in
`shared_blocks.py` asserts that every `cdnjs.cloudflare.com/ajax/libs/<lib>/<version>`
reference agrees across all plugins — today pdf.js 4.0.379 and xlsx 0.18.5. This is
deliberately *not* a shared block: the loaders sit inside javascript fences (see the
rule above), and the two skills wrap them in genuinely different prose because NetSuite
loads pdf.js in the record tab, where the `media.nl` fetch needs the session cookie,
while Procore loads it in an S3 scratch tab. The surrounding text differs for real
reasons; only the version may not. A one-sided bump is the drift worth catching, and it
needs no registration — any new cdnjs library is covered the moment it appears.

**What is deliberately *not* shared:** anything genuinely per-domain — NetSuite's
type/vendor filter axes against Procore's campus/building/type, the `M/D/YYYY` vs ISO
date parsing, NetSuite's three fixed buttons against Procore's verbs read from the
workflow step, and the record-URL shapes. Those differ for real reasons. Do not force
them into a shared block to raise the percentage.

---

## Traps (proven, not guessed)

Verified against Claude Code v2.1.227 by reproducing each failure.

**Relative-path sources install from the CLI and fail from the desktop app.**
This is the subtle one. `"source": "./plugins/<name>"` works perfectly in the
terminal, so it looks correct. It then fails in the Claude desktop app's
Settings → Plugins browser, where the catalog lists both plugins but clicking
install returns only:

> Plugin couldn't be installed. Try again.

Cause, from Anthropic's docs on the equivalent URL-based case: a surface that
holds `marketplace.json` **without a clone of the repo** has nothing for a
relative path to point at — *"URL-based marketplaces only download the
`marketplace.json` file itself. They don't download plugin files from the
server. Relative paths in the marketplace entry reference files on the remote
server that were not downloaded."* The CLI works only because `marketplace add`
clones the whole repository.

`git-subdir` entries are self-contained — they carry their own `url` and
`path`, so they resolve with or without a local clone, and they are supported
by org sync too. `scripts/validate.py` rejects a relative-path string.

**A bare folder name is invalid outright.**
`"source": "netsuite-approval-review"` passes a JSON syntax check and fails at
install with:

> This plugin's marketplace entry is invalid: source: Invalid input

**`metadata.pluginRoot` does not work. Do not use it.**
Anthropic's docs say `pluginRoot: "./plugins"` lets you shorten `source` to a
bare name. It does not. That combination fails as above; and `pluginRoot` plus
`"./name"` passes validation but resolves the source *from the repo root
anyway*, failing at install with:

> Source path does not exist: /…/<repo>/<name>

Use a `git-subdir` source and leave `pluginRoot` unset.
`scripts/validate.py` rejects the file if it reappears.

**Asset paths must use `${CLAUDE_PLUGIN_ROOT}`.**
Both skills reference assets as
`${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/assets/<file>`. A bare `assets/…`
path works in the repo and breaks once installed, because at run time the
working directory is the user's workspace, not the plugin. The validator
rejects bare paths.

**The widget host and the artifact host expose disjoint bridges.** Probed live
from inside each surface, 2026-08-11:

| | `show_widget` | artifact |
|---|---|---|
| origin | `https://<hash>.claudemcpcontent.com`, framed | `cowork-artifact://local/<id>` |
| `sendPrompt` / `openLink` | bare globals, functions | absent everywhere |
| `callMcpTool` / `askClaude` / `runScheduledTask` | absent | present on `window.cowork` |

Zero overlap, and two different namespacing conventions. The consequence: **an
artifact cannot send a message to chat.** A dashboard button that hands an
instruction back to the conversation is inert there, and fails closed — no
throw, no console output, nothing. `askClaude` is not a substitute; it runs a
small model in-page and returns to the page, so it cannot start a turn with real
tool access.

Both dashboards therefore render with `show_widget`, not `create_artifact`. The
cost is that `callMcpTool` is unavailable, so a page cannot re-query its own
data — the NetSuite dashboard used to do this on open. That check now lives in
the execute turn, which is strictly better: an on-open query is already stale by
the time execute is pressed, while a check in the moment before the click has no
window at all.

Do not "restore" the artifact path for persistence. A shareable URL was
considered and rejected — NetSuite and Procore are the systems of record, and
one-click execute is worth more than a link.

**The widget port is confirmed working end to end**, NetSuite, 2026-08-12. The dashboard
renders inline in the conversation and pressing execute puts the instruction straight into chat as
a new message — one click, no clipboard. So `window.sendPrompt` on the widget host takes a bare
string and really does post. The clipboard handoff in the template is now only the artifact-host
fallback and should never be reached in normal use.

**`show_widget` takes content inline only, and handing it a path fails silently.**
Schema read live, 2026-08-12: three properties — `loading_messages` (array of
strings, the only required one), `title`, `widget_code`. No path, no file, no
src. Nothing in the description mentions a byte, character, line or token limit
either, so there is no documented ceiling to design against.

Passing a file path where the content goes **does not error**. It returns
"Content rendered and shown to the user" and renders the path string itself. So
the obvious optimisation — hand over a path and skip reproducing the HTML —
looks like it worked and quietly shows the user a line of text instead of a
dashboard. Do not try it, and do not trust the success message on this tool as
evidence that the right thing rendered.

The whole document therefore has to go through the tool call. **That is not the
same as a size limit, and the difference cost two rounds of work.** Confirmed
2026-08-12: the complete Procore dashboard — 99 KB, 43 items — rendered in a
single call. Two runs before that had refused it on size grounds without
attempting it, one reading 929 of 1849 lines and extrapolating the rest.

So there is no known ceiling, and every threshold anyone has proposed for this
tool has been invented, including by these notes. Render first. The template
carries a guard that turns a truncated render into a red banner precisely so the
question can be settled by observation rather than by estimate — an estimate is
not an observed failure.

`publish_dashboard.py` still writes a slim `widget.html` beside the full
`index.html`. It is a fallback for a queue that one day genuinely does not fit,
not the default, because folding rows costs their response buttons and nothing
yet justifies paying that.

**That note and Procore's `SKILL.md` disagreed for a while, and the note was
right.** Procore rendered the slim copy as its *primary* dashboard, justified as
"roughly a fifth smaller". Measured 2026-08-24 across five fixture queue mixes,
the real figure is **0% to 12%** — 0% when nothing is skipped or ungated, 2–6%
on a realistic mix — because only those two verdicts fold and a live queue is
mostly neither. At the large end 113 KB became 101 KB, which crosses no
threshold anyone has observed. Procore now renders `index.html` like NetSuite,
and the slim copy is reached only when the integrity banner fires.

**NetSuite cannot have this feature at all, and that is structural rather than
an omission.** Its verdict vocabulary is exactly `("clear", "flagged")`, which
is precisely the slim build's *actionable* set, and the fold branch is the
`else`. So nothing would ever fold: the output would be a byte-for-byte copy of
`index.html`, every run. NetSuite has no `skipped` concept by design — a missing
attachment **flags** an item rather than skipping it (Step 4). It also could not
be a shared block even if it were wanted, because the folded keep-list is
per-domain (`projLabel`, `due`, `pid`, `cid`, `kind`, `wf`, `key` against
NetSuite's `trandate`). Do not add it for symmetry.

**The render is unverifiable from the agent's side, which is why it keeps being
declined.** `show_widget` returns `Content rendered and shown to the user`
whatever it rendered — the path test proved it says that while showing a line of
text. The integrity guard raises its banner to the *user*, not to the caller. So
an agent asked to render a large file is being asked to take an unobservable
risk with someone's approval queue, and refusing looks like the careful choice.

Four rounds of rewording did not shift that, and the note above about not
trusting this tool's success message probably reinforced it. The fix is not more
reassurance: it is to close the loop by asking the user to report the banner, one
sentence after the render. Both skills now do that.

**Runs began presenting the working files as chat file cards, 2026-08-21.** The
template, publish script, review log and rendered index all appeared as
download cards at the end of a run. Nothing in either skill asks for that —
newer harness builds push agents to surface files a run wrote, and the state
files pattern-match "deliverable". Both skills now carry an Absolute rule that
the widget is the only deliverable and the working files are never attached.
If cards still appear with that rule shipped, it is the surface auto-listing
written files, and no skill wording can suppress it.

**Do not let an agent refuse to render because the file looks big.** A 120 KB Procore dashboard was
handed over as a file instead, on the reasoning that it might truncate — which cost one-click
execute entirely to avoid a risk that had not happened. The truncation guard exists precisely to
catch that case after the fact. Render first, believe the guard, fall back only on an observed
failure.

**NetSuite runs pdf.js in-page, so neither skill downloads attachments now.**
Tested live 2026-08-13 against bill 2532506 before any file was changed, which is
the order worth keeping — the question "will CSP allow it" is answerable in a
chat in ten minutes and gates the whole design. It does allow it: `import()` from
cdnjs inside an `*.app.netsuite.com` tab loads, the worker fetches as text and
assigns as a blob URL exactly as Procore's recipe does, and a credentialed
same-origin fetch of `/core/media/media.nl?...` returns the PDF. Nothing reaches
disk.

The reason NetSuite loads pdf.js in the *record* tab, rather than a scratch tab
like Procore, is that the media URL needs the session cookie — so the fetch must
be same-origin, so pdf.js has to be wherever that origin is.

**Do not port Procore's `items.map(z => z.str).join(' ')` to NetSuite.** It
flattens the page and destroys column alignment, which is what the quantity x
rate and line-tie checks read. NetSuite rebuilds rows from pdf.js geometry
instead — bucket by y, sort by x, pad by a character width derived from
`item.width / str.length`. Checked against `pdftotext -layout` on a 3-page
utility invoice: same three columns, same figures. Both tools merge left and
right columns on a two-column page when rows share a y-coordinate, so that is a
parsing constraint to split on an x-threshold, not a regression to fix.

**`getDocument({data: arrayBuffer})` throws `InvalidPDFException` on valid
bytes.** Right content type, right `%PDF-1.6` header, 1,126,323 bytes, and it
still throws. `new Uint8Array(ab)` fixes it immediately. Procore's recipe always
wrapped, which looked like style and is load-bearing — both skills now carry a
comment saying so, because the wrap is exactly the kind of thing a later pass
removes as redundant, and the error it produces sends you debugging the download
instead of the call.

**Extracted PDF rows can trip the query-string output filter.** Returning a whole
page came back `[BLOCKED: Cookie/query string data]` — the payment stub's barcode
rows and a 30-digit remittance string read as query-string data. Dropping rows
matching `/^[\s01]{12,}$/` and `/\d{20,}/` clears it at a cost of 15 of 60 rows,
all stub noise, no figures. Long returns also truncate, so pages come back one
per call. Procore already documented this filter for JavaScript source; this is
the same filter reached from a direction the note did not cover.

**An approval comment is now a specified default, not something composed.** A run
invented "Approved by Claude", then stopped a 15-item $61.2M batch to ask whether
to keep it — reasoning that an auditor might question who reviewed the figures.
That hesitation came from the wording being improvised: an agent that made up the
text has something to second-guess. Specifying it removes the question.

Every affirmative response in **both** skills now carries `Approved by Claude`,
and a comment the user supplies for that item replaces it verbatim. Nothing else
is ever typed into a comment or note field. **This is a better default than blank** — a
response recorded with no comment reads as though the user clicked it, while the
attribution says what actually did. Rejection reasons are still required from the
user and never defaulted, because that is the case where boilerplate would be
actively harmful.

Both skills also now state that the user is one reviewer among several and not
the accountant of record, so an authorised batch is not stalled over amounts or
audit exposure. The mechanical checks are unchanged and still stop the batch.

**Both skills default the note. NetSuite routes every approval through Approve
With Notes so it can attach one** — a deliberate exception to "click only the
button named in the instruction". Plain Approve is reached only as the fallback
below. Reject is never substituted for either, in any direction.

**Approve With Notes is a same-tab page navigation, not a popup.** A tab froze
once immediately after that click — renderer locked, tab dropped out of the
automation group, note never typed — and the run correctly verified two ways and
refused to re-click. That freeze got diagnosed as a blocking native dialog, and a
`window.prompt` override was designed on that reasoning. **It was wrong.** The
button just loads an ordinary page in the same tab; there is no popup and no
native dialog, so the freeze was a transient hang and the override would have
overridden nothing. It was never built only because the design was checked
against the live UI first. Do not reintroduce it.

So a freeze is an **unknown** outcome, never a failed one. Recovery is a fallback
to plain Approve, gated on **a fresh page load, never SuiteQL.** The connector lag
documented above means an unchanged reading is *not yet*, never *failed* — gating
the fallback on a connector read would eventually click twice on a bill that had
already been approved. A page load reads the UI and has no lag. Still pending →
click Approve and log that the note was lost. Already advanced → click nothing,
log it as approved without a note.

**Plain Approve can no-op silently, and the mechanism is now pinned.** 2026-08-15,
five identical clicks with zero effect: the button's handler loads a client script
asynchronously and only then calls `win.open` — by then the click's transient
user-activation has expired, so Chrome drops the navigation with no error, no
dialog and no network request. The post-click page read is the only thing that
catches it, which is that verification rule earning its keep yet again. Recovery,
now in Step 8: **one** click, page-load check, then **navigate the approval URL
read verbatim out of the button's own handler** — parameters asserted (`recid`,
`acttype`, the user's approver id), fired once, same server path and same audit
trail as the button. It is the button's own request minus the dropped `win.open`,
not a REST bypass, so the never-`ns_updateRecord` rule is untouched. Affirmative
only, never Reject, and it carries no note. Confirmed live on record 2534442
after five dead clicks. Do not "fix" this by re-clicking harder, and do not
promote the URL to the primary route — Approve With Notes stays primary because
it is the only path that can attach the note.

**A CCO's workflow hangs off the commitment change order, not the package — which
closed a gap the skill had given up on.** Found by a teammate running the plugin,
2026-08-13. Step 2 used to say `ChangeOrderPackage` returns a 400, *"Those items
cannot be gated"*, so every CCO rendered `ungated` with no response buttons for
everybody.

The 400 is real, and so is the same 400 on every other package-style type string
and on the record's own `CommitmentContractChangeOrder`. What made it look
unsolvable is where the error points: a company-level `workflows/tools` endpoint
that an ordinary account gets a 403 on, which reads as a permissions wall. It is
not one. The workflow simply is not attached to that object. Querying
`workflowable_object_type=CommitmentChangeOrder` with the **commitment change
order id** returns the instance immediately.

That id is not the package id. **It is `line_items[].holder.id` on the package
payload** — confirmed 2026-08-14 against five packages, all five of which then
gated as actionable at Financial Analyst Review. That closes the open question
this note carried for a day: the first version said an API field might hold the
id, nobody had confirmed which, and the browser redirect was the method until
someone did. Someone did.

Two consequences worth keeping.

**The read now precedes the gate, for CCOs only.** Every other item type is
gated first so the fan-out can discard the noise cheaply, and inverting that for
one type looks like an inconsistency to tidy up. It is not: the read is what
produces the lookup id, so a CCO cannot be gated before it is read. The wasted
reads are bounded by the CCO count, which is small, and the alternative is no
gate at all.

**A package can span several commitment change orders**, since `holder` is per
line rather than per package. Dedupe across the lines: one id is the answer,
several means there is no single workflow instance the queue's one row stands
for, and the skill reports the ids and leaves it `ungated` rather than choosing.
Choosing would be a guess with the silent failure mode described below.

The `fetch(packageUrl, {redirect:'follow'})` trick the skill briefly carried is
**gone, deliberately.** It read `response.url` to resolve all the ids in one
call, and was hedged about because a client-side route resolution returns the URL
you sent — the package id — which is precisely the wrong id. `holder.id` gets the
same saving with none of that, so the hedge is dead weight. Do not reintroduce it.

The independent check on all of this is the UI, and it is worth keeping because
the failure mode is silent: open the change order record and a genuinely
actionable item renders a live **Respond** button naming the user against the
current step's role. Observed on CE #019 — Respond shown, user named as Financial
Analyst, gate returning `can_respond` true at Financial Analyst Review. Two
independent sources agreeing is what makes the recipe trustworthy; the gate alone
cannot detect its own miss.

**CCOs at Financial Analyst Review offer Approve / Revise and Resubmit**, the
invoice verbs, not the change risk's Yes / Reject. Worth stating because the
wrong guess is the intuitive one — a change order and a change risk are both
change work, so the pairing reads as though it should follow the subject matter.
It follows the step.

**The wrong id does not 400 — it returns 200 with zero rows, and that is worse.**
Corrected from a live run 2026-08-15; the earlier note here said it 400s. Two
different failures, and only one of them is loud:

- wrong **type** (`ChangeOrderPackage`) → **400**, unmissable
- right type, wrong **id** (the package id) → **200, empty**, indistinguishable
  from *no workflow instance exists*

Since that is exactly what the execute step reads as *already actioned elsewhere*,
the package id produces a clean success that logs a live item as done. **This is
what made CCOs look ungated to begin with.**

**Two more from the same run, both worth keeping.**

`per_page=100` is **required** on `workflows/instances`. On the default page size
the endpoint hid live instances outright — most likely the page window is applied
before the filters, so on a project with many instances the filtered one is not on
page 1. It now rides on every gate query, for every item type, because an empty
response becomes `empty` becomes *skip it*.

And **the 400 body's pointer is real, just version-shifted.** It names a
company-level `workflows/tools` endpoint; **v1.0 403s for an ordinary account**,
which is what made it read as a permissions wall, but
`/rest/v2.0/companies/<company>/workflows/tools` **works** and lists the valid
type strings. That is the tool to reach for if a fourth `item_type` ever appears,
instead of guessing candidates.

**The dangerous part is the failure mode, not the 400.** The execute instruction
treats a lookup returning no instance as *already actioned elsewhere* and skips
the item. So a wrong id does not raise an error — it silently logs a live item as
done. That is why `publish_dashboard.py` demotes a CCO with no `wfId` to
`ungated` and prints a warning, rather than falling back to the package id.
`ungated` items render Resolve-the-gate instead of response buttons, so an
unresolved id cannot reach the execute list at all. Keep that guard if the
lookup is ever changed.

The type is per item now (`wf`) with `wfId` beside it, because the queue's
`item_type` and the workflow endpoint's type are not the same thing and the old
kind-keyed constant assumed they were.

**A bill's PO comes from the transaction linkage. `custbody3` is a typed reference and
has never been the coding.** Found by a teammate running the plugin and confirmed against
production 2026-08-20. The skill flagged bills as *"coded to the wrong PO"*; NetSuite's
System Information did show a "PO #" field with the wrong PO, but **Related Records →
Purchase Orders showed the right one**. The teammate was right and the flags were false.

| Bill | `custbody3` (typed) | Real `OrdBill` link | The record's own contract field |
|---|---|---|---|
| `2325026-07` (2534437) | `PO11120` | **PO16093** | `5,400` — PO16093's contract |
| `182743734-0004` (2535881) | `PO16033` | **PO16034** | `284,078.31` — PO16034's contract |

Both bills were correctly coded, and **both records carried a second field that agreed with
the linkage and contradicted the flag.** Neither was read.

It was systematic, not two records. All four Sunbelt diffuser bills read `PO16033` and all
four are applied to `PO16034`; three were already **approved**. So the flag's headline —
*"$182,526.82 cumulative on the wrong PO"* — was phantom: that is PO16034 at 64% of a
`284,078.31` contract, on the correct commitment. Acting on it meant chasing reversals on
correctly posted transactions. The other flag claimed PO11120 was at *"130% of contract,
$478,012.50 billed"*; the two bills actually applied to it total exactly its `372,500`.

**Three compounding defects, all now fixed in Step 5.**

- **A typed reference read as the coding.** `createdfrom`,
  `previoustransactionlinelink`, `linkedtrans` and "Related Records" appeared **zero times
  in the whole repo**. Step 2 even queried `transactionline` — the right table — and never
  asked it for the link.
- **Contract and billed-to-date computed off two unjoined keys.** Contract from a `tranid`
  string match; billed-to-date from a vendor + memo `LIKE` sum with **no PO predicate at
  all**, so it swept in bills applied to other POs. That is where the `$478,012.50` came
  from.
- **The zero-evidence was inverted.** *"The PO the invoice names has $0 billed"* is the
  **expected** reading for a first draw and for any pending bill — a pending bill has
  incremented nothing. It was being offered as corroboration of miscoding. The history
  query selected `approvalstatus` and no rule ever spent it.

**`linktype = 'OrdBill'` is the filter and it is not optional** — the same PO also emits
`ShipRcpt` rows for the same bill. And **the link table carries one row per line pair, not
per document**: a three-line bill returns three `OrdBill` rows, and a naive `SUM` across the
join returned exactly 3× the truth (`136,369.02` came back as `409,107.06`). Deduplicate to
distinct bill ids before aggregating, always.

**Three states, never a boolean:** `linked` (that PO is the coding, authoritative),
`unlinked` (the query succeeded and found none — the typed value is all there is, and say
so), `failed` (the query errored — unknown, and **never** `unlinked`). This is the **fifth**
instance of the shape these notes had already written down four times — the fan-out's
`empty` vs `failed`, the CCO wrong-id returning 200-empty, a workbook read as `expired`, a
`[BLOCKED:]` marker read as an empty field. The PO path was the one major step where the
principle had never been applied.

**A typed reference that disagrees is a data-entry note, not a misallocation.** Report it —
a wrong reference field is a real data-quality problem worth telling AP — but it never
flags an item on its own and never produces a sentence about money on the wrong PO. The
signal was real; only its category was wrong.

Worth keeping about how this was caught: **the teammate's two independent sources
disagreeing is what settled it**, the same device that made the CCO recipe trustworthy. The
skill could not detect its own miss, because a `tranid` match resolves whatever string it is
handed and returns a clean, plausible answer about the wrong PO.

**Both skills fan out their reads now, and the fan-out has one failure mode that
governs the whole design.** Procore's gate used to issue one GET per queue item
across a ~73 item queue, ~41 of them only to learn the item was noise; NetSuite
re-read each record page with `get_page_text` when Step 1a's bulk query already
carried most of those fields. The dominant cost in both was **round trips**, not
the size of any one response.

Turning *N* sequential requests into *N* concurrent ones changes what a failure
looks like. A request that fails and returns nothing is indistinguishable from an
item with no workflow instance — which both skills define as *already actioned
elsewhere, skip it*. So a blip silently suppresses a live item and logs it as
done, plurally and quietly. Same bug class as a CCO resolving to the wrong
`wfId`.

Hence every fan-out returns one of **three** states per item — `ok`, `empty`
(the API genuinely returned nothing), `failed` (with the code). A `failed` is
named and excluded; it is never folded into the suppressed count. A 429 from
rate limiting is a `failed`, not an `empty`, which is why concurrency is capped
at 8–10 rather than let rip. **Never collapse those three back into a boolean.**

**Batching attachment extraction collides with the scanned-PDF branch.** The
presigned window is per window, not per file, so batching inside it is free — but
an expired link yields no text, and "no text" already means *"support is a
scanned image"*. An overrun batch therefore converts live invoices into `skipped`
verdicts nobody ordered. Only a **successful fetch** that parsed and yielded
nothing is a scan; a failed or expired fetch is re-navigated and retried.

**Both skills read every attachment as a PDF, and everything else fell into the
wrong bucket.** Reported from production 2026-08-14: PDFs review fine, Excel and
image support comes back unreviewed. It is not a limitation — it is one missing
type check, and the misfiling is what hid it.

Neither skill sniffed the bytes. `getDocument` throws `InvalidPDFException` on a
workbook, which is the same error a corrupt download gives, and both skills then
read that error through a two-state rule that had no room for it. Procore's said
*"fetch failed, **or a non-PDF** … → expired, retry it"* — a clause written for
S3's expired-signature XML, which a spreadsheet also satisfies. So Excel support
was re-fetched, failed identically, and landed as `skipped`, sometimes described
as *"a scanned image"*. The retry had no exit and no type check, so a format that
could never parse was retried forever. NetSuite was blunter still: *"Non-PDF
attachments are unusual; handle them the same way and note the type"* — an
instruction to feed a workbook to pdf.js, resting on an assumption about
frequency that was simply wrong.

**This is the same bug class as the CCO `wfId` and the fan-out's `empty` vs
`failed`** — a distinct failure folded into a category that means something else,
so it never surfaces. The principle was already written down twice and had just
never been applied to file formats. Six outcomes now, kept distinct: `text`,
`spreadsheet`, `image`, `scanned`, `expired`, `unsupported`. **`scanned` is the
narrow one** — the bytes were a PDF, it parsed, and it yielded almost nothing.
Anything that threw is named by what the bytes were.

Two rules that fall out and should not be relaxed:

- **A retry is only legitimate for `expired`.** Bounded at two. A file that
  parsed as the wrong type will parse as the wrong type again.
- **A skip must name which outcome caused it.** *"Unreadable"* is what hid this:
  it reads identically whether the file was a scan, a workbook, or a link that
  timed out, so entire formats went unread with nothing in the log to show it.

**Images get looked at, not OCR'd, where there is any choice.** Chrome renders the
file, so navigating to it and reading it visually is both more accurate and free
of any CDN. OCR is the fallback only, and **an OCR-derived figure never produces a
`clear` verdict** even when the arithmetic ties — it is labelled
`read by OCR, not independently verified` and left flagged for a human. A misread
digit in an eight-figure line is worse than an honest skip, and a table is exactly
where OCR misreads. If that cap ever feels noisy, fix the visual read; do not relax
the cap.

**`javascript_tool` can be denied by Cowork's permission classifier, and that is
the one failure that stops both skills dead.** Hit 2026-08-14 running the CDN
probe: the call was blocked before it reached the page, in auto mode, with the tab
already open and correct. Everything load-bearing in both skills goes through that
tool — the Procore gate fan-out, every attachment read, the NetSuite bulk query —
so a denial is not a degraded run, it is no run.

Two things follow. **The agent was right to stop rather than route around it**, and
right to reject the sandbox as a substitute: the sandbox is a different network and
CORS environment, so a result from there would not have answered the question it
was asked. Refusing to launder a denial through a different execution context is
the correct instinct; keep it.

And **it is worse on a schedule than in a chat.** The site-access prompt already
has a note above about picking the *always* option because a run stalling on a
prompt nobody is watching reads as a hang. This is the same shape one layer up, in
the permission classifier rather than the browser, and it fires on the first
`javascript_tool` call of every run. Approve it once, or add a rule for
`mcp__claude-in-chrome__javascript_tool`, before relying on a scheduled window.

**Auto mode works, and no permission configuration is needed for either plugin.**
Settled 2026-08-15 by re-running the exact snippet that had once been denied:
byte-identical code, no `autoMode` block, auto mode — it passed, with no prompt.
Every operation either plugin performs has now run clean in auto.

The single denial that started all this was **environmental — the run was in
skip-all, not auto.** Nothing about the code, the hosts, or the configuration.

**The root cause of the detour is worth more than the finding: an agent cannot read
its own permission mode.** There is no tool that reports it, so *"which mode was
that run in"* is unanswerable after the fact and can only be recorded by the person
at the keyboard, at the time. Three rounds of investigation and two wrong versions
of this note rested on a mode remembered afterwards. If a permission question ever
comes up again, **capture the mode at the moment of the run** — everything else
follows from that one fact, and without it no amount of probing converges.

Two smaller rules earned along the way:

- **Do not generalise from a diagnostic to the workflow.** The probe that was
  denied fetched five URLs across four CDNs; both skills only ever fetch cdnjs. A
  test that fails in a way the real thing cannot is not evidence about the real
  thing.
- **Do not mine the denial text.** *"Reason: Blocked by classifier"* is the
  documented fixed string from v2.1.208 on — the classifier scores severity
  internally rather than explaining. It will never contain a clue.

An onboarding section was written for a scheduled-run hang that turned out not to
exist, and removed unshipped. **Do not add one without a reproduction.**

`autoMode.environment` is therefore **not recommended** — it is config with no
demonstrated purpose, and unused config rots. The block is in this file's git
history if something is ever genuinely blocked; add it then.

**Still do not use skip-all**, on the documentation's own grounds rather than
ours: *"Only use this mode in isolated environments like containers or VMs where
Claude Code can't cause damage."* That is the exact opposite of a browser signed
into Procore and NetSuite with live approval authority. **Auto for everything.**

**`javascript_tool` can serialise a returned Promise as `{}`.** Observed the same
day: an `(async () => {…})()` IIFE returned the literal empty object, because the
bridge serialised the pending Promise before the fetches resolved. It is not an
empty result, it is a **null** result, and reading it as "everything came back
empty" would be the same misfile as every other bug in these notes.

Both skills already use the safe shape — **top-level `await`**, and named async
functions on `window` that are then awaited by a later call. That is load-bearing,
not style. Do not tidy either into a self-invoking async IIFE.

**The bucket-root scratch tab is an XML document, and `document.createElement` does
not work there.** Also 2026-08-14, found because the probe's canvas check threw:
`document.contentType` is `application/xml`, so `createElement('canvas')` yields a
null-namespace element with no `getContext`. The XML content type is exactly why
that tab was chosen — it is attachable where a PDF is not — so this is permanent.
Use `OffscreenCanvas`, or `createElementNS` with the XHTML namespace, and never
move the tab to an HTML page: it has to stay same-origin with the presigned link or
the fetch hits the CORS wall. NetSuite is unaffected, since it runs pdf.js in the
record tab, which is ordinary HTML. Do not normalise the two.

Worth noting how this surfaced: it was an incidental error in a probe written to
ask about something else, disclosed rather than smoothed over. The canvas line in
the probe was mine and it was wrong. A run that had quietly caught the exception
and reported four clean CDN results would have left a broken `page.render` in the
skill to be discovered later, by a scanned invoice, in production.

**The workbook reader is settled, and the simplest loader won.** Probed live
2026-08-14: `await import()` of the cdnjs UMD build populates `globalThis.XLSX` on
the first attempt, and a workbook round-trips through `read` and `sheet_to_csv`.
Four fallbacks sat behind it — blob import, XHTML-namespaced `<script>`,
`new Function`, ESM from SheetJS's own CDN — and **none was reached, so none is
known to work.** Do not add one back as a safety net; an untested fallback is not a
safety net.

The probe is also why this took two rounds rather than one, and the reason is worth
keeping: **reachability is not executability.** The first probe used `fetch` on five
CDNs and all five returned 200, which says `connect-src` allows them and says
nothing about `script-src`. cdnjs was the only host with any evidence for
*executing* code, and that evidence was the pdf.js recipe already doing it in
production. Anyone extending this to a new library should test the import, not the
fetch.

cdnjs pins 0.18.5, which predates SheetJS's prototype-pollution and ReDoS fixes.
Accepted deliberately: parsing happens in the S3 scratch tab, which holds no
Procore session, and the output is data that is never executed. `cdn.sheetjs.com`
serves a current build and fetches fine, but executing from it is untested for
exactly the reason above.

**The output filter has a second trigger nobody knew about, and it silently
rewrites values.** `LIB.version` — the literal string `0.18.5` — came back as
`[BLOCKED: JWT token]`. Not secret, not a token; the dotted-numeric shape matched a
credential classifier. The existing note covers `[BLOCKED: Cookie/query string
data]` and reads as though that were the only filter on the path. It is not.

This matters because both skills return **figures**, and dotted identifiers are
everywhere in construction data — spec sections, phase codes, drawing revisions. So
the rule in both skills is now: **a `[BLOCKED: …]` string is never a value.** Re-return
the field in another shape and read it again; never let the marker reach a verdict,
a comment or the dashboard, and never read it as the field being empty. A redaction
that reads as an empty field is the same silent-misfile shape as everything else in
these notes.

**`computer` is the only visual read in the browser tool set.** Confirmed against
the live list 2026-08-14. `get_page_text` and `read_page` extract text, `find`
locates text, `read_console_messages` and `read_network_requests` read logs, and
`upload_image` / `file_upload` are inputs rather than reads. So a scanned invoice or
a photographed proposal is read by screenshotting with `computer`, and **no text
extractor will ever return anything for one** — reaching for them is precisely what
produced "support present but unreadable". Good news for the OCR cap: with a real
visual read available, OCR should be a rare fallback rather than the normal path.

**The sniff table was designed from a failure report rather than a reproduction —
and is now reported working.** Confirmed 2026-08-20 by the person running the
plugins: real workbooks are read and real images are looked at. That is a user
report rather than a transcript, so it is weaker evidence than the CCO gate's
record ids, but it is no longer a guess. `prose.md` carries the exact standing.

**Two branches under it are still unfired and are not covered by that
confirmation:** `scanned` → rasterise → look (a PDF that parses but yields almost
nothing, which is not the same as an image attachment Chrome renders directly),
and the OCR fallback along with the rule that an OCR-derived figure never earns a
`clear` verdict. Do not cite either as established.

**Reduce the nesting, never the rows.** Computing the six G702 identities in the
page and returning residuals is a *tightening* — fixed arithmetic is more
reliable in JS than read off 50 KB of nested JSON. But returning residuals
*alone* was proposed and rejected: a duplicated line, a zero-quantity line, a
description that does not match the scope all survive a residual of `0.00`. A
reducer only finds what it was written to look for, and this review exists to
catch what nobody specified. So the G703 still comes back, flattened.

**Two checks are never batched, and both now say so in place** — because they are
what an optimisation pass reaches for next. The **pre-click** re-verification's
entire value is running in the moment before that item's click. The **post-click**
verification catches more than connector lag: an unexpected record state, a
response that routed wrongly, a frozen tab. Sweeping once at the end means every
remaining click has already landed before any of that is visible. Both were
costed as small savings. Neither is worth the trade.

**Per-item marks live in `localStorage`** (`ns_marks_v1`, `pc_marks_v1`) alongside
the view state (`pc_view_v2`, `ns_view_v1`), and are the only user state that
survives a re-render. Never rename those keys for tidiness; it silently discards
decisions the user marked but has not executed. The two kinds are not equivalent —
losing a view costs a scroll, losing a mark discards work — so a new control gets a
**new** key rather than widening a marks key.

**Both dashboards now sort, filter and search, and the NetSuite one is the port.**
Asked by a teammate 2026-08-19: *"how come netsuite dashboard is not sorting while
procore one has filtering"*. It had **no view controls at all** — a hardcoded
`rows.sort()` by verdict and nothing else — so Procore's toolbar was ported across,
names and idiom identical so the two templates stay diffable. NetSuite has no
campus/building, so its axes are **Type** and **Vendor** (vendor narrowing to the
chosen type, the way Procore's buildings narrow to campus), plus sort, search and
Reset.

Two things about that port are load-bearing:

- **`renderBar()` reads `REVIEW.items`, never the filtered list.** A marked item that
  is currently filtered off screen still has to execute. Narrowing the execute bar to
  what is visible is the obvious-looking tidy-up and would silently drop decisions the
  user made before they filtered — the same misfile shape as everything else in these
  notes. Both a comment and a test cover it; do not remove either. **The test was
  missing until 2026-08-20** — this note asserted one existed for a day and it did
  not, which is worth remembering the next time these notes claim coverage.

**Verdict is no longer the default sort. Newest first is, on both dashboards.** Asked
for directly, 2026-08-20, overriding the note that used to sit here — which argued
flagged-first was what the page is *for* and that a reader who touches nothing must see
what they saw before. That reasoning was sound and was still outranked: the person
reading the queue every day wanted recency. Verdict survives as an option in NetSuite's
dropdown, so nothing is lost, only re-defaulted. Do not quietly restore it.

Four things about that change are load-bearing, three of them earned by something that
was actually broken:

- **A new default must ship with a new view key.** `pc_view_v2` → `pc_view_v3`,
  `ns_view_v1` → `ns_view_v2`. A stored view overrides the default on every load, so
  shipping a new default under the old key reaches nobody who has ever touched the
  toolbar — which is everyone it is for. Both templates migrate the old key rather than
  discarding it: filters and search carry across, only `sort` resets. The marks-key rule
  above is untouched and still absolute.
- **"Newest" means different things on the two dashboards, and Procore's is a proxy.**
  NetSuite sorts on `trandate`, a real document date, with the internal id descending as
  the same-day tiebreak. **Procore has no creation date anywhere in its pipeline** — its
  only per-item date is `due`, the workflow step's *deadline* — so "newest first" there
  is *latest-deadline-first*, chosen deliberately as the closest available proxy and
  labelled `Newest first — latest deadline` so nobody reads it as an origin date. If a
  real creation date is ever wanted there it has to be added to the Step 3 record reads,
  the log schema and `publish_dashboard.py` together; do not relabel without doing that.
- **`ageDays` clamped at `Math.max(0,…)` and that clamp was wrong in a comparator.**
  Every future-dated bill collapsed to `0` and tied with every other one. Invisible while
  verdict was the default; wrong at the top of a newest-first list, which is precisely
  where future-dated rows now land. There are two helpers now — `ageDaysRaw` for
  ordering, `ageDays` for display, because "-3 days pending" is nonsense to read. Procore
  has the mirror-image of this: `daysSince` is correctly unsigned-free, and the *display*
  was the broken half, rendering "-13 days ago" for a deadline still ahead. `dueText()`
  phrases it; the comparator still gets the sign. **Never clamp the ordering key, and
  never sign the display.**
- **`position:sticky` resolves against the element's parent box.** The execute bar was
  first made sticky on `.bar`, whose parent `#bar` is exactly as tall as it — zero travel,
  no error, and it looked done. Caught by measuring the bar's viewport position at two
  scroll offsets in a real browser, not by reading the CSS. It now sits on `#bar` inside a
  `.worksec` that also holds the rows, which is what gives it the queue to float over. A
  test pins this. The same measurement is the only honest way to check the next one.

**The execute bar is rendered in every state now, zero marks included**, and there is a
second Execute button mirrored in the page header once something is marked. The bar used
to collapse to one line of grey text below the queue until you had marked something — so
step 2 was invisible until you had already worked out step 1 unaided, which is backwards
for the one thing the page has to teach. The two steps are also numbered in the markup.
**The header mirror is the half that is guaranteed to work**: whether the widget iframe
scrolls internally is not knowable from the agent side, and if it does not, sticky
silently degrades to an ordinary block. That is why both exist; do not delete one as
redundant.

**Procore's sticky bar carries only what you need in the second before clicking.** The
stale-snapshot warning and the Stale-safe explainer moved below it into `#barnote`,
because inside the bar they made it 249px — over a third of a 700px viewport. Both
dashboards' bars now measure 153px. Anything added to `.bar` is paid for in queue you
cannot see, so put reference text in `#barnote`.

**The teammate-facing onboarding sheet lives at `docs/onboarding.html`.** It is
served to teammates by **GitHub Pages** from `docs/` on `main`:

```
https://ssemwal-cdc.github.io/claude-sharables/
```

**The page is the file.** Edit, push, done — there is no publish step and no
second copy to drift. It replaced a published claude.ai artifact precisely
because that arrangement had two silent failure modes: editing the file changed
nothing teammates saw, and republishing without passing the existing URL minted a
*second* artifact while everyone kept reading the first.

Three consequences worth keeping in mind:

- **`docs/` is the website.** Anything added there is publicly served. Nothing
  sensitive goes in that folder, and the same rule as the rest of this repo
  applies with less margin for error.
- **`docs/onboarding.html` must stay a complete HTML document** — doctype,
  `<head>`, `<meta charset="utf-8">`. Pages serves the file verbatim. It was
  originally written as an artifact *fragment*, because the artifact host wraps
  content in its own skeleton at publish time; served raw without that wrapper,
  every em dash, arrow and middot in it becomes mojibake.
- **It now carries one small script, and that is the only one.** Copy buttons on the
  four code blocks, added 2026-08-19 — the schedule prompts are ~40 lines and selecting
  one by hand is exactly the friction the "one paste" restructure was meant to remove.
  The wrapper and the button are **built by the script at run time**, never written into
  the markup, so a reader with JS off sees a clean `<pre>` and not a dead button. It
  copies `pre.innerText`, deliberately: the schedule blocks carry `&lt;n&gt;` escapes and
  `innerText` hands over the `<n>` the chat should actually receive, where `textContent`
  would too but the source must stay escaped either way.
- **That also means it can no longer be published as an artifact as-is.** Handing
  the file to `show_widget` or an artifact publish would nest a second `<html>`.
  Strip the wrapper first, or just send the Pages link — which is the point of
  the move.

`docs/index.html` is a redirect to `onboarding.html` so the bare URL works;
Pages has no directory index and would otherwise 404 on the short link.

**Editing the sheet works normally; fetching the published page does not.** The
sandbox's egress proxy blocks `github.io` (along with `claude.com`,
`support.claude.com` and `chromewebstore.google.com`), so `WebFetch` on the live
URL returns `EGRESS_BLOCKED`. Do not read that as the site being broken, and do
not conclude from a green Pages deploy that the page renders — the deploy proves
GitHub built the file, nothing more.

What *is* checkable locally, and worth checking after any edit: the file decodes
as UTF-8, the markup has no unclosed tags, `<meta charset>` is present, `body`
sets its own `background` from a token, and every `var(--…)` used is defined on
bare `:root` — that last one is what stops the page rendering one theme's text on
the other theme's ground for anyone on the default "system" setting. Anything
genuinely visual has to be eyeballed by the user; ask rather than assume. Written
for someone who has never touched any of this, so it is deliberately
click-by-click: profile (bottom left) → Settings → Plugins → Add → Add
marketplace, auto sync left checked, then first run in a **Cowork** chat on Opus
5 / High effort. Every step ends in a "done when" check, which is the device that
makes it followable — keep that if you edit it.

**The page carries no `[data-theme]` blocks, deliberately.** It had both halves of
the artifact host's three-state pattern — a `:root[data-theme="dark"]` block and a
`:root:not([data-theme="light"])` guard on the dark media query — and on Pages both
are dead, because nothing sets the attribute and there is no toggle to set it.
Removed 2026-08-17, leaving a plain `prefers-color-scheme` query and a comment in
the file saying why. The rule above mandating all three states is correct *for
artifacts*; this file stopped being one when it moved to Pages. Do not restore them
from that rule.

Facts it carries that are not obvious from the skills:

- **The NetSuite connector needs a separate, Claude-enabled NetSuite account**, a
  second one issued on top of the user's usual login. A normal NetSuite login is
  *not* connector access, and people who only have one account assume it is. If
  the connector is not listed, they were never provisioned — email invite from
  Compass, otherwise IT. Approvals must still come from their *normal* account,
  since that is whose name lands on them.
- - **An expired connector session is a third state, and it must not be silent.**
  The say-nothing rule covers the never-provisioned case only, where a caveat is an
  apology on a loop for something the reader cannot fix. A stale session is seconds
  to fix and restores the cross-check, so the run says it once near the headline and
  never again. Collapsing the two is the tempting simplification; do not.
- **A failed connector call is never an empty result.** Step 1a is what finds bills
  pending approval, so an auth failure read as "no rows" reports an **empty approval
  queue** and the user closes the tab believing nothing is waiting. An error, an auth
  challenge, or any non-result-set response means switch that run to the browser
  route — same three-state rule as the Procore gate, reached from a different
  direction, and the highest-consequence instance of it in either skill.
**The connector is optional, and the sheet says so at step 2.** It was written
  as a required step, which told unprovisioned teammates to wait on IT when they
  could have started that day. What it adds is stated positively — faster queries
  and the PO/billing-history cross-check — rather than the browser route being
  described as lacking something. That framing is deliberate and matches the
  skill's own rule: state what was checked, never what was not.
- **The connector lapses every few days, and the sheet now says so up front.** Added
  2026-08-19 from teammate feedback. Two things about it are deliberate. The cadence is
  **reported, not measured** — nobody here has timed the TTL, so the sheet says *"every
  few days"* and never a number. And it is framed as *how the connector behaves
  generally*, not as something these plugins cause, because the person hitting it will
  otherwise file it as a plugin bug. It pairs with the third-state rule above: the run
  says it once, then carries on through the browser, so what lapses is the cross-check,
  not the review.
- **The workspace folder is declared, not chosen: Downloads.** The sheet used to say
  *"point it at any folder"*, which was two defects in one line — *point it at* is
  jargon for the Cowork folder picker, and *any folder* pushes a decision onto the
  reader for no benefit. **A declared folder is load-bearing**, not tidiness: the
  idempotency gate reads `<folder>/_netsuite_review_log.json`, so a reader who picks
  somewhere different on the second run is a brand-new user to the gate and gets asked
  the setup questions again. Downloads is safe because neither skill writes attachments
  there — both read PDFs and workbooks in-page.
- **The sheet now tells the reader to set permissions to Auto, and not to use skip-all.**
  Added 2026-08-20 on request, and it is the one permissions instruction the sheet carries.
  Note what it is *not*: the deleted onboarding section warned against above was
  troubleshooting for a scheduled-run hang that never existed. This is a setup instruction
  resting on two settled facts — every operation either plugin performs has run clean in
  auto, and skip-all is ruled out on Anthropic's own grounds for a browser holding live
  approval authority. The sheet gives that reason rather than just the prohibition, because
  a rule with no reason is the one people talk themselves out of.
- **Restart the computer, not the app.** Observed on Windows: an app restart is
  not reliably enough for a plugin install or update to show up. Updates land on
  the next reboot, which for most people is the following morning, so auto sync
  plus a normal work rhythm needs no commands at all.
- **Nothing runs with the machine off or Chrome closed.** Both plugins drive the
  real browser session, and a missed scheduled window does not queue up — hence
  more than one fire time, with the idempotency gate stopping the later ones once
  a day has succeeded.
- **`/plugin` and `claude plugin` are different things.** The first is typed in a
  chat, the second in a terminal. A sheet that says "terminal" and then shows
  `/plugin` is wrong, and `README.md` used to make exactly that mistake.
- **The sheet carries no terminal commands at all now — the terminal/app split above
  was resolved twice, and deleting won.** 2026-08-24. The split had just been
  documented and the sheet taught it: the terminal blocks were kept and *labelled*
  ("only for terminal installs", "separate copies"), with confusion-table rows for
  the terminal-side errors. Labelling is the more informative fix and it is not the
  one asked for. **The sheet's reader has no terminal install** — it walks them
  through the app, start to finish — so every terminal block was reference material
  for a thing they do not have, sitting in the middle of instructions they do.
  Deleted: step 3's "doing it in the terminal instead", the terminal update section,
  and **three confusion-table rows**. The rows are the part worth noticing — the
  missing-`@compass-claude-plugins` error, marketplace-updated-but-nothing-changed,
  and `claude plugin list` coming back empty are all errors *only a terminal command
  produces*, so with the commands gone they document failures the reader cannot
  reach, which is worse than saying nothing. The table is "Three things" now.
  **Nothing verified was lost**: the screenshot-verified in-app force-update path
  and "Which version am I on?" are what *Keeping it updated* is made of, and the
  app-side **Last updated** row stayed. **The maintainer-facing CLI guidance in this
  file and in `README.md` stays** — the maintainer does work in a terminal. Do not
  "restore consistency" by putting the commands back in `docs/onboarding.html`; if a
  teammate ever does end up with a terminal install, the commands are two sections
  up in this file, which is where the person helping them will be looking anyway.
- **The whole sheet is second-screenable, and saying so is worth more than the time
  figures were.** 2026-08-24, in two passes. "15-20 minutes" read as twenty minutes of
  sitting and watching — a much bigger ask than the thing is, and the sort of number
  that defers the step to a day that never comes. The first pass fixed only step 4's
  opener, which was the wrong scope: the claim is true of the *whole* document, and
  someone deciding whether to start today has not reached step 4 yet.
  **Three things about the fix are load-bearing.**
  - **The header carries no chips at all now** (2026-08-24, after two rounds of them).
    They went from `~25 min to set up` / `then a 15-20 min first run` — which invited
    adding the halves and reading the total as booked time — to a three-chip row, and
    then out entirely. Nothing was lost with them: `~45 min` and `mostly waiting` were
    already the paragraph's own words, and the break chip became *"take a break after
    step 3"* in the lead sentence, which names a step a reader can act on where
    `halfway` did not. **Both facts now live in that one sentence and nowhere else**, so
    they get an assertion each rather than one a half-edit could satisfy; the placement
    guard was re-anchored to the element (the `<p>` after `#before`) rather than to a
    phrase, since the phrase is the part that keeps getting rewritten. **The `.chip` class stays** — the step 1 and step 2 headings use it — so
    the test asserts `header .chip` is empty rather than the class being unused. The
    `.meta` rule went with the row, since that row was its only user.
  - **"On a second screen" was cut as a phrase while the meaning was kept.** In a sheet
    whose second section is a prerequisites list, it reads as a *hardware requirement*
    — "do I need two monitors?" — which is the exact opposite of the reassurance
    intended. What replaced it names the mechanism instead: most of the elapsed time is
    a download, an install, a restart, and a run that pauses and waits for you. That is
    a claim about the work, and it is checkable.
  - **It sits above the prerequisites list, not in it.** That list is things you must
    have; this is not one of them, and a fourth bullet would file it as one. It is also
    deliberately *not* inside a `<details>` — a reassurance nobody opens is not a
    reassurance. A test pins both, mutation-checked by folding the line away.

  **The first wording of it over-corrected, and that was caught the same day.** *"None
  of this needs your full attention"* invites starting it and leaving, and the run
  cannot survive that — it stops to ask permission and waits for an answer. The line
  now leads with **the two facts a reader decides from — how long, and where they can
  stop** — and the posture follows as explanation rather than as the headline:

  > **About 45 minutes, with a good place to stop after step 3.** Stay around for the
  > whole thing — it pauses to ask permission and won't go on without you. But most of
  > that time is a download, an install and a restart, so a glance every few minutes is
  > enough.

  Three sentences, one job each: how long, you have to be here, but lightly. *"Won't go
  on without you"* replaced *"can't run unattended"* deliberately — it states the
  consequence rather than issuing a rule, and the consequence is what makes someone
  stay. Both directions are load-bearing and dropping either produces a wrong sheet, so
  a test asserts the presence claim survives, mutation-checked by deleting it.

  **It then had to be cut in half, because the paragraph outgrew the list it
  introduces** — 76 words against 48 for all three prerequisites. Two of its four
  sentences were third copies: the halfway break is already a chip *and* a marker at
  step 3, and "mostly waiting" is already a chip. What a paragraph like this owes the
  reader is the part no chip can carry — *why* you can't walk off — so the enumeration
  went, the break sentence went, and the constraint stayed. 41 words. The general rule
  worth keeping: when a fact earns a chip or a marker, delete it from the prose rather
  than leaving the prose as the authority.

  **The break is marked at the end of step 3, and where it sits is the whole point.**
  It existed before as a clause *inside* step 4 — so the only reader who could find it
  had already started the step it lets them defer. It is now a `.note` after step 3's
  *Done when*, and a third chip (`break point halfway`) puts it on the decide-from
  surface, because "do I need a free 45 minutes" is the biggest single objection to
  starting today. Reuses the existing `.note` class rather than adding one: this sheet
  had just been through a brevity pass and a bespoke class for one element is exactly
  the accretion that pass was removing. A test pins that the marker is between step 3
  and step 4 and outside any `<details>`.

  Step 4 keeps a warning of its own but no longer repeats either point: the timeout is
  the one fact true of that step and not of the others.

**The marketplace name is not the repo name.**
Repo is `ssemwal-cdc/claude-sharables`; marketplace is `compass-claude-plugins`
(from `name` in `marketplace.json`). So `add` takes the repo and `install`
takes the marketplace:

```
/plugin marketplace add ssemwal-cdc/claude-sharables
/plugin install <plugin-name>@compass-claude-plugins
```

This looks like a typo and is not. Do not "fix" it.

**The NetSuite connector lags the UI by minutes after an approval, and the
obvious success check reads that lag as failure.** Found in production, 2026-08-12.

Step 8 used to verify an approval by re-querying the pending queue and checking
the item no longer returned. Two things break that:

- `approvalstatus` stays `1` after a successful approval, because the record is
  now pending the *next* approver. Observed: two bills approved and routed
  onward, both still reading `approvalstatus = 1`.
- The connector takes minutes to catch up, so even a correct query returns stale
  rows straight after the click.

Together they produce a false failure on work that succeeded — which stops the
batch, logs a failure that did not happen, and invites a re-run that would
approve twice. Verify the **record**, not the queue:

```sql
SELECT id, approvalstatus,
       custbody_sna_cdc_next_approver     AS next_appr,
       custbody_sna_cdc_previous_approver AS prev_appr,
       custbody_sna_cdc_app_count         AS app_count
FROM transaction WHERE id = <id>
```

Advanced means `prev_appr` is now the user, `next_appr` is someone else, and
`app_count` went up by one. Unchanged means *not yet*, never *failed* — wait and
re-check, and never re-click on it.

The same lag is why an outcome must never be written to `actions` before it is
observed. A pre-written entry is a fabrication and later reads exactly like a
real one.

**The two skills used to share a state filename, and it cost real
cross-contamination.** Both called it `_review_log.json`, differing only by
parent folder, with both folders under the same workspace parent. An agent
running both in one session resolved the bare name against the wrong folder and
wrote NetSuite records into the Procore log. They are now
`_netsuite_review_log.json` and `_procore_review_log.json`, each publish script
migrates the old name in place, and each skill carries an Absolute rule that it
owns exactly one file and quarantines foreign records rather than merging them.
Never give two skills the same state filename, however different their folders.

**Updating an installed plugin takes two commands, and the first one looks like
it was enough.** Verified 2026-08-11. `marketplace update` refreshes the
*catalog*. It does not touch an installed plugin, but it reports success as
though it did:

```
> claude plugin marketplace update compass-claude-plugins
√ Successfully updated marketplace: compass-claude-plugins
```

The installed version does not move. The plugin needs a second command, and that
one **requires the `@marketplace` qualifier** — the bare name fails with an error
pointing at the wrong problem entirely:

```
> claude plugin update netsuite-approval-review
× Failed to update plugin "netsuite-approval-review": Plugin "netsuite-approval-review" not found
```

It is installed. `claude plugin list` shows it on the next line. This is the same
repo-vs-marketplace split as above, surfacing in a command the verification
snippet never exercises — that snippet installs and uninstalls, it never updates.

The sequence that works, from any directory. Plugins install at `user` scope, so
there is nothing to `cd` into:

```bash
claude plugin marketplace update compass-claude-plugins
claude plugin update netsuite-approval-review@compass-claude-plugins
claude plugin update procore-open-items-review@compass-claude-plugins
# then restart the app - the CLI says "Restart to apply changes"
```

Then confirm it landed. The version is the commit SHA, so it should match the tip
of `main`:

```
netsuite-approval-review   9ea01d3a5df2 -> 5c242055c130
```

**Prefer this over the `/plugin` flow.** It is scriptable, it prints the before
and after versions so you can see whether anything actually shipped, and it
surfaces the qualifier error rather than failing quietly.

**Those commands update terminal installs only — the app has its own store and
its own update path.** Verified with screenshots, 2026-08-21. App-installed
plugins live in the app's account-synced store, not `~/.claude/plugins` (the
split under [Versioning](#versioning)), and the app's force-update is: profile
(bottom left) → **Settings → Plugins** → **Browse** → **Personal** tab → the
`claude-sharables` chip beside "Local uploads" → **⋯** → **Check for updates**.
That menu also carries the **Sync automatically** toggle and shows **Synced
commit** — the installed release, directly comparable to `main`'s tip. Two
display traps nearby, both observed: the app labels the marketplace by **repo**
name (`claude-sharables`), not marketplace name — the repo-vs-marketplace split
again, surfacing in reverse — and the Settings → Plugins list's **Last
updated** column tracks the last commit to `marketplace.json` (2026-08-12 for a
long stretch), not plugin content, so an old date there is not staleness.
Removing the marketplace from that ⋯ menu uninstalls its plugins and a re-add
lands on current — the reliable last resort when Check for updates doesn't move
the synced commit.

**A stale install presents as a bug in the repo, and it is worth recognising on
sight.** Reported 2026-08-14: `publish_dashboard.py` was hardcoding
`cco -> ChangeOrderPackage`, the type that 400s — except the repo had shipped
`CommitmentChangeOrder` the day before. Both observations were correct. Procore's
Step 0 copies the plugin's assets over the workspace copies on *every* run, so
the workspace always mirrors **the installed plugin**, never the repo. An install
that predates the fix therefore keeps restoring the old file, and the natural
reading — "the workspace copy is stale, fix it upstream" — points at a file that
is already right.

**Correction, 2026-08-15, from a live Cowork run: the sandbox shell there cannot
see the plugin directory at all** — only the connected workspace folder, outputs
and uploads are mounted — so on that surface Step 0's `cp` never runs and the
workspace mirrors **the last successful sync**, which can lag the installed
plugin. "Always mirrors the installed plugin" above holds only where the shell can
reach `${CLAUDE_PLUGIN_ROOT}`. It also reopens the 2026-08-14 diagnosis: a
workspace stale because the old install kept restoring it and one stale because
nothing could restore anything produce the same symptom, and only the first is
fixed by updating the plugin. Step 0 in both skills now carries a sync ladder —
`cp`, then Read → Write through the file tools, then use-what-is-there and say so
once — so the failure is visible instead of silent.

**Deleting the workspace folder is not a fourth fix, and it makes things worse.** The
copies are stale because the *write failed*, so deleting the destination does not make
`${CLAUDE_PLUGIN_ROOT}` reachable — the next run fails the same way, except rung 3 now has
nothing to fall back on. Delete-then-write converts a fail-open into a fail-closed. It also
destroys the state file in that folder: `config` (publish then aborts rather than guessing
an identity), the review history, and `lastCompletedRun`. The narrow version — deleting only
the two asset files and keeping the log — still only helps on a surface where the sync can
actually run. **The template carries a version marker and `publish_dashboard.py` warns on a
mismatch — but that pair only catches a *torn* sync, not a stale one.** The template and the
script are copied together, so a workspace three versions old has both files agreeing and
publishes silently; verified 2026-08-24. The check that actually catches staleness is in Step 0 of
each `SKILL.md`, which states the expected `layout template vN` and reads the workspace copy back,
because `SKILL.md` always ships with the plugin and is the only fixed point left when the plugin
directory cannot be reached. Bump the marker whenever the template changes;
`scripts/test_skill_code.py` fails if script and template disagree, and `validate.py` fails if
either disagrees with the version `SKILL.md` states.

**The stale-copy family is therefore three states, with three different fixes.**
A stale **install** needs the two-command update and a restart. A stale
**workspace** needs the sync to actually run (a rung of the Step 0 ladder). A
stale **dashboard** needs a re-render — an old chat replays its old instructions
forever regardless of the other two. The symptoms overlap almost completely, so
diagnose in order: install version against `main`; then the workspace copy's
`layout template vN` against the version Step 0 states, which is a **direct** check
rather than an inference from modification dates; then the render date on the widget.

**A rendered dashboard is a snapshot of the template, so an old chat replays old
instructions — and that reads as a stale install.** Cost a wrong diagnosis
2026-08-15. A resolve-the-gate button was quoted saying *"try the alternative type
strings"*, wording removed in `7100c5d`, so the install was called out as
predating that commit. It was not: the install was `5767839`, which contains
`7100c5d`. The button was in a dashboard **rendered before that update** and still
sitting in an older conversation.

Both are stale-copy problems, and the fix differs. A stale install needs the
two-command update. A stale *dashboard* just needs a re-render — running the
review again is enough, and updating changes nothing about the old widget, which
will keep offering its old instruction forever. **Check the version before
concluding either**, and note that clicking a button in an old chat is not
evidence about the installed plugin at all.

So when a fix that is provably in `main` does not appear in a run, check the
installed version against the tip of `main` before editing anything. The tell is
that `SKILL.md` describes behaviour the assets do not have: prose and assets ship
in the same commit, so they cannot disagree in the repo, only across an install
boundary. The fix is the two-command update above, then a restart.

**A full git URL needs the `.git` suffix.**
`https://github.com/ssemwal-cdc/claude-sharables.git` works. Without `.git`,
Claude Code treats the URL as a direct link to a hosted `marketplace.json`
instead of a repo to clone. The `owner/repo` shorthand also works and is what
the README tells teammates to use.

---

## Versioning

No `version` field anywhere — not in `plugin.json`, not in marketplace entries.
Version then resolves from the git commit SHA, so **every push to `main` is
automatically a new version**.

If a `version` string is ever added and someone forgets to bump it, everyone
silently keeps their cached copy and the fix never ships. `scripts/validate.py`
rejects a `version` field in either file for that reason.

Confirm it is working — installed version should be a commit SHA prefix:

```bash
claude plugin list        # Version: 7ca6a2ea2c70
```

**`claude plugin list` only sees CLI installs.** Confirmed 2026-08-21 on a
machine with the plugins installed and working through the desktop app: the
terminal list came back empty. The CLI and the desktop app keep separate plugin
inventories — the CLI's lives in `~/.claude/plugins/installed_plugins.json`,
the app's in its own store — and the terminal update commands above only ever
touch the CLI copy. So a terminal update does nothing for plugins that were
installed through the app, and an empty `claude plugin list` does not mean the
app has no plugins. Update app installs through the app.

### Skill version lines

The no-`version` rule above bans the *machine* fields — the ones install
resolution reads. Separately, every skill carries a *human* version marker, and
that one is **required**: the first line under the title in each `SKILL.md`
reads

```
**Skill version N — YYYY-MM-DD.** …
```

mirrored as `vN` in the README's Available plugins table. It exists because an
installed skill is a snapshot and the desktop app shows no commit SHA anywhere;
opening the skill shows `SKILL.md`, so the file itself is the only place a
version can be read on that surface. An installed copy with no version line at
all predates 2026-08-21. Because the line is in the prompt, the running skill
can also answer "what version are you on?" in chat.

**The Settings → Plugins screen never shows the SKILL.md body** — settled by
screenshot, 2026-08-21: the plugin detail page renders `plugin.json`'s
description in full and the skill's frontmatter description truncated to one
line, and nothing else from the skill. So the version lives in **four synced
sites**, each for the surface that shows it: the START of the skill's
frontmatter description (`vN — …`, visible in the truncated Skills row and the
in-chat skills list), the END of the `plugin.json` description
(`Skill version N — date.`, the plugin detail page — prose, deliberately not
the banned `version` field), the SKILL.md body line (the in-chat skill panel,
and how the running skill answers in chat), and the README table (`vN`, the
current-version side, on GitHub). The marketplace.json descriptions carry no
version on purpose: a stale catalog could show a number that matches neither
the installed copy nor `main`.

Bump the number, the date, the two descriptions, and the README cell **in the
same commit as any change under that skill**. `scripts/validate.py` enforces
that every site exists and all of them agree — it cannot enforce the bump
itself, so that part is habit. A new skill starts at version 1.

The line's wording matters, and the first live run set it. Asked "what version
are you on?", the installed skill reported its line correctly — then went
looking for the README table *locally*, found nothing (a git-subdir install
ships only the plugin folder, never the repo root), reported the staleness
check as unrunnable, and suggested adding a `version` field to `plugin.json` —
the exact field the rule above bans. The line now names GitHub as the only
comparison point and rules that field out in place, and each plugin README
carries the same note under **Versioning**. Keep both when editing; an
installed copy has no repo around it, so anything the line asks a reader to do
must work from the plugin folder alone.

---

## House conventions

Both existing plugins follow one shape. Match it when porting, and if a new
skill deviates, say so explicitly rather than quietly normalising it.

- **A plugin is a prerequisite bucket, not one skill.** Both plugins happen to
  hold one skill today; that is an accident of having ported two skills with
  two different prerequisites, not a rule. Multi-skill plugins are the
  documented standard layout and the ecosystem norm. Use
  [the prerequisite test](#the-prerequisite-test) — never "one skill per
  plugin".
- **Frontmatter** is `name` + `description` only. `description` carries the
  trigger phrases — it is what decides whether the skill fires, so it is long
  and specific on purpose. Do not trim it for tidiness.
- **Dashboard-publishing pattern**: `assets/dashboard_template.html` +
  `assets/publish_dashboard.py`, copied into a workspace state folder on first
  run, output published to an artifact rather than to chat.
- **First-run setup** is per-plugin, asks the user to confirm identifiers that
  differ per person or per company, and stores them in a state file.
- **Neither plugin acts on its own judgement.** Both only approve/respond on an
  explicit per-item instruction. Preserve that in anything ported in.

---

## Repo facts

- Remote: `https://github.com/ssemwal-cdc/claude-sharables` — default branch `main`
- Marketplace name: `compass-claude-plugins`
- Plugins currently registered:
  - `netsuite-approval-review` — skill `netsuite-approval-double-check`;
    needs Claude in Chrome signed in to NetSuite; the NetSuite MCP connector is
    optional and adds bulk queries plus the PO and billing-history cross-check
  - `procore-open-items-review` — skill `procore-open-items-review`;
    needs Claude in Chrome signed in to Procore, and has no connector
- **Visibility: public, and that is a decision — not an oversight.** Shivam
  distributes by handing teammates the install commands and asking them to
  enable auto-update. Public is the only setting where that route needs no
  GitHub account per teammate and has no silent update failure. Org-wide admin
  sync was considered and explicitly rejected. Do not propose going private, and
  do not "fix" prose that says public. The reasoning is in README.md under
  *Distribution: why this repo is public*.
- **Because it is public, nothing sensitive may land here.** No tokens, no
  company ids, no endpoints, no real documents in fixtures or examples. If a
  ported skill carries any of those, stop and raise it before committing.
- No CI beyond `.github/workflows/validate.yml`, which runs `scripts/validate.py`.

---

## Do not

- Do not add a `version` field anywhere.
- Do not use `metadata.pluginRoot`.
- Do not put `skills/`, `commands/`, `agents/`, or `hooks/` inside
  `.claude-plugin/` — only `plugin.json` lives there.
- Do not create a second marketplace. One person can register only one
  marketplace per name, so a second would replace this one rather than sit
  beside it. Everything goes in `plugins/`.
- Do not edit a ported skill's `SKILL.md` prose to match house style unless
  asked. Port it verbatim, then raise anything that looks wrong.
- Do not tell a user a skill can self-update by putting `/plugin marketplace
  update` in its `SKILL.md`. `SKILL.md` is a prompt, not a script; `/plugin` is
  a client command Claude cannot invoke; and the file carrying the instruction
  is itself the stale copy. Point them at marketplace auto-update instead.


---

## Skill invocation (verified, 2026-08-11)

- The **short** slash name resolves to the plugin's skill while it is
  unambiguous: `/netsuite-approval-double-check` runs the plugin copy. The
  namespaced form `/<plugin>:<skill>` always works. Both are fine.
- A skill's `assets/` travel with the plugin and are visible in the skill
  panel. `${CLAUDE_PLUGIN_ROOT}` resolves them at run time.

- **Cowork works.** Both plugins run in Cowork sessions, artifacts and assets
  included. Do not write that plugins are machine-level and cannot reach
  Cowork — that was asserted from a docs passage about personal skills in
  `~/.claude/skills/` and is wrong for installed plugins.

**Do not warn users about duplicate standalone copies.** An earlier version of
these notes claimed the short name meant a stale personal skill was shadowing
the plugin. That was wrong — checked against a live run, the short name loads
the plugin's own skill, description and assets included.
