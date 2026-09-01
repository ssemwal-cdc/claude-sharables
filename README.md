# Compass Claude plugins

Internal marketplace of Claude plugins for Compass Datacenters.

## For teammates: installing

**Start here: [`docs/onboarding.html`](docs/onboarding.html)** — the start-to-finish
setup sheet, written for someone who has never touched any of this. Browser,
connector, install, first run, and scheduling, with a "done when" check on every
step.

Send teammates this link:

```
https://ssemwal-cdc.github.io/claude-sharables/
```

That is GitHub Pages serving `docs/` from `main`, so **the page is the file** —
edit `docs/onboarding.html`, push, and the live page updates itself. There is
nothing to re-publish and no second copy to drift out of step.

Two things follow from that:

- **Everything in `docs/` is served publicly.** The folder is the website. Do not
  put anything there you would not hand to a stranger.
- **`docs/onboarding.html` is a complete HTML document** — doctype, `<head>`,
  `charset`. It has to be: Pages serves the file verbatim, and without the
  charset declaration every dash and arrow in it renders as mojibake.

The rest of this section is the short version for people who only need the
commands.

Register the marketplace once, in the Claude desktop app or the Claude Code
CLI (see [Cowork](#cowork) below — it works differently). In the desktop app:
**profile (bottom left) → Settings → Plugins → Add → Add marketplace**, enter
`ssemwal-cdc/claude-sharables`, and leave **auto sync** checked so updates
arrive on their own. Or from a chat:

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

### Cowork

**These plugins work in Cowork.** Install them once as above and run them from
a Cowork session the same way — verified against both plugins on
2026-08-11, including their inline dashboard widgets and their `assets/`.

If you are running a plugin in a **cloud session against a repository** rather
than in Cowork, that case is different: declare the plugin in that repo's
`.claude/settings.json` under `enabledPlugins` so it installs at session start.

## Available plugins

| Plugin | Version | What it does | Needs |
|---|---|---|---|
| `netsuite-approval-review` | v24 | Reviews the bills, purchase orders and change orders in your NetSuite approval queue, publishes verdicts to a live dashboard, and lets you approve or reject from it | Claude in Chrome, signed in to NetSuite. NetSuite MCP connector optional — adds bulk queries and the PO cross-check |
| `procore-open-items-review` | v26 | Filters your Procore open items down to the ones actually awaiting your workflow response — change risks, subcontractor invoices, commitment change orders, and the commitments themselves — verifies their figures against the attached support, and lets you respond from a dashboard | Claude in Chrome, signed in to Procore |

**Checking what you have installed:** the easiest read is **profile (bottom
left) → Settings → Plugins → click the plugin** — the last sentence of its
Description is the installed version ("Skill version N — date"). The same
number starts each skill's one-line description (`vN — …`), opens its
`SKILL.md`, and comes back if you just ask in a chat ("what skill version is
the NetSuite check on?"). Compare it to the Version column above: a lower
number — or no version anywhere — means your installed copy is stale; update
or reinstall the plugin.

## For maintainers: releasing an update

Push to the default branch. That is the whole release process — version resolves
from the commit SHA, so every push is a new version.

If the push changes anything under a skill, bump that skill's
`**Skill version N — date.**` line and the Version cell in the table above in
the same commit. `validate.py` enforces that the two agree; the bump itself is
the habit it cannot check for you.

Teammates get it automatically **only if auto sync is enabled on this
marketplace.** It is off by default: Claude Code enables auto-update for
Anthropic's own marketplaces, not for third-party ones like this. Turn it on
once, in `/plugin` → **Marketplaces** → `compass-claude-plugins` → **Enable
auto-update**. Claude Code then refreshes in the background shortly after each
session starts.

Without that, nothing arrives until someone runs the two-command update from a
terminal — the CLI form, not the `/plugin` one, because it prints the before and
after versions and surfaces the qualifier error instead of failing quietly:

```
claude plugin marketplace update compass-claude-plugins
claude plugin update netsuite-approval-review@compass-claude-plugins
claude plugin update procore-open-items-review@compass-claude-plugins
```

Then restart the computer. Observed on Windows: an app restart is not always
enough for a plugin change to show up.

Those terminal commands update **terminal installs only**. Plugins installed
through the desktop app live in a separate, account-synced store; the app's
own force-update is **Settings → Plugins → Browse → Personal →
`claude-sharables` → ⋯ → Check for updates**, and that menu's **Synced
commit** should match the tip of `main`. The onboarding sheet walks teammates
through it.

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

One check does **not** run in CI, because it needs a browser: the dashboards' floating
header is placed from JavaScript against the slice of the page the reader can actually
see, and where it lands is not visible to any static check. `scripts/measure_float.js`
publishes both dashboards from fixtures, serves them cross-origin into a scrolling host,
and measures the bar's real viewport position. Run it by hand after changing the dashboard
layout:

```bash
NODE_PATH=$(npm root -g) node scripts/measure_float.js   # needs playwright + chromium
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

The tradeoff accepted in exchange: both plugins are **world-readable** — not
enterprise-private, and forkable by anyone. They describe approval gates and
cost-field mappings, and their worked examples use placeholders rather than live
tenant ids, counterparty names or amounts. Keep it that way: never commit a token
or a credential, and keep every example a teammate copies free of real values.
Maintainer notes in `CLAUDE.md` and `prose.md` do cite record ids where those are
the evidence for a documented defect — see the rule under *Repo facts* in
`CLAUDE.md`, which spells out the distinction.

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
