Cut from `plugins/netsuite-approval-review/skills/netsuite-approval-double-check/assets/publish_dashboard.py` by review-only-mode. Verbatim; do not edit.

===== plugins/netsuite-approval-review/skills/netsuite-approval-double-check/assets/publish_dashboard.py line 7, sentence trim =====
was: (An earlier design published this to an artifact. That path was dropped on 2026-08-11: the
artifact host exposes no sendPrompt, so a dashboard there cannot put the execute instruction
into chat. The clipboard handoff still in dashboard_template.html is the deliberate fallback
for that host and is not leftover - do not remove it.)
now: (An earlier design published this to an artifact. That path was dropped on 2026-08-11: the
artifact host exposes no sendPrompt, so a dashboard there cannot put the re-run instruction
into chat. The clipboard handoff still in dashboard_template.html is the deliberate fallback
for that host and is not leftover - do not remove it.)
