---
id: G3
slug: cowork-storage-location-unverified
kind: gap
status: unobserved
date: 2026-08-26
---
# Cowork storage leads only

**Outcome protected.** A session reads a research note as leads, never as settled behaviour.

**Argument.** The maintainer objected that the folder requirement is a property of the prompt we wrote.
It is not a law.
Any other durable Cowork location could hold the state file instead.
Everything below is a community bug report on `anthropics/claude-code`.
None of it is Anthropic documentation.
`support.claude.com` is blocked by the sandbox egress proxy.
The primary source stayed unreadable.
These are reports of defects, so some may already be fixed.
Behaviour may differ by version and platform.
Treat them as leads to verify on a real machine.

A folderless session appears to write to a per-session area.
That explains a folderless run working while it re-interviews every time.
The state file is genuinely gone, not merely misplaced.

`~/Documents/Claude/` is reported as a hardcoded, stable Cowork path.
It is the candidate for durable state that needs no folder picked.
One report says the setup folder choice is ignored in favour of it.
That report is filed as a bug, so do not rely on the path staying.

One report calls scheduled tasks unusable for unattended automation.
It says permissions re-prompt on every run despite always-allow.
That does not hold here.
Scheduled runs of these plugins have worked several times.
They worked in the configuration the sheet already mandates.
That configuration is always-allow at the site prompt and permissions on Auto.
The two required settings may be what avoids the reported behaviour.
That reconciliation is inference, not established.
It makes the sheet's permissions instruction load-bearing rather than advisory.

A connected folder is not always actually connected.
One report shows a session with zero connected folders while the project UI shows one.
Output went silently to downloads.
That failure becomes visible only after the work is done.

The maintainer's point stands as a real option.
One reason against it has gone, because the permission re-prompt does not bite here.
The candidate path is still reported as hardcoded rather than supported.
One look at a real machine settles it, not more reading.
Check whether `Documents/Claude` exists there.
Check whether anything written into it survives a second run.
The payoff is smaller than the question suggests.
Scheduled runs work today with a folder.
Folderless and scheduled would still stop at the setup interview unless state persists.
Do not change the shipped scheduled prompt on the strength of this record.

**Method note.** Do not settle current behaviour from an issue tracker.
A maintainer observation contradicted a GitHub issue twice in one day.
It contradicted the issue on folderless runs working.
It contradicted the issue on scheduled permissions.
Issue trackers are self-selected for failure and stay open after fixes ship.
Use them to find candidate mechanisms.
Settle behaviour by watching it.

**Evidence.** 2026-08-26 research note.
Issue #47179, per-session output path under `AppData\Roaming\Claude`.
Issues #57177 and #54859, the hardcoded `~/Documents/Claude/` path.
Issue #47180, scheduled tasks re-prompting for permissions.
Issue #86647, a connected folder reporting as not connected.
No claim here is measured on a real machine. `unmeasured`.
F76, a folderless run completes, contradicts issue #47179 on usability.
F77, nothing lands in `Documents/Claude`.

**Checks.** none.
