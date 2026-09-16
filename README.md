# Compass Claude plugins

Internal marketplace of Claude plugins for Compass Datacenters.

## For teammates: installing

Start with [`docs/onboarding.html`](docs/onboarding.html). It is the
start-to-finish setup sheet. It covers the browser, the connector, the install,
the first run and scheduling. Every step ends in a "done when" check. It is
written for someone who has never touched any of this.

Send teammates this link:

```
https://ssemwal-cdc.github.io/claude-sharables/
```

GitHub Pages serves `docs/` from `main`. The page is the file. Edit
`docs/onboarding.html` and push. The live page updates itself. There is no
publish step and no second copy to drift.

Two things follow:

- Everything in `docs/` is served publicly. The folder is the website. Put
  nothing there you would not hand to a stranger.
- `docs/onboarding.html` must stay a complete HTML document. It needs a
  doctype, a `<head>` and a `charset` declaration. Pages serves the file
  verbatim. Without the charset declaration every dash and arrow renders as
  mojibake.

The rest of this section is the short version for people who only need the
commands.

Register the marketplace once. Use the Claude desktop app or the Claude Code
CLI. In the desktop app, open profile at the bottom left. Go to
**Settings → Plugins → Add → Add marketplace**. Enter
`ssemwal-cdc/claude-sharables`. Tick auto sync in the Add dialog. Updates
arrive only while it is on.

From a chat, run this instead:

```
/plugin marketplace add ssemwal-cdc/claude-sharables
```

Then install the plugins you need:

```
/plugin install netsuite-approval-review@compass-claude-plugins
/plugin install procore-open-items-review@compass-claude-plugins
```

`marketplace add` takes this repo. The `@compass-claude-plugins` suffix is the
marketplace name declared in `.claude-plugin/marketplace.json`. That is why the
two differ. If an install summary says `Run /reload-plugins to activate.`, run
that too.

After installing, say "run my approval check" for the NetSuite queue. Say
"run my Procore review" for the Procore one. Each plugin runs its own
first-time setup on first use. NetSuite asks you to confirm your NetSuite
identity. Procore asks for your company id, plus per-company tool and field
ids.

### Where the skills show up

Two things surprise people here. Neither is a fault.

- The skills are not in the Skills tab. That tab lists personal skills from
  `~/.claude/skills/`. Plugin skills sit in a separate registry. Find them
  under the **+** button next to the prompt box, then **Plugins**, listed
  inside their plugin.
- Either slash form works. The short name resolves while it is unambiguous.
  The namespaced form always works.

  ```
  /netsuite-approval-double-check      /netsuite-approval-review:netsuite-approval-double-check
  /procore-open-items-review           /procore-open-items-review:procore-open-items-review
  ```

You rarely need either form. Both skills fire from plain language. Say
"run my approval check" or "run my Procore review". If you installed
mid-session, run `/reload-plugins` first.

Opening a skill from the panel shows its `assets/` beside `SKILL.md`. The
supporting files travel with the plugin. They resolve through
`${CLAUDE_PLUGIN_ROOT}` at run time. Nothing extra to install or copy.

### Cowork

These plugins install and run in Cowork the same way. Verified against both
plugins on 2026-08-11, including the inline dashboard widgets and the
`assets/`.

A cloud session against a repository is different. Declare the plugin in that
repo's `.claude/settings.json` under `enabledPlugins`. It then installs at
session start.

## Available plugins

| Plugin | Version | What it does | Needs |
|---|---|---|---|
| `netsuite-approval-review` | v29 | Reviews the bills, purchase orders and change orders in your NetSuite approval queue. Publishes a verdict per item to a live dashboard. Lets you approve or reject from it. | Claude in Chrome, signed in to NetSuite. The machine on and Chrome open whenever it runs. A workspace folder is recommended for state. The NetSuite MCP connector is optional. It adds bulk queries and the PO cross-check. |
| `procore-open-items-review` | v29 | Filters your Procore open items down to the ones awaiting your workflow response. Those are change risks, subcontractor invoices, commitment change orders and the commitments themselves. Verifies every figure against the attached support. Lets you respond from a dashboard. | Claude in Chrome, signed in to Procore. The machine on and Chrome open whenever it runs. A workspace folder is recommended for state. Procore has no connector. |

Purchase orders are reviewed. Their execute route has never fired against a
real purchase order. See G16, PO execute route
unfired.

The workspace folder is recommended, not required. A run without one works.
See F76, folderless runs work.

**Checking what you have installed.** Open profile at the bottom left. Go to
**Settings → Plugins** and click the plugin. The last sentence of its
Description is the installed version, in the form "Skill version N — date".
The same number starts each skill's one-line description, as `vN — …`. It also
sits at the top of `SKILL.md`. Ask in a chat and the skill reports it. Compare
that number to the Version column above. A lower number means your copy is
stale. No version anywhere means the same. Update or reinstall the plugin.

## For maintainers: releasing an update

Push to the default branch. That is the whole release. The version resolves
from the commit SHA, so every push is a new version. Observed 2026-08-11: an
install reports a commit SHA prefix as its version.

