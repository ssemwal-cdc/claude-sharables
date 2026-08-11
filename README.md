# Compass Claude plugins

Internal marketplace of Claude plugins for Compass Datacenters.

## For teammates: installing

Run these two commands in Cowork or Claude Code, once:

```
/plugin marketplace add ssemwal-cdc/claude-sharables
/plugin install netsuite-approval-review@compass-claude-plugins
```

The first argument is this repo; the `@compass-claude-plugins` suffix is the
marketplace name declared in `.claude-plugin/marketplace.json`, which is why
the two differ. If the install summary says `Run /reload-plugins to activate.`,
run that too.

After installing, say "run my approval check". First-time setup happens
automatically and asks you to confirm your own NetSuite identity.

## Available plugins

| Plugin | What it does |
|---|---|
| `netsuite-approval-review` | Reviews the bills and change orders in your NetSuite approval queue, publishes verdicts to a live dashboard, and lets you approve or reject from it |

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

Put it in `plugins/<name>/` and add an entry to the `plugins` array in
`.claude-plugin/marketplace.json`. Keep everything in this one marketplace —
each person can only register one marketplace per name, so a second marketplace
would replace this one rather than sit alongside it.

## Repo visibility

This should be private or internal. Note that a private HTTPS remote can't
authenticate during the background auto-refresh; it falls back to re-cloning,
which still works. An SSH remote avoids the fallback.

If Compass is on a Team or Enterprise plan, an admin can sync this marketplace
to everyone from `claude.ai/admin-settings/plugins` so there is nothing for
teammates to run at all. That route requires the repo to be private or internal
and the plugin folders to live inside this repo, which is how it is laid out.
