---
id: pending
slug: in-page-call-deadline
kind: decision
status: settled
date: 2026-10-09
---
# Every in-page call has a whole-call deadline

**Rule.** Every in-page fan-out in the Procore skill runs through `window.__deadline(tasks, ms, cap)`. It never rejects. A task that fails, is unfinished at `ms`, or never started is `failed`, never `empty`. Every `fetch` in the skill code carries `signal: AbortSignal.timeout(20000)`. A fetch timeout on an attachment is a named failed read, not `expired`, and is not retried. Step 3 names the previous-requisition read. After one browser call times out mid-run, the run calls `tabs_context_mcp` once. If that is also stuck, it stops and reports what finished. It never publishes a partial queue as complete.

**Outcome protected.** A run that hits a stuck call ends with a report of what finished. It does not hold the browser to the four-minute ceiling. It never publishes a partial queue as complete.

**Argument.**

The 2026-10-09 live Procore run (73 items) read a previous pay application in the page. The read never settled. `javascript_tool` held until the Claude in Chrome ceiling of about four minutes. The next two trivial calls, a one-line check and a tab close, also timed out.

Only the Step 2 gate fetch had a timeout. No step named the previous-requisition read, so the run improvised one with none.

A per-fetch timeout is not enough. A promise that never settles ignores it, and a queue behind a stuck worker never starts. The deadline sits on the whole call.

A restart clears a stuck call. It does not prevent the next one. Only the deadline and the stop rule do.

The stop rule is in the shared block `skill-chrome-first-call`, so NetSuite carries it too. NetSuite takes only the one line. Its fan-outs are unchanged.

**Evidence.**

- Incident: the 2026-10-09 live Procore run, 73 items.
- Related: D41, three states never a boolean. D27, retry only an expired link.

**Checks.** `scripts/test_skill_code.py`: `test_fetch_timeouts`, `test_deadline_helper`, `test_step3_previous_requisition`, `test_midrun_stop_rule`.
