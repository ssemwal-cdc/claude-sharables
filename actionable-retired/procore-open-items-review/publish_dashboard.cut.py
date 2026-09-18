Cut from `plugins/procore-open-items-review/skills/procore-open-items-review/assets/publish_dashboard.py` by review-only-mode. Verbatim; do not edit.

===== plugins/procore-open-items-review/skills/procore-open-items-review/assets/publish_dashboard.py lines 253-258 =====
    no_resp = [i["doc"] for i in items
               if i["verdict"] in ("clear", "flagged", "skipped") and not i["resp"]]
    if no_resp:
        print("WARNING: no response verbs captured for: " + ", ".join(no_resp) +
              " - those rows will offer no buttons. Capture available_responses "
              "from the workflow step.", file=sys.stderr)

===== plugins/procore-open-items-review/skills/procore-open-items-review/assets/publish_dashboard.py line 7, sentence trim =====
was: (An earlier design published this to an artifact. That path was dropped on 2026-08-11: the
artifact host exposes no sendPrompt, so a dashboard there cannot put the execute instruction
into chat. The clipboard handoff still in dashboard_template.html is the deliberate fallback
for that host and is not leftover - do not remove it.)
now: (An earlier design published this to an artifact. That path was dropped on 2026-08-11: the
artifact host exposes no sendPrompt, so a dashboard there cannot put the re-run instruction
into chat. The clipboard handoff still in dashboard_template.html is the deliberate fallback
for that host and is not leftover - do not remove it.)

===== plugins/procore-open-items-review/skills/procore-open-items-review/assets/publish_dashboard.py line 155, sentence trim =====
was:         # workflows/instances 400s on it, and the execute instruction reads "no instance" as
        # "already actioned elsewhere", so a live item would be silently logged as done.
now:         # workflows/instances 400s on it, so the gate can never be confirmed for that item.

===== plugins/procore-open-items-review/skills/procore-open-items-review/assets/publish_dashboard.py line 243, sentence trim =====
was:               "them respondable. It decides both the record link's collection and the type the "
              "execute step re-queries with, and the wrong one returns an empty instance rather "
              "than an error.")
now:               "them respondable. It decides the record link's collection, and the wrong one "
              "returns an empty instance rather than an error.")
