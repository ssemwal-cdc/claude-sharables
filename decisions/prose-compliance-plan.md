---
id: pending
slug: prose-compliance-plan
kind: decision
status: open
date: 2026-09-15
title: Bring every markdown file into compliance with the global mandate
---

# Bring every markdown file into compliance with the global mandate

**Outcome protected.** A maintainer or a session reads one short rule, one record, or one
index. Nobody loads 147 KB to find a rule. Every rule names its argument. Every claim names its
measurement or says `unmeasured`.

**Scope of this pass.** The five maintainer and teammate markdown files: `CLAUDE.md`,
`prose.md`, `README.md`, and the two plugin `README.md` files. The two `SKILL.md` prompts are
deferred to their own pass (see Deferred below). Code, scripts, hooks and checks are deferred.
This is a prose redo.

## Decisions taken in the interview, 2026-09-15

| # | Decision | Chosen |
|---|---|---|
| 1 | Simplified Technical English scope | Every markdown file |
| 2 | Record storage | One file per record, one folder per kind |
| 3 | NetSuite browser-mode silence about skipped `core` checks | Keep silence. Record it as a named exception with its argument |
| 4 | Skill chat output shape | Out of scope. Skills run in teammate sessions, not under the mandate |
| 5 | `SKILL.md` prose and size | Deferred to a separate pass |
| 6 | Hooks and new checks | Deferred to a separate pass |
| 7 | Three widths, both themes | A usability check across devices, not a documentation exception. Deferred to the code pass |

## Target structure

```
CLAUDE.md            index. Rules as one line each, with a record id. Target: 150 lines or fewer.
decisions/           one file per decision. Filename is the slug.
findings/            one file per observed defect or measurement.
gaps/                one file per unobserved claim or unfired branch.
decisions/_index.md  id, slug, title, status, one line each. Same for findings/ and gaps/.
```

`prose.md` is removed. Its content moves to the three folders. `README.md` keeps its
teammate role and cites records by id.

### Record file format

```
---
id: pending            # slug only on a branch. Number claimed at merge.
slug: <kebab-case>
kind: decision | finding | gap
status: open | settled | superseded | abandoned | observed | unobserved
date: YYYY-MM-DD       # date of the observation or decision, not of the file
supersedes: <id>       # optional
---
# <title, five words or fewer>

**Rule.** One sentence. (decisions only)
**Outcome protected.** One sentence.
**Argument.** Short paragraphs. STE.
**Evidence.** Record ids, dates, figures. Say `unmeasured` where no figure exists.
**Checks.** The script or test that enforces it, or `none`.
```

### Ids and citation

- On a branch a record has `id: pending` and is cited as `D‹slug›, gloss`.
- At merge the maintainer names the act. The last commit on the branch claims the next
  number per kind (`D`, `F`, `G`), writes it into the frontmatter, and rewrites every
  `D‹slug›` citation to `D12`. The filename does not change.
- A citation is always `id, gloss`. Example: `D3, public repo`. Never a bare id. Never a path.
- Step ordinals inside a document are positions, not ids. They are not cited across files.

### Simplified Technical English house rules

1. One sentence carries one instruction or one fact. Target 20 words or fewer.
2. Imperative for rules. Active voice for facts.
3. No em-dash chains. No parenthetical asides. A second thought is a second sentence.
4. Figures as digits. Dates as ISO.
5. A rule is one line. Its argument lives in its record, not beside it.
6. A claim states its measurement or the word `unmeasured`.
7. Define a term at first use. Use the same term everywhere after.

## Migration map

### `CLAUDE.md` sections

| Lines | Section | Goes to |
|---|---|---|
| 12-53 | Org protocol does not apply here | `decisions/org-protocol-override` plus one index line |
| 57-188 | Adding a plugin, steps 1-7 | Index keeps the seven steps as one line each. Layout and manifest facts stay in the index. Each trap cited from step 6 becomes a finding |
| 190-268 | The prerequisite test | `decisions/prerequisite-bucket`. Index keeps the three-row pre-decided table |
| 272-303 | Two other files | Replaced by the three `_index.md` files |
| 305-434 | Shared blocks | `decisions/shared-blocks` plus `findings/dashboard-drift-six-defects`. Index keeps the two commands |
| 436-2091 | Traps | One finding per trap. About 60 records. The index keeps none of them |
| 2093-2166 | Versioning and version lines | `decisions/no-version-field`, `decisions/skill-version-lines`. Index keeps the four-site rule as one line |
| 2168-2206 | House conventions | One decision per convention. Index keeps one line each |
| 2208-2249 | Repo facts | Stays in the index. `decisions/public-repo` holds the argument |
| 2251-2272 | Do not | Stays in the index, each line citing its decision |
| 2274-2290 | Skill invocation | `findings/skill-invocation-verified` |

### `prose.md` sections

