# Findings

Generated from the frontmatter and the first outcome sentence of every record in this folder, sorted by `date` then `slug`.

| id | slug | title | status | date | outcome |
|---|---|---|---|---|---|
| F1 | `bare-folder-name-invalid` | A bare folder name fails | observed | 2026-08-11 | A marketplace entry that passes JSON review also installs. |
| F2 | `cowork-runs-plugins` | Cowork runs installed plugins | observed | 2026-08-11 | A teammate can run both plugins in the session they were told to use. |
| F3 | `disjoint-host-bridges` | Host bridges do not overlap | observed | 2026-08-11 | A dashboard button starts a real turn instead of failing closed. |
| F4 | `git-url-needs-dot-git` | A git URL needs .git | observed | 2026-08-11 | A marketplace URL clones the repo instead of reading one file. |
| F5 | `no-duplicate-copy-warning` | No duplicate-copy warning | observed | 2026-08-11 | A teammate is not sent hunting for a shadow copy that does not exist. |
| F6 | `plugin-root-does-not-work` | pluginRoot does not work | observed | 2026-08-11 | Nobody spends a round on a documented shortcut that fails at install. |
| F7 | `relative-path-source-app-fail` | Relative source fails in app | observed | 2026-08-11 | A teammate installing from the desktop app gets the plugin. |
| F8 | `skill-invocation-verified` | Both slash forms resolve | observed | 2026-08-11 | A teammate can invoke a plugin skill by the short name. |
| F9 | `two-command-update` | Updating needs two commands | observed | 2026-08-11 | A maintainer can see whether an update actually shipped. |
| F10 | `connector-lag-verify-record` | Verify the record not queue | observed | 2026-08-12 | A successful approval is never logged as a failure and never clicked twice. |
| F11 | `shared-state-filename-collision` | A shared filename crossed records | observed | 2026-08-12 | Each skill log holds its own records only. |
| F12 | `show-widget-inline-only` | show_widget takes content inline | observed | 2026-08-12 | A reviewer sees a dashboard instead of a line of text. |
| F13 | `widget-sendprompt-works` | sendPrompt posts to chat | observed | 2026-08-12 | A reviewer executes a batch with one click and no clipboard. |
| F14 | `getdocument-needs-uint8array` | getDocument needs a typed array | observed | 2026-08-13 | A valid PDF parses instead of sending someone to debug the fetch. |
| F15 | `pdf-rows-blocked-filter` | Stub rows trip the filter | observed | 2026-08-13 | An extracted invoice page returns figures instead of a redaction marker. |
| F16 | `pdfjs-in-page-csp-allows` | pdf.js runs in-page | observed | 2026-08-13 | No attachment reaches disk, and no download step can fail. |
| F17 | `attachment-sniff-six-outcomes` | Six attachment outcomes | observed | 2026-08-14 | A workbook and an image are read instead of reported unreadable. |
| F18 | `cco-holder-id-route` | CCO workflow hangs off holder.id | observed | 2026-08-14 | A commitment change order gets response buttons instead of a dead gate. |
| F19 | `cco-verbs-follow-step` | CCO verbs follow the step | observed | 2026-08-14 | A dashboard shows the buttons the record actually offers. |
| F20 | `computer-only-visual-read` | One visual read exists | observed | 2026-08-14 | A scanned invoice is looked at instead of reported unreadable. |
| F21 | `fanout-three-states-cap` | The fan-out caps concurrency | observed | 2026-08-14 | A blip during a fan-out is named, not counted as an item with nothing to do. |
| F22 | `javascript-tool-denied-classifier` | The classifier can deny everything | observed | 2026-08-14 | A denial stops the run instead of being routed around. |
| F23 | `output-filter-second-trigger` | The filter has two triggers | observed | 2026-08-14 | A dotted identifier in construction data reaches a verdict as itself. |
| F24 | `stale-install-reads-as-repo-bug` | Stale install reads as bug | observed | 2026-08-14 | A maintainer checks the install version before editing a file that is already right. |
| F25 | `xlsx-cdnjs-import-works` | The cdnjs import works | observed | 2026-08-14 | A workbook attachment is read with the simplest loader. |
| F26 | `xml-scratch-tab-no-createelement` | The scratch tab is XML | observed | 2026-08-14 | A rasterised PDF page renders instead of throwing. |
| F27 | `approve-notes-same-tab-freeze` | The notes click navigates | observed | 2026-08-15 | A frozen tab never produces a second click on a bill already approved. |
| F28 | `cowork-shell-no-plugin-dir` | Cowork shell cannot see plugins | observed | 2026-08-15 | A stale workspace copy is visible instead of silent. |
| F29 | `fewer-larger-tool-calls` | Fewer, larger tool calls | settled | 2026-08-15 | A session spends its turns on work, not on round trips. |
| F30 | `old-chat-replays-old-dashboard` | Old chats replay old dashboards | observed | 2026-08-15 | A maintainer does not blame an install for a button rendered weeks ago. |
| F31 | `per-page-100-required` | Workflow queries need per_page | observed | 2026-08-15 | A live workflow instance is found instead of skipped. |
| F32 | `permission-mode-unreadable` | Four rounds, no bug | settled | 2026-08-15 | A permission question converges in one round instead of four. |
| F33 | `plain-approve-noop-user-activation` | Plain Approve can no-op | observed | 2026-08-15 | A click that did nothing is caught before the batch moves on. |
| F34 | `promise-serialised-empty` | A returned promise serialises empty | observed | 2026-08-15 | A null result is never read as an empty result. |
| F35 | `workflows-tools-v2-works` | The tools endpoint needs v2 | observed | 2026-08-15 | A new item type is looked up instead of guessed. |
| F36 | `wrong-id-returns-200-empty` | A wrong id returns empty | observed | 2026-08-15 | A live item is never logged as actioned by someone else. |
| F37 | `github-io-egress-blocked` | The live page is unfetchable | observed | 2026-08-17 | A blocked fetch is not read as a broken site. |
| F38 | `connector-lapses-reported` | The lapse cadence is reported | observed | 2026-08-19 | A teammate files a lapsed connector as normal, not as a plugin bug. |
| F39 | `connector-needs-second-account` | The connector needs another account | observed | 2026-08-19 | A teammate knows whether they were provisioned or not. |
| F40 | `netsuite-view-controls-port` | NetSuite got the Procore toolbar | observed | 2026-08-19 | Both dashboards sort, filter and search the same way. |
| F41 | `age-clamp-wrong-in-comparator` | Never clamp an ordering key | observed | 2026-08-20 | A future-dated row sorts correctly and reads sensibly. |
| F42 | `bill-po-from-ordbill-link` | Bill PO comes from linkage | observed | 2026-08-20 | No correctly coded bill is flagged as miscoded. |
| F43 | `ordbill-dedupe-line-pairs` | Dedupe the link rows first | observed | 2026-08-20 | A billed-to-date total is the truth, not a multiple of it. |
| F44 | `procore-newest-is-deadline-proxy` | Procore newest is a proxy | observed | 2026-08-20 | Nobody reads a Procore deadline as an origin date. |
| F45 | `retraction-not-applied-to-sheet` | A retraction reached one surface | observed | 2026-08-20 | No session cites a claim this repo already withdrew. |
| F46 | `sniff-table-reported-working` | The sniff table is working | observed | 2026-08-20 | Nobody redesigns a working type check, and nobody cites an unfired branch. |
| F47 | `sticky-needs-taller-parent` | Sticky resolves against its parent | observed | 2026-08-20 | A pinned bar has somewhere to travel. |
| F48 | `app-store-separate-update-path` | App installs update in-app | observed | 2026-08-21 | A teammate can force an update and read which release they run. |
| F49 | `plugin-list-cli-only` | plugin list sees CLI installs | observed | 2026-08-21 | An empty terminal list is not read as a missing install. |
| F50 | `version-line-wording-set-by-run` | A run set version wording | observed | 2026-08-21 | A teammate asking a skill its version gets an answer they can act on. |
| F51 | `actioned-bin-never-rendered` | Actioned bin never rendered | settled | 2026-08-24 | The queue count on the dashboard matches the queue. |
| F52 | `amber-boilerplate-removed` | Amber was the real finding | observed | 2026-08-24 | An amber warning means look here. |
| F53 | `audit-list-worked` | Working the audit list | settled | 2026-08-24 | An audit finding ends as a check or a stated reason, never as a note. |
| F54 | `bigger-type-measured-worse` | Bigger type measured worse | observed | 2026-08-24 | A density change is judged by a measurement, not by a look. |
| F55 | `blind-critique-card-rules` | Four rules from a critique | observed | 2026-08-24 | Every row title starts at the same x, and a flagged row still reads as flagged. |
| F56 | `dashboard-drift-six-defects` | Six defects from dashboard drift | settled | 2026-08-24 | A fix that reaches one plugin reaches the other one. |
| F57 | `disabled-button-three-states` | One disabled style, two meanings | observed | 2026-08-24 | A blocked execute button reads as blocked, not as broken. |
| F58 | `freshness-fold-flex-regression` | A fold restored the height | observed | 2026-08-24 | The chrome above the first item is smaller, measurably. |
| F59 | `more-button-needs-clipping` | A clamp needs real clipping | observed | 2026-08-24 | A control that is offered does something visible. |
| F60 | `netsuite-no-slim-build` | NetSuite cannot fold rows | superseded | 2026-08-24 | Nobody adds a feature to NetSuite that would copy a file byte for byte. |
| F61 | `nine-agent-prose-audit` | Nine agent prose audit | settled | 2026-08-24 | The text closest to a real approve click is governed text. |
| F62 | `no-run-without-browser` | Nothing runs without Chrome | observed | 2026-08-24 | A missed window is covered by a later one instead of being lost. |
| F63 | `onboarding-claims-unchecked` | Four claimed tests were absent | observed | 2026-08-24 | Every claim about the onboarding sheet has a reader or is deleted. |
| F64 | `plugin-command-two-surfaces` | Two plugin commands exist | observed | 2026-08-24 | An instruction names the surface it works on. |
| F65 | `render-unverifiable-ask-user` | The render is unverifiable agent-side | observed | 2026-08-24 | A truncated dashboard is reported instead of hidden. |
| F66 | `restart-computer-not-app` | Restart the computer | observed | 2026-08-24 | A teammate sees a plugin install or update without running a command. |
| F67 | `sheet-time-and-posture` | Say how long and where | observed | 2026-08-24 | A teammate starts the setup today instead of deferring it. |
| F68 | `skill-md-block-eligibility` | Only 34 SKILL.md lines eligible | observed | 2026-08-24 | Nobody rewords a correct skill to raise a sharing percentage. |
| F69 | `slim-build-not-a-fallback` | Slim build is no fallback | settled | 2026-08-24 | A skipped item keeps the response button it most often needs. |
| F70 | `slim-build-saves-little` | The slim build saves little | superseded | 2026-08-24 | A reviewer keeps the response buttons a folded row would cost. |
| F71 | `staleness-check-blind` | Staleness check was blind | settled | 2026-08-24 | A run tells the user when its workspace copies are old. |
| F72 | `tick-must-not-render` | The tick must not render | observed | 2026-08-24 | An open detail stays open while the reader reads it. |
| F73 | `attachment-file-evidences-verdict` | Name the file read | observed | 2026-08-26 | A clear item can be asked what was read to clear it. |
| F74 | `capability-verdicts-gate` | Capability rows name real verdicts | observed | 2026-08-26 | A capability table cannot promise a verdict the publish script rejects. |
| F75 | `cowork-storage-leads` | Cowork storage leads only | unobserved | 2026-08-26 | A session reads a research note as leads, never as settled behaviour. |
| F76 | `folderless-run-works` | Folderless run works | observed | 2026-08-26 | A teammate with no workspace folder can still review their queue. |
| F77 | `folderless-scheduled-run-works` | Folderless scheduled run works | observed | 2026-08-26 | A teammate schedules a run without first choosing a folder. |
| F78 | `marketplace-add-tests-published-tree` | marketplace add tests the release | observed | 2026-08-26 | A pre-push check answers the question a maintainer asked it. |
| F79 | `netsuite-visual-read-thin` | NetSuite visual read prose thin | settled | 2026-08-26 | Procedure gets written from an observation, not from symmetry. |
| F80 | `parity-audit-two-false` | Two audit findings were wrong | observed | 2026-08-26 | A parity audit is read as evidence, not as a diff of vocabularies. |
| F81 | `plugin-dir-loads-working-tree` | plugin-dir loads the working tree | observed | 2026-08-26 | A maintainer can prove a change installs before pushing it. |
| F82 | `widget-iframe-does-not-scroll` | The widget frame never scrolls | observed | 2026-08-26 | No version is spent fixing a defect this host cannot produce. |
| F83 | `portlet-empty-case-ladder` | No portlet found lacked rule | observed | 2026-08-27 | A partial queue is named as partial in the same breath as its count. |
| F84 | `tiled-sentinels-track-band` | Tiled sentinels track the band | observed | 2026-08-27 | A reader mid-queue has the filter state and the commit button on screen. |
| F85 | `workspace-write-works` | The workspace write works | observed | 2026-08-27 | State persists between runs, so first-run setup is asked once. |
| F86 | `write-states-kept-refused-not-attempted` | Three write states | observed | 2026-08-27 | A run that never tried the write says so, instead of reporting a failure. |
| F87 | `commitment-payload-three-of-four` | Three borrowed names in four | observed | 2026-08-28 | A dashboard column names the real counterparty. |
| F88 | `commitment-two-collections` | One kind covers two collections | observed | 2026-08-28 | A commitment link and its gate query name the right collection. |
| F89 | `onboarding-copy-buttons` | Onboarding copy buttons work | settled | 2026-08-28 | A teammate pastes the whole schedule prompt on one click. |
| F90 | `prohibition-list-let-a-stray-through` | A list let strays through | observed | 2026-08-28 | A prohibition catches the next instance, not only the last one. |
| F91 | `a-wrong-run-found-four-defects` | A wrong run found defects | observed | 2026-09-01 | A run is judged claim by claim, not accepted or dismissed whole. |
| F92 | `dehydrated-onedrive-rename-over` | A dehydrated file needs rename-over | observed | 2026-09-01 | A run on a cloud mount can still write its state file. |
| F93 | `invented-threshold-in-comment` | An asset invented a threshold | observed | 2026-09-01 | A run cannot assemble an authoritative refusal out of repo text. |
| F94 | `netsuite-po-execute-gap` | NetSuite could not click POs | observed | 2026-09-01 | Every reviewed type can be actioned. |
| F95 | `pycache-stray-file` | Python bytecode left a stray | observed | 2026-09-01 | The workspace folder holds only files a step names. |
| F96 | `render-read-wall-serialise` | Read-side wall, fixed by serialise | observed | 2026-09-01 | A 62-item dashboard fits in one file read. |
| F97 | `two-custom-tools-unchecked` | Second custom tool unchecked | observed | 2026-09-01 | Every custom tool in the queue is read against its own fields. |
| F98 | `run-self-banned-login` | A run banned itself again | settled | 2026-09-10 | An expired session gets a hand-off the user can act on, in the same run. |
| F99 | `device-shots-first-run` | Device shots first run | observed | 2026-09-15 | The three widths and the two themes are measured, not assumed. |
| F100 | `record-checks-mutation-tested` | Record checks went red first | observed | 2026-09-15 | A check is trusted only after it fails on the defect it guards. |
| pending | `fetch-tab-state-lost` | Fetch tab navigated, first pass lost | observed | 2026-09-16 | A run fetches its data once, and leaves no tab parked on a dead link. |
| F101 | `mandate-gaps-closed` | Three mandate gaps closed | observed | 2026-09-16 | Three mandate rules run as a command, not a memory. |
