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
`README.md` including its prerequisite.

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

**Do not let an agent refuse to render because the file looks big.** A 120 KB Procore dashboard was
handed over as a file instead, on the reasoning that it might truncate — which cost one-click
execute entirely to avoid a risk that had not happened. The truncation guard exists precisely to
catch that case after the fact. Render first, believe the guard, fall back only on an observed
failure.

**Per-item marks live in `localStorage`** (`ns_marks_v1`, `pc_marks_v1`,
`pc_view_v2`) and are the only user state that survives a re-render. Never
rename those keys for tidiness; it silently discards decisions the user marked
but has not executed.

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
    needs the NetSuite MCP connector
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
