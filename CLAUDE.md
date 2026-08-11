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
| A bare skill (a `SKILL.md`, maybe with `assets/`) | Decide: new plugin, or new skill inside an existing one. **Ask the user which** — do not guess. A skill only belongs in an existing plugin if it shares that plugin's data source and setup. |
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
  "source": "./plugins/<plugin-name>",
  "description": "..."
}
```

`source` is a path from the repo root and **must start with `./`**. See
[Traps](#traps-proven-not-guessed) — this is the one that has already broken
this repo once.

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

## Traps (proven, not guessed)

Verified against Claude Code v2.1.227 by reproducing each failure.

**`source` must start with `./`.**
A bare folder name (`"source": "netsuite-approval-review"`) passes a JSON
syntax check and fails at install with:

> This plugin's marketplace entry is invalid: source: Invalid input

**`metadata.pluginRoot` does not work. Do not use it.**
Anthropic's docs say `pluginRoot: "./plugins"` lets you shorten `source` to a
bare name. It does not. That combination fails as above; and `pluginRoot` plus
`"./name"` passes validation but resolves the source *from the repo root
anyway*, failing at install with:

> Source path does not exist: /…/<repo>/<name>

Spell every source out as `./plugins/<name>` and leave `pluginRoot` unset.
`scripts/validate.py` rejects the file if it reappears.

**Asset paths must use `${CLAUDE_PLUGIN_ROOT}`.**
Both skills reference assets as
`${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/assets/<file>`. A bare `assets/…`
path works in the repo and breaks once installed, because at run time the
working directory is the user's workspace, not the plugin. The validator
rejects bare paths.

**The marketplace name is not the repo name.**
Repo is `ssemwal-cdc/claude-sharables`; marketplace is `compass-claude-plugins`
(from `name` in `marketplace.json`). So `add` takes the repo and `install`
takes the marketplace:

```
/plugin marketplace add ssemwal-cdc/claude-sharables
/plugin install <plugin-name>@compass-claude-plugins
```

This looks like a typo and is not. Do not "fix" it.

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

- **One skill per plugin so far**, named the same as its plugin (except
  `netsuite-approval-review` → `netsuite-approval-double-check`). The `skills/`
  layout is used regardless, so a second skill can be added without moving
  anything.
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
- **Visibility: public.** The README's distribution notes discuss the private
  case because org-wide sync requires it; the repo is not private today. Do not
  write prose that asserts it is. Flag the mismatch if it becomes relevant.
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
