Run the daily NetSuite approval double-check.

FIRST — idempotency gate. Read `NetSuite Approval Checks/_netsuite_review_log.json`
in the connected workspace folder. If `lastCompletedRun` equals today's date, a run
already succeeded today — stop immediately and output only: "Approval check already
completed today at <time>. Nothing to do." Do not open Chrome. Do not re-review
anything. If the file is missing or unreadable, treat that as "no run today" and
continue.

Otherwise, invoke the `netsuite-approval-double-check` skill and follow it end to
end. The skill owns the whole procedure. That covers the queue queries, how
attachments are read, the math and support-adequacy checks, and the cross-checks.
It also covers the state file and how the dashboard is published. It also covers
what to do when the connector or a session is unavailable, and which tabs to close.
This prompt restates none of its rules on purpose. Where anything here seems to
disagree with the skill, the skill wins.

On success, update the state file per the skill's schema, including today's date as
`lastCompletedRun` and the run time as `lastRunTime`.

Then report in chat with one line, in this exact shape:

```
<n> pending · <n> flagged · dashboard updated
```

Add a second line only if something blocked the run. Do not put per-item
verdicts in chat.

If the run fails partway, do NOT set `lastCompletedRun`. Leave it so the next
fallback window retries. The one exception: the skill says the blocker will
not clear on its own. Report what blocked it.
