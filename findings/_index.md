# Findings

Generated from the frontmatter and the first outcome sentence of every record in this folder, sorted by `date` then `slug`.

| id | slug | title | status | date | outcome |
|---|---|---|---|---|---|
| F1 | `bare-folder-name-invalid` | A bare folder name fails | observed | 2026-08-11 | A marketplace entry that passes JSON review also installs. |
| F2 | `cowork-runs-plugins` | Cowork runs installed plugins | observed | 2026-08-11 | A teammate can run both plugins in the session they were told to use. |
| F3 | `disjoint-host-bridges` | Host bridges do not overlap | observed | 2026-08-11 | A dashboard button starts a real turn instead of failing closed. |
| F4 | `git-url-needs-dot-git` | A git URL needs .git | observed | 2026-08-11 | A marketplace URL clones the repo instead of reading one file. |
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
| F5 | `confounded-comparison-looked-like-fix` | A confound looked like a result | observed | 2026-08-15 | A permission question converges in one round instead of four. |
| F28 | `cowork-shell-no-plugin-dir` | Cowork shell cannot see plugins | observed | 2026-08-15 | A stale workspace copy is visible instead of silent. |
| F29 | `diagnostic-overgeneralized-from-probe` | A probe was read as evidence about the workflow | observed | 2026-08-15 | A permission question converges in one round instead of four. |
| F32 | `mechanical-edits-are-not-semantic` | Mechanical edits do not need Edit's guard | settled | 2026-08-15 | A session spends its turns on work, not on round trips. |
| F30 | `old-chat-replays-old-dashboard` | Old chats replay old dashboards | observed | 2026-08-15 | A maintainer does not blame an install for a button rendered weeks ago. |
| F31 | `per-page-100-required` | Workflow queries need per_page | observed | 2026-08-15 | A live workflow instance is found instead of skipped. |
| F42 | `permission-mode-unreadable-by-agent` | An agent cannot read its own permission mode | settled | 2026-08-15 | A permission question converges in one round instead of four. |
| F33 | `plain-approve-noop-user-activation` | Plain Approve can no-op | observed | 2026-08-15 | A click that did nothing is caught before the batch moves on. |
| F34 | `promise-serialised-empty` | A returned promise serialises empty | observed | 2026-08-15 | A null result is never read as an empty result. |
| F51 | `run-before-reading-wastes-turns` | Running before reading wasted two turns | settled | 2026-08-15 | A session spends its turns on work, not on round trips. |
| F53 | `serial-reads-should-batch` | Independent reads went out serially | settled | 2026-08-15 | A session spends its turns on work, not on round trips. |
| F56 | `unresolved-confound-stayed-off-main` | A doubted fix stayed off main | observed | 2026-08-15 | A fabricated step never ships to teammates. |
| F61 | `whole-file-reads-beat-eight-slices` | One read beats eight slices of one file | settled | 2026-08-15 | A session spends its turns on work, not on round trips. |
| F35 | `workflows-tools-v2-works` | The tools endpoint needs v2 | observed | 2026-08-15 | A new item type is looked up instead of guessed. |
| F36 | `wrong-id-returns-200-empty` | A wrong id returns empty | observed | 2026-08-15 | A live item is never logged as actioned by someone else. |
| F37 | `github-io-egress-blocked` | The live page is unfetchable | observed | 2026-08-17 | A blocked fetch is not read as a broken site. |
| F38 | `connector-lapses-reported` | The lapse cadence is reported | observed | 2026-08-19 | A teammate files a lapsed connector as normal, not as a plugin bug. |
| F39 | `connector-needs-second-account` | The connector needs another account | observed | 2026-08-19 | A teammate knows whether they were provisioned or not. |
| F40 | `netsuite-view-controls-port` | NetSuite got the Procore toolbar | observed | 2026-08-19 | Both dashboards sort, filter and search the same way. |
| F41 | `age-clamp-wrong-in-comparator` | Never clamp an ordering key | observed | 2026-08-20 | A future-dated row sorts correctly and reads sensibly. |
| F67 | `attachment-sniff-workbooks-images-read` | Vendor workbooks and images read outside mocks | observed | 2026-08-20 | A workbook or an image is read, not filed as unreadable. |
| F69 | `contract-and-billed-off-unjoined-keys` | Contract and billed totals used unjoined keys | settled | 2026-08-20 | No correctly coded bill is flagged as miscoded. |
| F43 | `ordbill-dedupe-line-pairs` | Dedupe the link rows first | observed | 2026-08-20 | A billed-to-date total is the truth, not a multiple of it. |
| F71 | `phantom-po-miscoding-flag-was-wrong` | Bill PO comes from linkage | observed | 2026-08-20 | No correctly coded bill is flagged as miscoded. |
| F44 | `procore-newest-is-deadline-proxy` | Procore newest is a proxy | observed | 2026-08-20 | Nobody reads a Procore deadline as an origin date. |
| F45 | `retraction-not-applied-to-sheet` | A retraction reached one surface | observed | 2026-08-20 | No session cites a claim this repo already withdrew. |
| F46 | `sniff-table-reported-working` | The sniff table is working | observed | 2026-08-20 | Nobody redesigns a working type check, and nobody cites an unfired branch. |
| F47 | `sticky-needs-taller-parent` | Sticky resolves against its parent | observed | 2026-08-20 | A pinned bar has somewhere to travel. |
| F75 | `typed-reference-read-as-coding-not-linkage` | A typed reference was read as the coding | settled | 2026-08-20 | No correctly coded bill is flagged as miscoded. |
| F84 | `zero-billed-evidence-was-inverted` | Zero billed was read as corroboration | settled | 2026-08-20 | No correctly coded bill is flagged as miscoded. |
| F48 | `app-store-separate-update-path` | App installs update in-app | observed | 2026-08-21 | A teammate can force an update and read which release they run. |
| F49 | `plugin-list-cli-only` | plugin list sees CLI installs | observed | 2026-08-21 | An empty terminal list is not read as a missing install. |
| F50 | `version-line-wording-set-by-run` | A run set version wording | observed | 2026-08-21 | A teammate asking a skill its version gets an answer they can act on. |
| F98 | `absent-verdict-key-defaulted-clear` | A missing verdict defaulted to clear | settled | 2026-08-24 | A missing verdict key fails loud instead of defaulting to an approvable one. |
| F52 | `amber-boilerplate-removed` | Amber was the real finding | observed | 2026-08-24 | An amber warning means look here. |
| F100 | `audit-list-38-items-resolved` | 38 audit items closed with no decision | observed | 2026-08-24 | An audit finding ends as a check or a stated reason, never as a note. |
| F54 | `bigger-type-measured-worse` | Bigger type measured worse | observed | 2026-08-24 | A density change is judged by a measurement, not by a look. |
| F55 | `blind-critique-card-rules` | Four rules from a critique | observed | 2026-08-24 | Every row title starts at the same x, and a flagged row still reads as flagged. |
| F101 | `checks-whose-inputs-fail-together` | Some checks fail together with their inputs | observed | 2026-08-24 | A freshness check keeps one input that cannot go stale. |
| F104 | `chips-removed-two-facts-one-sentence` | Onboarding time now reads as one sentence | observed | 2026-08-24 | A teammate starts the setup today instead of deferring it. |
| F57 | `disabled-button-three-states` | One disabled style, two meanings | observed | 2026-08-24 | A blocked execute button reads as blocked, not as broken. |
| F105 | `docs-vs-code-drift-not-caught` | Docs pointing at removed code go uncaught | observed | 2026-08-24 | Prose that survives its own code's deletion is found, not left to drift forever. |
| F106 | `drift-check-built-from-six-defects` | The drift check came out of six defects | observed | 2026-08-24 | A one-sided edit, a reworded comment, a missing canonical file and an orphaned one all fail the build. |
| F107 | `execute-message-least-governed` | Execute message was least governed | settled | 2026-08-24 | The text closest to a real approve click is governed text. |
| F58 | `freshness-fold-flex-regression` | A fold restored the height | observed | 2026-08-24 | The chrome above the first item is smaller, measurably. |
| F108 | `hand-maintained-strings-drift-unchecked` | Hand-maintained strings drift unchecked | observed | 2026-08-24 | A claim that names an identifier gets a mechanical check, not just a human re-read. |
| F109 | `mechanism-replaces-second-screen-phrase` | A hardware phrase became a mechanism claim | observed | 2026-08-24 | A prerequisite reads as a thing you must have, not as a description of the wait. |
| F59 | `more-button-needs-clipping` | A clamp needs real clipping | observed | 2026-08-24 | A control that is offered does something visible. |
| F110 | `netsuite-bin-fed-dead-live-state` | NetSuite's actioned bin fed dead state | settled | 2026-08-24 | The queue count on the dashboard matches the queue. |
| F111 | `netsuite-co-buttons-are-the-gate` | NetSuite change orders gate on their buttons | settled | 2026-08-24 | A whole batch is never logged as actioned on a role mistake. |
| F60 | `netsuite-no-slim-build` | NetSuite cannot fold rows | superseded | 2026-08-24 | Nobody adds a feature to NetSuite that would copy a file byte for byte. |
| F112 | `netsuite-verdict-vocabulary-blocks-fold` | NetSuite cannot fold rows | settled | 2026-08-24 | Nobody adds a feature to NetSuite that would copy a file byte for byte. |
| F113 | `nine-agent-audit-corrected-four-claims` | Interview corrected four audit claims | observed | 2026-08-24 | A maintainer interview catches an auditor's wrong premise before it ships as a rule. |
| F62 | `no-run-without-browser` | Nothing runs without Chrome | observed | 2026-08-24 | A missed window is covered by a later one instead of being lost. |
| F63 | `onboarding-claims-unchecked` | Four claimed tests were absent | observed | 2026-08-24 | Every claim about the onboarding sheet has a reader or is deleted. |
| F114 | `phantom-bin-inflated-queue-count-only` | The dead bin inflated a count, not a click | observed | 2026-08-24 | A departed item never causes a wrong click, only a wrong number. |
| F64 | `plugin-command-two-surfaces` | Two plugin commands exist | observed | 2026-08-24 | An instruction names the surface it works on. |
| F115 | `procore-bin-blocked-by-verdict-guard` | Procore's actioned bin never worked | settled | 2026-08-24 | The queue count on the dashboard matches the queue. |
| F65 | `render-unverifiable-ask-user` | The render is unverifiable agent-side | observed | 2026-08-24 | A truncated dashboard is reported instead of hidden. |
| F66 | `restart-computer-not-app` | Restart the computer | observed | 2026-08-24 | A teammate sees a plugin install or update without running a command. |
| F116 | `same-session-self-fixes` | Three fixes to that session's own work | settled | 2026-08-24 | A reachability check catches the inequality form of a filter, not only the equality form. |
| F117 | `second-source-found-what-self-check-couldnt` | A second source found what self-checks could not | observed | 2026-08-24 | A plugin's own drift is found by comparison, not by asking it about itself. |
| F118 | `shared-block-loop-and-checks-enforced` | The shared-block loop ran for real | observed | 2026-08-24 | A claim that used to stand in for a check now runs as a check. |
| F119 | `shipped-examples-now-placeholders` | Shipped examples now use placeholders | settled | 2026-08-24 | A teammate cannot copy a live value out of a shipped example. |
| F120 | `six-one-sided-dashboard-defects` | Six defects from one-sided drift | settled | 2026-08-24 | A fix that reaches one plugin reaches the other one. |
| F68 | `skill-md-block-eligibility` | Only 34 SKILL.md lines eligible | observed | 2026-08-24 | Nobody rewords a correct skill to raise a sharing percentage. |
| F121 | `skill-md-duplication-not-block-coverable` | SKILL.md duplication resists the block mechanism | observed | 2026-08-24 | Nobody expects the shared-block mechanism to reach prose it cannot cover. |
| F122 | `skill-md-is-the-fixed-point-for-freshness` | SKILL.md is the fixed point for freshness | settled | 2026-08-24 | A run tells the user when its workspace copies are old. |
| F70 | `slim-build-saves-little` | The slim build saves little | superseded | 2026-08-24 | A reviewer keeps the response buttons a folded row would cost. |
| F123 | `slim-fold-saves-0-to-12-percent` | Slim build is no fallback | settled | 2026-08-24 | A skipped item keeps the response button it most often needs. |
| F124 | `staleness-check-missed-second-site` | Staleness fix was itself stale | settled | 2026-08-24 | A version check compares every site that carries the version, not just the first. |
| F125 | `step3-break-marker-relocated` | The onboarding break moved to step 3's end | observed | 2026-08-24 | A reader can find the point where they may stop. |
| F126 | `template-version-check-blind-to-lockstep` | The version check missed lockstep staleness | settled | 2026-08-24 | A run tells the user when its workspace copies are old. |
| F72 | `tick-must-not-render` | The tick must not render | observed | 2026-08-24 | An open detail stays open while the reader reads it. |
| F127 | `verdict-vocabulary-check-reproduces-bin` | The verdict check reproduces the dead bin | settled | 2026-08-24 | A check that passes because its own mutation never landed is caught, not trusted. |
| F128 | `withdrawn-uncommitted-fixtures` | Uncommitted fixtures were withdrawn, not faked | observed | 2026-08-24 | A certification that cannot be reproduced is withdrawn, not patched with an after-the-fact fixture. |
| F73 | `attachment-file-evidences-verdict` | Name the file read | observed | 2026-08-26 | A clear item can be asked what was read to clear it. |
| F74 | `capability-verdicts-gate` | Capability rows name real verdicts | observed | 2026-08-26 | A capability table cannot promise a verdict the publish script rejects. |
| F76 | `folderless-run-works` | Folderless run works | observed | 2026-08-26 | A teammate with no workspace folder can still review their queue. |
| F77 | `folderless-scheduled-run-works` | Folderless scheduled run works | observed | 2026-08-26 | A teammate schedules a run without first choosing a folder. |
| F78 | `marketplace-add-tests-published-tree` | marketplace add tests the release | observed | 2026-08-26 | A pre-push check answers the question a maintainer asked it. |
| F79 | `netsuite-visual-read-thin` | NetSuite visual read prose thin | settled | 2026-08-26 | A rule for reading an image or a scan reaches both skills in the same change. |
| F80 | `parity-audit-two-false` | Two audit findings were wrong | observed | 2026-08-26 | A parity audit is read as evidence, not as a diff of vocabularies. |
| F81 | `plugin-dir-loads-working-tree` | plugin-dir loads the working tree | observed | 2026-08-26 | A maintainer can prove a change installs before pushing it. |
| F82 | `widget-iframe-does-not-scroll` | The widget frame never scrolls | observed | 2026-08-26 | No version is spent fixing a defect this host cannot produce. |
| F129 | `floating-bar-mirrors-filter-and-commit` | The floating bar mirrors filter and commit only | observed | 2026-08-27 | A reader mid-queue has the filter state and the commit button on screen. |
| F130 | `intersection-observer-reads-clip-rect` | An observer reads scroll position across a frame | observed | 2026-08-27 | A reader mid-queue has the filter state and the commit button on screen. |
| F83 | `portlet-empty-case-ladder` | No portlet found lacked rule | observed | 2026-08-27 | A partial queue is named as partial in the same breath as its count. |
| F131 | `retile-on-resize-not-render` | Re-tiling hangs off a resize, not a render | observed | 2026-08-27 | A reader mid-queue has the filter state and the commit button on screen. |
| F132 | `sticky-fails-cross-origin-iframe` | CSS sticky cannot survive a cross-origin frame | observed | 2026-08-27 | A reader mid-queue has the filter state and the commit button on screen. |
| F133 | `tiled-sentinels-beat-single-sentinel` | Tiled sentinels track the band, one big one does not | observed | 2026-08-27 | A reader mid-queue has the filter state and the commit button on screen. |
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
| F134 | `hand-off-had-no-stated-action` | A hand-off rule named no action | settled | 2026-09-10 | A rule that forbids a retry also states the one action that replaces it. |
| F135 | `login-rewrite-caused-refusal` | A prose rewrite caused a login refusal | settled | 2026-09-10 | An expired session gets a hand-off the user can act on, in the same run. |
| F136 | `login-rung-three-named-outcomes` | Login rung now names three outcomes | settled | 2026-09-10 | A run decides the login screen on what is on screen, not on a misread absolute. |
| F137 | `onboarding-skill-login-contradiction` | Two files disagreed on login behaviour | settled | 2026-09-10 | Two files describing one behaviour to two audiences never contradict each other. |
| F138 | `password-box-correctly-triggers-wall` | A password box correctly triggers wall | observed | 2026-09-10 | The login table decides on the password box, not on whether an email field sits beside it. |
| F139 | `check-mutations-all-caught-defect` | Every record check caught its mutation | observed | 2026-09-15 | A check is trusted only after it fails on the defect it guards. |
| F140 | `citation-regex-was-blind-once` | The slug-citation check was blind once | settled | 2026-09-15 | A slug citation that names no pending record fails the build, and did not always. |
| F141 | `claim-ids-proved-twice` | The id claim ran clean twice | observed | 2026-09-15 | Claiming ids never moves an existing id, and always rewrites the citations it can. |
| F99 | `device-shots-first-run` | Device shots first run | observed | 2026-09-15 | The three widths and the two themes are measured, not assumed. |
| F142 | `hook-proved-with-15-payloads` | The shared-tree hook was proved on 15 payloads | observed | 2026-09-15 | A forbidden shared-tree command exits 2 before it runs, and a safe one does not. |
| F143 | `device-shots-check-catches-overflow-and-count` | The device-shots check has three outcomes | observed | 2026-09-16 | Every screen is measured at three widths and both themes, or the gap is a stated note. |
| F102 | `fetch-tab-state-lost` | Fetch tab navigated, first pass lost | observed | 2026-09-16 | A run fetches its data once, and leaves no tab parked on a dead link. |
| F144 | `netsuite-approval-note-confirmed` | NetSuite approval note confirmed | observed | 2026-09-16 | An approval note lands where the auditor will look for it. |
| F145 | `pending-id-checks-gate-main-and-citations` | Pending-id checks gate main and citations | observed | 2026-09-16 | No numbered record is claimed on a branch, and no citation stays unresolved after claiming. |
| F146 | `po-crosscheck-run-confirmed` | PO cross-check run confirmed | observed | 2026-09-16 | A correctly coded bill is never flagged as coded to the wrong purchase order. |
| F147 | `procore-missed-window-confirmed` | Procore missed window confirmed | observed | 2026-09-16 | A scheduled Procore window reviews the queue once, not repeatedly. |
| F103 | `version-line-silently-stale` | A version line can silently miss its bump | observed | 2026-09-16 | A teammate compares their installed version against the README table. |
| F148 | `waiter-loop-check-fires-on-defect` | The waiter-loop check fires on a real defect | observed | 2026-09-16 | No sentence in this repo instructs an unbounded wait-and-retry. |
| F149 | `onboarding-check-silent-on-missing-file` | The onboarding page check passed on a missing file | observed | 2026-09-18 | A missing `docs/onboarding.html` fails the build, per `D89`, the markdown compliance fix plan, ruling 3. |
| F150 | `review-only-dashboards-measured` | Review-only dashboards measured | observed | 2026-09-18 | A reviewer sees the whole queue, with no control they cannot use. |
| F151 | `browser-assumed-absent-in-cloud` | A session assumed no browser | observed | 2026-09-23 | A capability is measured before a run claims it cannot run. |
| F152 | `invalid-font-shorthand-dropped` | An invalid shorthand was dropped | observed | 2026-09-23 | A control renders in the font the template authored for it. |
| F153 | `toolbar-select-overflow` | Long option text overflows toolbar | observed | 2026-09-23 | A reader on a narrow panel is not made to scroll sideways. |
| pending | `commitment-payload-unread` | Commitment payload reported closed | observed | 2026-09-24 | A commitment's figures come from fields the payload really has. |
| pending | `dashboard-empty-context-strip` | Dashboard context strip arrives with text | observed | 2026-09-24 | A reviewer sees no blank grey block on a dashboard row. |
| pending | `dashboard-widget-host-confirmed` | Dashboard bar confirmed in widget host | observed | 2026-09-24 | The reader can see the item count and reach Filters wherever they are in the queue. |
| pending | `end-to-end-runs-routine` | End-to-end runs confirmed routine | observed | 2026-09-24 | A reviewer's verdicts come from a path somebody has watched work. |
| pending | `execute-button-blocked-state-confirmed` | Execute button blocked state confirmed | observed | 2026-09-24 | A blocked execute button reads as blocked, not as broken. |
| pending | `netsuite-browser-mode` | NetSuite browser mode confirmed | observed | 2026-09-24 | A teammate with no connector still gets a complete review. |
| pending | `no-guard-on-render-fallback` | No guard on the render fallback | observed | 2026-09-24 | A verdict the allowlist accepts always reaches its own branch on the dashboard, never the `clear` default. |
| pending | `pdf-geometry-line-math-confirmed` | PDF geometry line math confirmed | observed | 2026-09-24 | A quantity times rate check reads the invoice's real columns. |
| F154 | `plugin-skill-switch-off` | One plugin skill can be switched off | observed | 2026-09-24 | A teammate can switch off the work they cannot run, and keeps the work they can. |
| pending | `po-execute-route-confirmed` | Purchase order route reported working | observed | 2026-09-24 | A reviewed purchase order can be actioned, and only as the reviewer instructed. |
| pending | `procore-gate-fanout` | Procore gate fan-out confirmed solid | observed | 2026-09-24 | A live item is never logged as done because one request failed. |
| pending | `scheduled-runs-builtin-browser` | Scheduled runs drive the built-in browser | observed | 2026-09-24 | A scheduled run reaches the teammate's own signed-in session, not a separate, unsigned-in browser. |