| Lines | Section | Goes to |
|---|---|---|
| 9-24 | What has not been verified yet | `gaps/_index.md` header |
| 26-170 | Folderless runs, Cowork storage | Three findings |
| 172-395 | Open decisions and deferrals | One decision per item, `status: open`. Each written as options plus recommendation |
| 397-828 | Gaps 0-12 | One gap per numbered item. `8a` becomes its own slug. Cleared items get `status: observed` |
| 830-1005 | Drift, staleness, actioned bin | Three findings |
| 1007-1164 | Audit, audit list, directions not taken | Two findings, one decision per direction with `status: abandoned` |
| 1166-1330 | Retrospectives and late notes | One finding each |

## Content fixes landed in the same pass

Each is a repo sentence that breaks a mandate sentence. Line numbers are as of `3775cc8`.

| File:line | Defect | Fix |
|---|---|---|
| `CLAUDE.md:1938` | "wait and re-check" is a waiter loop | Report `still propagating` once and end the round |
| `CLAUDE.md:146` | "Ignore it" discards a command's output | Record the warning as expected |
| `CLAUDE.md:2222` | "Do not propose going private" forbids the mandate's review move | Point at the argument in `decisions/public-repo` and invite challenge of the argument |
| `CLAUDE.md:259` | Multi-skill plugin is a documented standard the validator blocks | Mark the standard `unbuilt` in `gaps/` until the check is widened |
| `CLAUDE.md:1642, 2068` | Bare commit SHAs | Add a gloss to each |
| `CLAUDE.md:421` | Silence about skipped `core` checks | Keep. Record as `decisions/silent-connector-absence`, a named exception, argument attached |
| `README.md:162` | "enforces everything" is false. 2 of about 28 published strings are checked | State what `validate.py` checks. Say the rest is unchecked |
| `README.md:36` vs `:121` | Auto sync "leave checked" vs "off by default" | One statement, verified against the Add dialog |
| `README.md:34` vs `:86` | Cowork "works differently" vs "the same way" | Delete one |
| `README.md:99-100` vs plugin READMEs | Needs cells omit the workspace folder | Agree the three files |
| `netsuite README:68` | Workspace folder called a hard requirement. `prose.md:60-70` falsified that | Restate as recommended. Cite the finding |
| `netsuite README:9`, `README.md:99` | Purchase-order execute route published as working. Never fired | Add the gap marker |
| `procore README:15` | "75 items down to 32" has no date or source | Add date and finding id |
| `procore README:128-133`, `:78-88`, `:148-158` | Execute path, widget behaviour, CCO route stated as fact. All in the unobserved list | Add the gap marker to each |
| `.claude-plugin/marketplace.json` | NetSuite description omits purchase orders | Add them |
| all | Zero occurrences of `unmeasured` | Mark every unmeasured claim the audit listed |

## Deferred, recorded as open decisions

| Slug | Question | Recommendation |
|---|---|---|
| `skill-prose-pass` | Which mandate rules bind the two `SKILL.md` prompts, and do they split into a router plus `references/`? | Prose form and engineering rules bind. Output shape does not. Split |
| `hooks-and-checks-pass` | Install `.claude/settings.json` hooks and widen `validate.py` for prose-only rules? | Yes, after the prose pass lands |
| `device-usability-check` | Extend `scripts/measure_float.js` to capture 390, 1200 and 1600 px in light and dark for both dashboards and the onboarding sheet? | Yes, run by hand, images not committed |
| `xlsx-pin-target` | Name the first SheetJS version fixing the accepted CVEs. The NetSuite loader runs in an authenticated tab, so the session-less argument does not hold there | Name the target. Keep the pin until the `script-src` probe passes |

## Lanes

| Lane | Work | Files | Depends on |
|---|---|---|---|
| 1a | Records from `CLAUDE.md`. Rewrite `CLAUDE.md` as the index | `CLAUDE.md`, `decisions/`, `findings/` | none |
| 1b | Records from `prose.md`. Remove `prose.md`. Write the four deferred decisions | `prose.md`, `decisions/`, `findings/`, `gaps/` | none |
| 2 | README STE rewrite and the content fixes above. Cite records by `D‹slug›` | three `README.md`, `marketplace.json` description | reserved slugs below |
| 3 | Integration. Generate the three `_index.md` files from frontmatter. Claim ids at merge. Rewrite `‹slug›` citations to numbers | all | lanes 1a, 1b, 2 merged |

Lanes 1a, 1b and 2 run in parallel, each in its own worktree, and merge to the integration
branch `claude/eloquent-mccarthy-ji1fp1`. No lane writes an `_index.md`. Lane 3 generates them.

### Reserved slugs

A lane cites a reserved slug without checking that the file exists. The owning lane must create
it under exactly this name. A topic both source files cover has one owner.

