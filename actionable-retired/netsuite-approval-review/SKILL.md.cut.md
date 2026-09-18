Cut from `plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md` by review-only-mode. Verbatim; do not edit.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md lines 12-16 =====
## Two modes

This skill does two different jobs. Know which one you are in:
- **Review mode**, Steps 1-7, is the default. It is read-only. It never clicks an approval button.
- **Execute mode**, Step 8, runs only on an explicit instruction naming specific documents. It clicks the real NetSuite buttons on the user's behalf. An instruction to review is never an instruction to execute. A verdict of `clear` is a recommendation and authorises nothing.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md lines 30-31 =====
- **Every approval carries the note `Approved by Claude`.** A note the user supplied for that document replaces it verbatim. Those two are the only text this skill types into a note field. Approvals route through Approve With Notes so the note can be attached. See Step 8. Do not ask permission for the default, and do not vary its wording.
- **A rejection reason always comes from the user.** Never default one.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md lines 164-164 =====
| 8 — gate and verify a click | query on bills and purchase orders, the record page on change orders | the record page, all three |

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md lines 578-578 =====
- per-item decision marking with local-storage persistence, and the batched execute bar

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md lines 595-598 =====

## Step 8 — Execute decisions (only on explicit instruction)

**Mandatory, before executing anything.** Read `${CLAUDE_PLUGIN_ROOT}/skills/netsuite-approval-double-check/references/step-8-execute.md` in full. Do not summarise it from memory or from this spine. Do not execute a single item until you have read that file this run.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md lines 608-609 =====

The tabs this skill opens are the record tabs. In Step 8's frozen-tab case, that also includes the fresh tab opened to read the approval state.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 16, sentence trim =====
was: Those three buttons sit adjacent at the top-left of every record, above Primary Information. In review mode, keep all clicks well away from that region.
now: Those three buttons sit adjacent at the top-left of every record, above Primary Information. Keep all clicks well away from that region.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 19, sentence trim =====
was: Treat the connector as read-only. Approvals go through the real UI, so the workflow routes and the trail records the user as the approver. A REST field flip would bypass SuiteFlow and leave no trail.
now: Treat the connector as read-only. This skill writes nothing to NetSuite, by any route.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 30, sentence trim =====
was: Never close a tab the user opened. See Step 9.
now: Never close a tab the user opened. See Step 8.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 34, sentence trim =====
was: Do not stall it over how an auditor might read it later. The `Approved by Claude` note keeps the trail honest about what performed the click. The checks that do matter are mechanical, and Step 8 has them. The document is still theirs to action.
now: Do not stall it over how an auditor might read it later. The document is still theirs to action.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 160, sentence trim =====
was: Attachment reading, every arithmetic check and every approval click are identical either way. pdf.js runs same-origin in the record tab, and approvals always go through the real UI.
now: Attachment reading and every arithmetic check are identical either way. pdf.js runs same-origin in the record tab.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 162, sentence trim =====
was: Never change that key. Doing so silently discards decisions the user has marked but not yet executed.
now: Never change that key. `D38`, never rename a marks key, holds even with nothing writing it.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 524, sentence trim =====
was: **`type` is required, and those three strings are the whole vocabulary.** They are also what Step 8's record-type table routes on. The two lists are gated against each other in the plugin repo. Write it on every item.
now: **`type` is required, and those three strings are the whole vocabulary.** Write it on every item.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 547, sentence trim =====
was: Handing the user a file or an artifact instead of attempting the render is a failure of this step. It is not a cautious alternative. It silently costs them one-click execute.
now: Handing the user a file or an artifact instead of attempting the render is a failure of this step. It is not a cautious alternative.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 576, sentence trim =====
was: Step 9 runs first, and the headline follows it.
now: Step 8 runs first, and the headline follows it.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md line 590, sentence trim =====
was: ## Step 9 — Close down
now: ## Step 8 — Close down
