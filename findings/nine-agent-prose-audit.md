---
id: F61
slug: nine-agent-prose-audit
kind: finding
status: settled
date: 2026-08-24
---
# Nine agent prose audit

**Outcome protected.** The text closest to a real approve click is governed text.

**Argument.** Five auditors read the whole prose corpus cold.
They were deliberately given none of the session's conclusions.
They were told not to read git history.
Three debaters then contested the pooled findings.
Those positions were defence, prosecution and adjudication.

**The headline was a place nobody had looked: the composed execute message.**
It is the text closest to a real approve click.
It is the least-governed text in either plugin.
It is a JavaScript string inside an HTML template, covered by no shared block and read by no test.
Both copies had independently drifted into carrying procedure.
Both had got it wrong in the same week.
NetSuite's told the run to click the named button only.
That is the button rule Approve With Notes exists to override.
It then told the run to re-query the pending queue, which is the retired verification.
That verification invites a re-run that would approve twice.
Procore's carried its whole five-step ladder and omitted `per_page=100`.
Procore's own Step 2 records that omission converting a live workflow into an empty response.
Step 8 then reads that response as already actioned, and skips the item.

**A gap in that morning's own fix.** The new verdict allowlist caught a wrong verdict.
It did not catch a missing one.
`it.get("verdict", "clear")` defaulted an absent key to `clear` and sailed through the check.
Procore's sibling defaulted to `skipped`.
The fix removed the default entirely and let the allowlist abort.

**The staleness check added the previous turn was itself stale.**
Procore's Step 0 stated it ships `v5` and then tested for `v4`.
So the check written to detect a stale workspace would have called a current one stale.
It would have passed a genuinely stale one.
`check_template_versions()` missed it because `re.search` stops at the first match.
There were two sites.
It compares every site now.
That is the third instance of one shape: a check whose inputs fail together.
The checker only looked at one of them.

**Four things the interview corrected, and this is why the interview existed.**
Auditors reason from the documents, and the documents are not the system.
First, the panel asked whether NetSuite change orders should be executable at all.
The maintainer conflated Procore's CCO gate, which was resolved, with NetSuite's change orders.
NetSuite change orders carry no approval status and no next approver.
So they cannot be gated or confirmed that way.
Different systems used the same word, and the docs now distinguish them.
Second, the maintainer reports browser-mode execute works through Claude in Chrome.
That is a user report rather than an observed run.
It answers a narrower question than the panel asked, because the clicks landing is not the gate running.
Third, the maintainer believed the repo was enterprise-private.
The GitHub API says otherwise.
The judgment about sensitivity is theirs, and the premise was checkable and wrong.
Fourth, the precedence question resolved on two facts no auditor could have known.
Execute is always pressed in the session that ran the review.
The run is not watched.

**The generalisable lesson.** Every number a command regenerates was verified correct that day.
Almost every string a human retyped had drifted.
The corpus's defects cluster on hand-maintained text that no command reads.
That argues for extending mechanical checks into prose wherever a claim names an identifier.
Treat any unchecked string near a click as suspect by default.

**Evidence.** Audit dated 2026-08-24.
122 raw findings, 29 surviving contest.
`grep per_page plugins/` returned three hits, all in `SKILL.md`, none in the template.
The GitHub API reported `"private": false`, `"visibility": "public"`, forkable, personal account.
See D13, public is a decision.
F71, two inputs failing together, is the same shape one turn earlier.

**Checks.** `check_execute_prompt_purity()` in `scripts/shared_blocks.py`.
