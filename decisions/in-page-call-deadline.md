---
id: pending
slug: in-page-call-deadline
kind: decision
status: settled
date: 2026-10-09
---
# Every in-page call stops itself

**Rule.** Every in-page call in the Procore skill ends within about 60 to 90 seconds. Each fan-out in Steps 2 and 3, and each Step 4 read, runs through `window.__deadline(tasks, ms, cap)`. One `__deadline` runs per `javascript_tool` call. A task that fails, is unfinished at `ms`, or never started is `failed`, never `empty`. Every `fetch` carries `signal: AbortSignal.timeout(20000)`. An attachment read that times out is the seventh outcome, "support read timed out". It is never retried and never `clear` or `tied` (D27, retry only an expired link). Step 3 names the previous-requisition read. After one browser call times out mid-run, the run calls `tabs_context_mcp` once. If that is also stuck, it stops and reports what finished. A `__deadline` return where every task failed by timeout counts as a stuck call.

**Outcome protected.** A run that hits a stuck call ends with a report of what finished. It does not hold the browser to the four-minute ceiling. It never publishes a partial queue as complete.

**Argument.**

The 2026-10-09 live Procore run (73 items) read a previous pay application in the page. The read never settled. `javascript_tool` held until the Claude in Chrome ceiling of about four minutes. The next two trivial calls, a one-line check and a tab close, also timed out.

Only the Step 2 gate fetch had a timeout. No step named the previous-requisition read, so the run improvised one with none.

A per-fetch timeout is not enough. A promise that never settles ignores it, and a queue behind a stuck worker never starts. The deadline sits on the whole call.

Whether a restart clears a stuck call is unproven. The rule does not rely on it.

The stop rule is in the shared block `skill-chrome-first-call`, so NetSuite carries it too. Its `__deadline` clause has no effect there. NetSuite has no such helper, and its fan-outs are unchanged.

**Evidence.**

- Incident: the 2026-10-09 live Procore run, 73 items. The four-minute hold and the two later timeouts were seen. The cause of the stuck read is `unmeasured`.
- The 20-second limit is unmeasured against real payloads. See G`fetch-limit-includes-body`, the 20 second limit counts the body.
- Related: D41, three states never a boolean. D27, retry only an expired link.

**Checks.** `scripts/test_skill_code.py`: `test_fetch_timeouts`, `test_deadline_helper`, `test_step3_previous_requisition`, `test_midrun_stop_rule`, `test_retry_timeout_pairing`, `test_step4_dispatch_under_deadline`.