If the push changes anything under a skill, bump two places in the same commit.
Bump that skill's `**Skill version N — date.**` line. Bump the Version cell in
the table above. `validate.py` checks that the two agree. It cannot check the
bump itself, so that part is habit.

Teammates get an update automatically only while auto sync is on for this
marketplace. Turn it on from `/plugin` → **Marketplaces** →
`compass-claude-plugins` → **Enable auto-update**. Claude Code then refreshes
in the background after a session starts. How soon it refreshes is unmeasured.

Without auto sync, someone must run the two-command update from a terminal.
Prefer the CLI form over the `/plugin` one. It prints the before and after
versions. It also surfaces the qualifier error instead of failing quietly.

```
claude plugin marketplace update compass-claude-plugins
claude plugin update netsuite-approval-review@compass-claude-plugins
claude plugin update procore-open-items-review@compass-claude-plugins
```

Those terminal commands update terminal installs only. Plugins installed
through the desktop app live in a separate account-synced store. Force-update
those in the app: **Settings → Plugins → Browse → Personal →
`claude-sharables` → ⋯ → Check for updates**. That menu's **Synced commit**
should match the tip of `main`. The onboarding sheet walks teammates through
it.

If **Check for updates** does not move the synced commit, restart the computer.
Restarting the computer is the observed workaround. An app restart is not
reliably enough on Windows for a plugin change to show up. See
F66, restart the computer.

## Adding another plugin or skill

Drop the plugin in `plugins/<name>/` with its own
`.claude-plugin/plugin.json`. Register it in `.claude-plugin/marketplace.json`
with a `git-subdir` source pointing at `plugins/<name>`. Then run
`python3 scripts/validate.py`.

The layout rules are D4, git-subdir sources;
D9, no version field; and D56,
prerequisite bucket. Records live under `decisions/`, `findings/` and `gaps/`.

## Checks

`scripts/validate.py` runs in CI on every push and pull request.

```bash
python3 scripts/validate.py
```

It checks seven things:

- Every marketplace entry resolves to a plugin folder, and the names agree.
- No `plugin.json` and no marketplace entry sets a `version` field.
- Every skill asset path resolves through `${CLAUDE_PLUGIN_ROOT}` and exists.
- The two repo-root documents name every registered plugin and no unregistered
  one.
- Each Version cell in the table above matches that skill's version line.
- Neither of those documents tells anyone to write a relative-path source.
- The shared-block checks in `scripts/shared_blocks.py` pass.

Every other command, URL and path in this README is unchecked.

One check does not run in CI, because it needs a browser. The dashboards place
a floating header from JavaScript, against the slice of the page the reader can
see. No static check can see where it lands. `scripts/measure_float.js`
publishes both dashboards from fixtures. It serves them cross-origin into a
scrolling host. It then measures the bar's real viewport position. Run it by
hand after changing the dashboard layout:

```bash
NODE_PATH=$(npm root -g) node scripts/measure_float.js   # needs playwright + chromium
```

## Distribution: why this repo is public

Distribution is by link. Send a teammate the two install commands above. Ask
them to enable auto-update. There is no admin step and no access to grant.

The repo is public on purpose. That is the only setting where the
link-and-auto-update route needs no per-person setup and has no silent failure
mode.

| Repo | Teammate needs a GitHub account? | Auto-update |
|---|---|---|
| **Public**, what we do | No, an anonymous clone works | Works, unmeasured |
| Private over SSH | Yes, plus repo access | Works only while their key is in `ssh-agent` |
| Private over HTTPS | Yes, plus repo access | Degrades, see below |

Going private would cost a GitHub account and a repo grant per teammate. It
would also make updates unreliable. The background refresh disables git
credential helpers for its `git pull`. So it cannot authenticate to a private
HTTPS remote. It falls back to re-cloning the whole marketplace. Whether that
re-clone times out is unmeasured. The result is a teammate who silently stops
receiving updates. That is the failure the no-version rule exists to prevent.
See D9, no version field. SSH remotes avoid the problem, but
only while every teammate keeps a key loaded in `ssh-agent`.

One tradeoff is accepted in exchange. Both plugins are world-readable. They are
not enterprise-private, and anyone can fork them. They describe approval gates
and cost-field mappings. Never commit a token or a credential. Shipped examples
use placeholders, never live tenant ids, counterparty names or amounts.
Maintainer records may name a business record id, where that id is the evidence
for a documented defect. See D13, public repo.

<details>
<summary>The one route that would beat public, and why it is not used</summary>

On a Team or Enterprise plan an admin can distribute a marketplace from
`claude.ai/admin-settings/plugins`. It reads the repo through the Claude GitHub
App and packages each plugin. Teammates then need no GitHub account, no repo
access, and run nothing at all. They do not even set the auto-update toggle.

It is unused here for two reasons. It requires an admin to own distribution,
and this marketplace is deliberately self-serve. It also requires the repo to
be private or internal, so adopting it later means flipping visibility.

The `git-subdir` sources this repo uses are supported by that route, so no
rework would be needed. One step comes before any of it. A personal account
owns this repo, not the Compass organization. Whether org sync accepts a
personally-owned private repo is not documented. Moving the repo into the
organization would be the first step, not flipping visibility.

</details>
