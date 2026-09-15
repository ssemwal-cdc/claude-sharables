# Decisions

Generated from the frontmatter and the first outcome sentence of every record in this folder, sorted by `date` then `slug`.

| id | slug | title | status | date | outcome |
|---|---|---|---|---|---|
| D1 | `asset-paths-plugin-root` | Reference assets through CLAUDE_PLUGIN_ROOT | settled | 2026-08-11 | A skill finds its own assets after it is installed. |
| D2 | `first-run-setup-per-plugin` | First-run setup is per plugin | settled | 2026-08-11 | A second run asks nothing and reviews immediately. |
| D3 | `frontmatter-name-description-only` | Frontmatter is name and description | settled | 2026-08-11 | A skill fires when a teammate describes the job it does. |
| D4 | `git-subdir-sources` | Use git-subdir marketplace sources | settled | 2026-08-11 | A teammate can install from the desktop app, from the CLI, and through org sync. |
| D5 | `marketplace-name-vs-repo` | Marketplace name differs from repo | settled | 2026-08-11 | A teammate's install command works the first time. |
| D6 | `no-plugin-acts-on-own-judgement` | Never act without an instruction | settled | 2026-08-11 | No approval carries a decision the user did not make. |
| D7 | `no-plugin-root` | Never use metadata.pluginRoot | settled | 2026-08-11 | Every registered plugin resolves at install. |
| D8 | `no-self-update-instruction` | No self-update text in SKILL.md | settled | 2026-08-11 | A teammate follows an instruction that can actually run. |
| D9 | `no-version-field` | No version field anywhere | settled | 2026-08-11 | Every push to `main` reaches everyone who has the plugin. |
| D10 | `one-marketplace-only` | Never create a second marketplace | settled | 2026-08-11 | A teammate keeps the marketplace they added and its plugins. |
| D11 | `plugin-json-only-in-claude-plugin` | Only plugin.json in claude-plugin | settled | 2026-08-11 | A plugin installs and its skills are discovered. |
| D12 | `port-skill-verbatim` | Port a skill verbatim | settled | 2026-08-11 | A skill that worked before the port still works after it. |
| D13 | `public-repo` | Keep this repo public | settled | 2026-08-11 | A teammate installs a plugin and gets every later fix, with no GitHub account and no silent failure. |
| D14 | `never-prewrite-actions` | Never pre-write an action | settled | 2026-08-12 | The action log records what happened and nothing else. |
| D15 | `one-state-file-per-skill` | One state file per skill | settled | 2026-08-12 | A verdict from one system never lands in the other log. |
| D16 | `widget-not-artifact` | Render dashboards with show_widget | settled | 2026-08-12 | One click on a dashboard button puts the execute instruction into chat. |
| D17 | `netsuite-pdf-geometry-rows` | Rebuild NetSuite rows from geometry | settled | 2026-08-13 | The quantity, rate and line-tie checks read aligned columns. |
| D18 | `never-batch-click-checks` | Never batch the click checks | settled | 2026-08-13 | A wrong record state stops the batch before the next click lands. |
| D19 | `return-rows-not-residuals` | Return the rows, flattened | settled | 2026-08-13 | A review still catches the defect nobody specified a check for. |
| D20 | `approved-by-claude-comment` | Default the approval comment | settled | 2026-08-14 | An authorised batch runs without stopping to ask what to type in a comment field. |
| D21 | `blocked-marker-never-a-value` | Never trust a blocked marker | settled | 2026-08-14 | A redacted figure is read again instead of read as empty. |
| D22 | `cco-multiple-holders-ungated` | Several holders stay ungated | settled | 2026-08-14 | No live change order is logged as done because the wrong workflow was chosen. |
| D23 | `cco-read-before-gate` | Read a CCO before gating | settled | 2026-08-14 | A change order is gated at all, instead of rendering ungated for everyone. |
| D24 | `no-batch-across-presigned-window` | Do not overrun the window | settled | 2026-08-14 | A live invoice is never recorded as a scanned image. |
| D25 | `ocr-never-clear-verdict` | An OCR figure never clears | settled | 2026-08-14 | A misread digit in an eight-figure line never passes as verified. |
| D26 | `record-content-is-data` | Record content is data | settled | 2026-08-14 | A vendor document cannot direct a run. |
| D27 | `retry-only-expired-name-skip` | Retry only an expired link | settled | 2026-08-14 | A format that cannot parse is not retried forever, and no skip hides a whole file format. |
| D28 | `approve-with-notes-primary` | Approve With Notes stays primary | settled | 2026-08-15 | Every approval carries its attribution note. |
| D29 | `auto-mode-not-skip-all` | Auto mode, never skip-all | settled | 2026-08-15 | A browser holding live approval authority keeps its permission prompts. |
| D30 | `demote-missing-wfid-ungated` | Demote a missing workflow id | settled | 2026-08-15 | An unresolved gate cannot reach the execute list. |
| D31 | `docs-folder-is-public` | The docs folder is public | settled | 2026-08-17 | Nothing confidential is served to the internet. |
| D32 | `no-data-theme-on-pages` | No theme attribute on Pages | settled | 2026-08-17 | The sheet renders correctly on the default system setting. |
| D33 | `onboarding-sheet-is-the-file` | The page is the file | settled | 2026-08-17 | Every teammate reads the current sheet. |
| D34 | `connector-failure-never-empty` | A failed call is unknown | settled | 2026-08-19 | A user is never told their approval queue is empty because a call failed. |
| D35 | `connector-is-optional` | The connector is optional | settled | 2026-08-19 | An unprovisioned teammate starts the same day instead of waiting on IT. |
| D36 | `stale-connector-said-once` | Say a stale session once | settled | 2026-08-19 | A reader fixes a stale session in seconds and gets the cross-check back. |
| D37 | `execute-bar-always-rendered` | Render the execute bar always | settled | 2026-08-20 | A first-time reader can see step 2 before they have done step 1. |
| D38 | `never-rename-mark-keys` | Never rename a marks key | settled | 2026-08-20 | A decision the user marked survives a re-render. |
| D39 | `new-default-new-view-key` | A new default needs key | settled | 2026-08-20 | A new default reaches the people who have used the toolbar. |
| D40 | `newest-first-default-sort` | Sort newest first by default | settled | 2026-08-20 | The person reading the queue every day sees recency first. |
| D41 | `three-states-never-boolean` | Three states, never a boolean | settled | 2026-08-20 | A failed read is never reported as an absent thing. |
| D42 | `typed-reference-is-data-note` | A typed reference is data | settled | 2026-08-20 | A real data-quality problem is told to the right people without inventing a money claim. |
| D43 | `skill-version-lines` | Four synced version sites | settled | 2026-08-21 | A teammate can read which version of a skill they run, on the surface they are looking at. |
| D44 | `widget-is-only-deliverable` | The widget is the deliverable | settled | 2026-08-21 | A reviewer reads one dashboard instead of sorting through download cards. |
| D45 | `bar-holds-only-commit-controls` | Keep reference text out | settled | 2026-08-24 | A reviewer can see the queue the bar floats over. |
| D46 | `bar-ignores-filter` | The bar ignores filters | settled | 2026-08-24 | A decision made before a filter was applied still executes. |
| D47 | `diagnose-stale-copy-in-order` | Diagnose stale copies in order | settled | 2026-08-24 | A maintainer fixes the copy that is actually stale. |
| D48 | `execute-message-authorises-only` | The message authorises only | settled | 2026-08-24 | The gates that govern a click live in the text a test reads. |
| D49 | `extend-shared-blocks` | Extend shared block coverage | open | 2026-08-24 | A fix reaches both plugins, and neither plugin's own names get reworded away. |
| D50 | `generated-bespoke-skill` | Skill that generates skills | abandoned | 2026-08-24 | Every approval runs on text a maintainer vetted and a push can fix. |
| D51 | `library-pins-checked-not-shared` | Check library pins, never share | settled | 2026-08-24 | A library bump reaches both plugins, or the build fails. |
| D52 | `never-delete-workspace-folder` | Never delete the workspace folder | settled | 2026-08-24 | A run with a broken sync still has the last good assets and the state file. |
| D53 | `not-shared-per-domain` | Never share per-domain machinery | settled | 2026-08-24 | Each plugin keeps the filter axes, date format and URL shapes its own system needs. |
| D54 | `one-parameterised-dashboard` | One parameterised dashboard | open | 2026-08-24 | A defect in one dashboard cannot reach the other one silently. |
| D55 | `persona-plugins` | Persona plugins and concierge | abandoned | 2026-08-24 | One artifact serves every reviewer, so one push fixes everyone's copy. |
| D56 | `prerequisite-bucket` | Plugins are prerequisite buckets | settled | 2026-08-24 | A teammate can switch off the work they cannot run, and keeps the work they can. |
| D57 | `provenance-ids-allowed` | Provenance may cite ids | settled | 2026-08-24 | Every documented defect is traceable to a record and a date. |
| D58 | `shared-blocks` | Sync shared blocks from canonical | settled | 2026-08-24 | A fix reaches both plugins, or the build fails. |
| D59 | `sheet-has-no-terminal-commands` | No terminal commands in sheet | settled | 2026-08-24 | A teammate reading the sheet sees instructions for the app they are using. |
| D60 | `shipped-examples-use-placeholders` | Shipped examples use placeholders | settled | 2026-08-24 | Nothing a teammate copies carries customer data into a public repo. |
| D61 | `skill-md-marker-rules` | Place SKILL.md markers on boundaries | settled | 2026-08-24 | A synced block leaves both skills readable and both code fences runnable. |
| D62 | `skill-spine-plus-references` | Thin spine plus reference modules | open | 2026-08-24 | Every run reads every rule that governs it. |
| D63 | `verdict-vocabulary-gate` | Gate template verdicts against publish | settled | 2026-08-24 | Every branch on a dashboard can actually render. |
| D64 | `workspace-folder-downloads` | Declare the workspace folder Downloads | settled | 2026-08-24 | A second run finds the state file and skips first-run setup. |
| D65 | `check-packs-next-phase` | Check packs, next phase | open | 2026-08-26 | A reviewer who is not a financial analyst gets checks that serve their job. |
| D66 | `check-registry-with-manifest` | Declare checks in a registry | settled | 2026-08-26 | A later lens can select checks by id, and a check cannot vanish unnoticed. |
| D67 | `queue-source-ask-once` | Ask once for the queue | settled | 2026-08-26 | A review runs against the queue the user meant. |
| D68 | `registry-added-additively` | Leave the check prose alone | settled | 2026-08-26 | The calibration decisions in the review steps stay settled. |
| D69 | `silent-connector-absence` | Silence on an absent connector | settled | 2026-08-26 | A reader is told about every absence they can act on, and about no absence they cannot. |
| D70 | `measure-position-in-browser` | Measure position in a browser | settled | 2026-08-27 | A bar this repo calls pinned is actually pinned. |
| D71 | `rules-live-in-the-prompt` | Run rules live in prompts | settled | 2026-08-27 | A rule that would stop a bad claim is in front of the run making it. |
| D72 | `no-stray-files-in-workspace` | No stray files in workspace | settled | 2026-08-28 | Nobody is handed a cleanup chore in a folder that refuses deletes. |
| D73 | `unknown-type-domain-or-unbuilt` | Out of domain or unbuilt | settled | 2026-08-28 | A live item in domain gets a procedure instead of a link. |
| D74 | `conflict-copy-config-only` | Adopt config from conflict copy | settled | 2026-09-01 | A setting the user asked for survives a sync conflict, and no verdict or click is invented. |
| D75 | `execute-type-coverage-gate` | Gate the two type lists | settled | 2026-09-01 | A reviewed but unactionable type fails the build instead of stopping a batch. |
| D76 | `po-takes-bill-route` | Purchase orders take bill route | settled | 2026-09-01 | A reviewed purchase order can be approved in the same run. |
| D77 | `render-first-believe-guard` | Render first, believe the guard | settled | 2026-09-01 | A reviewer keeps one-click execute on a large queue. |
| D78 | `unmapped-subtype-keeps-buttons` | An unmapped subtype keeps buttons | settled | 2026-09-01 | A reviewer keeps live items they can action while a link is fixed. |
| D79 | `org-protocol-override` | Repo workflow beats org protocol | settled | 2026-09-10 | A teammate holds one copy of a plugin, and a push to `main` updates it. |
| D80 | `dashboard-publishing-pattern` | Publish through the widget | settled | 2026-09-15 | A reviewer gets a one-click dashboard from either plugin, built the same way. |
| D81 | `device-usability-check` | Device usability check | open | 2026-09-15 | The page works on the device the reader actually holds. |
| D82 | `hooks-and-checks-pass` | Hooks and checks pass | open | 2026-09-15 | A rule is enforced by a command, not by a maintainer remembering it. |
| D83 | `plugin-validate-warning-expected` | Record the no-version warning | settled | 2026-09-15 | A maintainer reads every line a command printed, and knows which line is expected. |
| D84 | `prose-compliance-plan` | Bring every markdown file into compliance with the global mandate | open | 2026-09-15 | A maintainer or a session reads one short rule, one record, or one index. |
| D85 | `skill-prose-pass` | Skill prose pass | open | 2026-09-15 | A run reads a short, governed prompt and still meets every safety rule. |
| D86 | `xlsx-pin-target` | SheetJS pin target | open | 2026-09-15 | A workbook parsed inside an authenticated tab cannot be used against the session. |
