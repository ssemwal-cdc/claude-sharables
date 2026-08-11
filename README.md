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

## Available plugins

| Plugin | What it does | Needs |
|---|---|---|
| `netsuite-approval-review` | Reviews the bills and change orders in your NetSuite approval queue, publishes verdicts to a live dashboard, and lets you approve or reject from it | NetSuite MCP connector |
| `procore-open-items-review` | Filters your Procore open items down to the ones actually awaiting your workflow response — change risks, subcontractor invoices, commitment change orders — verifies their figures against the attached support, and lets you respond from a dashboard | Claude in Chrome, signed in to Procore |

## For maintainers: releasing an update

Push to the default branch. That is the whole release process.

Teammates pick it up on the next background refresh, or immediately with:

```
/plugin marketplace update
```

**Do not add a `version` field to any plugin's `plugin.json`.** Version is
deliberately omitted so it resolves from the git commit SHA, which means every
push is automatically a new version. If you add a version string and forget to
bump it, everyone silently keeps their cached copy and your fix never lands.

## Adding another plugin

Both steps are required, and missing the first one fails silently at install
time rather than at push time:

1. Put the plugin in `plugins/<name>/`, with its own
   `plugins/<name>/.claude-plugin/plugin.json` declaring a `name` and
   `description` — and no `version`, per the rule above. Skills go in
   `plugins/<name>/skills/<skill-name>/SKILL.md`; the conventional `skills/`
   location is picked up automatically, so `plugin.json` needs no `skills` key.
2. Add an entry to the `plugins` array in `.claude-plugin/marketplace.json`.
   `source` is relative to `metadata.pluginRoot` (`./plugins`), so it is just
   the folder name. Keep `name` identical to the one in `plugin.json`.

Either existing plugin works as a template for the layout.

Keep everything in this one marketplace — each person can only register one
marketplace per name, so a second marketplace would replace this one rather
than sit alongside it.

## Repo visibility

This should be private or internal. Note that a private HTTPS remote can't
authenticate during the background auto-refresh; it falls back to re-cloning,
which still works. An SSH remote avoids the fallback.

If Compass is on a Team or Enterprise plan, an admin can sync this marketplace
to everyone from `claude.ai/admin-settings/plugins` so there is nothing for
teammates to run at all. That route requires the repo to be private or internal
and the plugin folders to live inside this repo, which is how it is laid out.
