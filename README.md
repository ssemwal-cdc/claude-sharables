# Compass Claude plugins

Internal marketplace of Claude plugins for Compass Datacenters.

## For teammates: installing

Register the marketplace once, in the Claude desktop app or the Claude Code
CLI (see [Cowork](#cowork-and-cloud-sessions) below — it works differently):

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
- **Either slash form works.** The short name resolves while it is
  unambiguous; the namespaced form always works:

  ```
  /netsuite-approval-double-check      /netsuite-approval-review:netsuite-approval-double-check
  /procore-open-items-review           /procore-open-items-review:procore-open-items-review
  ```

You rarely need either. Both skills fire from plain language — "run my approval
check", "run my Procore review" — which is what their trigger phrases are for.
If you installed mid-session, run `/reload-plugins` first.

Opening a skill from the panel shows its `assets/` alongside `SKILL.md`. The
supporting files travel with the plugin and resolve through
`${CLAUDE_PLUGIN_ROOT}` at run time — nothing extra to install or copy.

### Cowork and cloud sessions

Plugins installed in the desktop app are **machine-level and do not reach
Cowork**. Cowork sessions — interactive and scheduled — load the skills enabled
for your **claude.ai account**, synced at session start, not anything installed
on your machine. Plugins enabled only in your user settings do not transfer.

- **For Cowork**: enable the skill for your claude.ai account under
  **Customize**. (Mind the section above: enable it once, in one place.)
- **For cloud sessions on a repository**: declare the plugin in that repo's
  `.claude/settings.json` under `enabledPlugins`, and it installs at session
  start.

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

## Distribution: why this repo is public

**Distribution is by link.** Send a teammate the two commands at the top of
this README, ask them to enable auto-update, and they are done. There is no
admin step and no access to grant.

The repo is public **on purpose**, because that is the only setting under which
the link-and-auto-update route has no per-person setup and no silent failure
mode:

| Repo | Teammate needs a GitHub account? | Auto-update |
|---|---|---|
| **Public** — what we do | No, anonymous clone | Just works |
| Private over SSH | Yes, plus repo access | Works only if their key is in `ssh-agent` |
| Private over HTTPS | Yes, plus repo access | Degrades — see below |

Going private would cost a GitHub account and a repo grant per teammate, and
would make updates unreliable: the background refresh **disables git credential
helpers** for its `git pull`, so it cannot authenticate to a private HTTPS
remote. It falls back to re-cloning the whole marketplace, which can time out.
The result is a teammate who silently stops receiving updates — exactly the
failure the no-`version` rule exists to prevent. SSH remotes avoid it, but only
while every teammate keeps a key loaded in `ssh-agent`.

The tradeoff accepted in exchange: both plugins are **world-readable**. They
describe approval gates and cost-field mappings; they carry no credentials,
endpoints, or customer data. Keep it that way — never commit a token, a company
id, or a real document into this repo.

<details>
<summary>The one route that would beat public, and why it is not used</summary>

On a Team or Enterprise plan an admin can distribute a marketplace from
`claude.ai/admin-settings/plugins`. It reads the repo through the Claude GitHub
App and packages each plugin, so teammates need no GitHub account, no repo
access, and run nothing at all — not even the auto-update toggle.

It is unused here because it requires an admin to own distribution, and this
marketplace is deliberately self-serve. It also requires the repo be private or
internal, so adopting it later means flipping visibility. The `git-subdir`
sources this repo uses are supported by that route, so no rework would be
needed. Note that the repo is owned by a personal account rather than the
Compass organization, and whether org sync accepts a personally-owned private
repo is not documented — moving the repo into the org would be the first step,
not flipping visibility.

</details>