| Slug | Kind | Owner | Source |
|---|---|---|---|
| `public-repo` | decision | 1a | `CLAUDE.md` Repo facts, `README.md` Distribution |
| `no-version-field` | decision | 1a | `CLAUDE.md` Versioning |
| `skill-version-lines` | decision | 1a | `CLAUDE.md` Skill version lines |
| `prerequisite-bucket` | decision | 1a | `CLAUDE.md` The prerequisite test |
| `git-subdir-sources` | decision | 1a | `CLAUDE.md` step 4 and Traps |
| `marketplace-name-vs-repo` | decision | 1a | `CLAUDE.md` Traps |
| `org-protocol-override` | decision | 1a | `CLAUDE.md` lines 12-53 |
| `shared-blocks` | decision | 1a | `CLAUDE.md` lines 305-434 |
| `workspace-folder-downloads` | decision | 1a | `CLAUDE.md` onboarding bullets |
| `approved-by-claude-comment` | decision | 1a | `CLAUDE.md` Traps |
| `silent-connector-absence` | decision | 1a | `CLAUDE.md` lines 415-430. Named exception, argument attached |
| `widget-not-artifact` | decision | 1a | `CLAUDE.md` Traps |
| `two-command-update` | finding | 1a | `CLAUDE.md` Traps |
| `restart-computer-not-app` | finding | 1a | `CLAUDE.md` onboarding bullets |
| `cco-holder-id-route` | finding | 1a | `CLAUDE.md` Traps, confirmed 2026-08-14 |
| `dashboard-drift-six-defects` | finding | 1b | `prose.md` 830-920 |
| `staleness-check-blind` | finding | 1b | `prose.md` 922-959 |
| `actioned-bin-never-rendered` | finding | 1b | `prose.md` 961-1005 |
| `folderless-run-works` | finding | 1b | `prose.md` 26-170. Falsifies the hard-requirement claim |
| `run-self-banned-login` | finding | 1b | `prose.md` 1273-1330 |
| `onboarding-copy-buttons` | finding | 1b | `prose.md` 1245-1271 |
| `no-end-to-end-run` | gap | 1b | `prose.md` gap 1 |
| `netsuite-notes-page` | gap | 1b | `prose.md` gap 2 |
| `freeze-fallback-unfired` | gap | 1b | `prose.md` gap 3 |
| `procore-gate-fanout` | gap | 1b | `prose.md` gap 5 |
| `netsuite-browser-mode` | gap | 1b | `prose.md` gap 7 |
| `write-never-attempted` | gap | 1b | `prose.md` gap 8a |
| `dashboard-widget-host-unseen` | gap | 1b | `prose.md` gap 9 |
| `commitment-payload-unread` | gap | 1b | `prose.md` gap 10 |
| `po-execute-route-unfired` | gap | 1b | `prose.md` gap 11 |
| `custom-tool-subtypes-unwatched` | gap | 1b | `prose.md` gap 12 |
| `pdf-geometry-mock-verified` | gap | 1b | `prose.md` 428-440 |
| `multi-skill-plugin-unbuilt` | gap | 1a | `CLAUDE.md` lines 256-268 |
| `skill-prose-pass` | decision, open | 1b | Deferred table above |
| `hooks-and-checks-pass` | decision, open | 1b | Deferred table above |
| `device-usability-check` | decision, open | 1b | Deferred table above |
| `xlsx-pin-target` | decision, open | 1b | Deferred table above |

Every other record takes a slug its owner chooses. Lane 1a owns every `CLAUDE.md` Trap not
listed here. Lane 1b owns every `prose.md` section not listed here. Where `CLAUDE.md` repeats a
1b topic, 1a cites the 1b slug and writes no record.

## Done when

- `python3 scripts/validate.py` is green. The index still names both plugins.
- `CLAUDE.md` is 150 lines or fewer. `prose.md` does not exist.
- `grep -rn "prose.md\|CLAUDE.md#\|see Step" *.md plugins/*/README.md` returns nothing.
- Every file under `decisions/`, `findings/`, `gaps/` has the frontmatter above.
- Every record is cited from an index or from another record.
- No sentence in the five files exceeds 30 words. Median is 20 or fewer. Measured by a
  scratch script and reported with the round, not committed.
- Every "blocks" and "should fix" line in the 2026-09-15 audit is closed or recorded as a gap.
- The four deferred decisions exist as records with `status: open`.

## Risks

- `validate.py:256-269` requires `CLAUDE.md` to name every registered plugin and to name no
  unregistered one. The index satisfies this. Records may name retired plugins. They live
  outside the checked files.
- Provenance ids in findings stay. Shipped examples keep placeholders. The rule is unchanged.
- Number claim at merge is a manual step until the checks pass exists. A duplicate number is
  possible with two concurrent merges. One maintainer merges, so the risk is accepted.
- The README STE rewrite changes teammate-facing text. Verify each install command against
  the live Add dialog before landing lane 2.
