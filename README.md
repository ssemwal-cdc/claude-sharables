# Compass Claude plugins

Internal marketplace of Claude plugins for Compass Datacenters.

## For teammates: installing

Register the marketplace once in Cowork or Claude Code:

```
/plugin marketplace add ssemwal-cdc/claude-sharables
```

Then install whichever plugins you need:

```
/plugin install netsuite-approval-review@compass-claude-plugins
/plugin install procore-open-items-review@compass-claude-plugins
```

The argument to `marketplace add` is this repo; the `@compass-claude-plugins`
suffix is the marketplace name declared in `.claude-plugin/marketplace.json`,
which is why the two differ. If an install summary says
`Run /reload-plugins to activate.`, run that too.

After installing, say "run my approval check" for the NetSuite queue, or
"run my Procore review" for the Procore one. Each plugin runs its own
first-time setup automatically the first time you use it — NetSuite asks you
to confirm your NetSuite identity, Procore asks for your company id and a
couple of per-company tool and field ids.

### Where the skills show up

Two things surprise people here, and neither is a fault:

- **They are not in the Skills tab.** That tab lists personal skills from
  `~/.claude/skills/`. Plugin skills are a separate registry — find them under
  the **+** button next to the prompt box → **Plugins**, listed inside their
  plugin.
- **The slash commands are namespaced by plugin.** `/netsuite-approval-double-check`
  does not exist. The real names are:

  ```
  /netsuite-approval-review:netsuite-approval-double-check
  /procore-open-items-review:procore-open-items-review
  ```

You rarely need either. Both skills fire from plain language — "run my approval
check", "run my Procore review" — which is what their trigger phrases are for.
If you installed mid-session, run `/reload-plugins` first.

Note that plugins installed in the desktop app do **not** carry into Cowork or
other cloud sessions. To use them there, declare them in a repository's
`.claude/settings.json` under `enabledPlugins` so they install at session start.

## Available plugins

| Plugin | What it does | Needs |
|---|---|---|
| `netsuite-approval-review` | Reviews the bills and change orders in your NetSuite approval queue, publishes verdicts to a live dashboard, and lets you approve or reject from it | NetSuite MCP connector |
| `procore-open-items-review` | Filters your Procore open items down to the ones actually awaiting your workflow response — change risks, subcontractor invoices, commitment change orders — verifies their figures against the attached support, and lets you respond from a dashboard | Claude in Chrome, signed in to Procore |

## For maintainers: releasing an update

Push to the default branch. That is the whole release process — version resolves
from the commit SHA, so every push is a new version.

Teammates get it automatically **only if they have auto-update enabled on this
marketplace.** It is off by default: Claude Code enables auto-update for
Anthropic's own marketplaces, not for third-party ones like this. Turn it on
once, in `/plugin` → **Marketplaces** → `compass-claude-plugins` → **Enable
auto-update**. Claude Code then refreshes in the background shortly after each
session starts.

Without that, nothing arrives until someone runs:

```
/plugin marketplace update compass-claude-plugins
```

## Adding another plugin or skill

**See [CLAUDE.md](CLAUDE.md)** for the full layout, the required fields, the
verification commands, and the traps that have already broken this repo once.
It is the single source of truth so the two files cannot drift; Claude Code
loads it automatically when you open this repo as a project.

The short version: drop the plugin in `plugins/<name>/` with its own
`.claude-plugin/plugin.json`, register it in `.claude-plugin/marketplace.json`
with a `git-subdir` source pointing at `plugins/<name>`, then run
`python3 scripts/validate.py`.

## Checks

`scripts/validate.py` enforces everything the two documents above promise —
manifests resolve, names agree, no `version` fields, no unregistered plugins,
asset paths portable, and both docs still describing the plugins that actually
exist. It runs in CI on every push and pull request.

```bash
python3 scripts/validate.py
```

## Distribution and access

This repo is currently **public**, so anyone can add the marketplace and both
plugins are world-readable.

If you make it private, access is governed entirely by GitHub permissions —
there is nothing Claude-specific to grant. `/plugin marketplace add` and
`/plugin install` use each person's own git credentials, so a teammate can
install exactly when they could `git clone` the repo themselves. GitHub
`owner/repo` shorthand clones over SSH by default.

Two things to know before going private:

- **Background auto-update is the weak spot over HTTPS.** The background pull
  disables git credential helpers, so it cannot authenticate to a private HTTPS
  remote; it falls back to a full re-clone, which does use stored credentials
  but can time out. SSH remotes are unaffected. Setting
  `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` keeps the working clone
  when a background pull fails.
- **Org sync removes the problem entirely, and requires private.** On a Team or
  Enterprise plan an admin can distribute this marketplace from
  `claude.ai/admin-settings/plugins`; it reads the repo through the Claude
  GitHub App and packages each plugin, so teammates need no repo access and run
  nothing at all. That route requires the repo to be private or internal and
  the plugin folders to live inside it, which is how this is laid out.
