Cut from `plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md` by review-only-mode. Verbatim; do not edit.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md lines 9-12 =====
## Two modes
- **Review mode**, Steps 1 to 7, is the default. It is read-only. It never clicks Respond.
- **Execute mode**, Step 8, runs only on an explicit instruction naming specific items.
- An instruction to review is never an instruction to execute. A verdict of `clear` authorises nothing.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md lines 18-18 =====
- Send every response through the real UI, so the audit trail records the user.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md lines 23-23 =====
- A dashboard is a snapshot, not a live view. Re-verify each item before any click. See Step 8.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md lines 25-27 =====
- Every affirmative response carries the comment `Approved by Claude`.
- A comment the user supplied for that item replaces it verbatim. Those two strings are the only text this skill writes into a comment box.
- Do not ask permission for the default comment. Do not vary its wording.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md lines 42-42 =====
- The `Approved by Claude` comment keeps the trail honest about what performed the click. Step 8 still stops the batch: the item is still theirs, the figures match, the response is offered.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md lines 442-442 =====
- Items where `can_respond` is `false` are **suppressed**, not skipped. They collapse to a single count.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md lines 523-525 =====
## Step 8 — Execute responses, only on explicit instruction

**Mandatory, before executing anything.** Read `${CLAUDE_PLUGIN_ROOT}/skills/procore-open-items-review/references/step-8-execute.md` in full. Do not summarise it from memory or from this spine. Do not execute a single item until you have read that file this run.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 12, sentence trim =====
was: - In review mode keep clicks away from the orange Respond button and the orange Edit button.
now: - Keep clicks away from the orange Respond button and the orange Edit button.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 14, sentence trim =====
was: - Every Procore call in review mode is a GET. Never POST, PUT, PATCH or DELETE.
now: - Every Procore call this skill makes is a GET. Never POST, PUT, PATCH or DELETE.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 24, sentence trim =====
was: Never close a tab the user opened. See Step 9.
now: Never close a tab the user opened. See Step 8.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 151, sentence trim =====
was: An empty response is `empty`, and Step 8 reads `empty` as already actioned elsewhere. So a page-size default silently converts actionable items into ones logged as done. Always send it.
now: An empty response is `empty`, and a page-size default silently converts a live instance into one. Always send it.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 201, sentence trim =====
was: A right type with the wrong *id* returns **200 with zero rows**, which Step 8 reads as already actioned.
now: A right type with the wrong *id* returns **200 with zero rows**, which reads as no instance at all.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 435, sentence trim =====
was: - **An unmapped subtype loses its record link and a `clear` becomes `skipped`. It keeps its response buttons.**
now: - **An unmapped subtype loses its record link and a `clear` becomes `skipped`.**

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 437, sentence trim =====
was: - **A commitment with no `wfType` loses its buttons.** That is because the wrong collection returns 200 with zero rows, which Step 8 reads as already actioned.
now: - **A commitment with no `wfType` is demoted to `ungated`.** The wrong collection returns 200 with zero rows, so the gate is never confirmed.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 487, sentence trim =====
was: A truncated render costs one turn and a re-render, while declining to try costs the user one-click execute.
now: A truncated render costs one turn and a re-render.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 513, sentence trim =====
was: Step 9 runs first, and the headline follows it.
now: Step 8 runs first, and the headline follows it.

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 515, sentence trim =====
was: ## Step 9 — Close down
now: ## Step 8 — Close down

===== plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md line 524, sentence trim =====
was: The tabs this skill opens are the fetch tab, the carrier tabs and the pdf.js tab. Step 2 and Step 8 also open the record tabs.
now: The tabs this skill opens are the fetch tab, the carrier tabs and the pdf.js tab. Step 2 also opens the record tabs.
