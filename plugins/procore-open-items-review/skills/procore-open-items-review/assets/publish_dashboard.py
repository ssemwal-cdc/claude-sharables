#!/usr/bin/env python3
"""Publish the Procore open items dashboard.

Reads _review_log.json, injects it into dashboard_template.html, and writes
index.html, whose contents are then rendered inline with show_widget.

(An earlier design published this to an artifact. That path was dropped on 2026-08-11: the
artifact host exposes no sendPrompt, so a dashboard there cannot put the execute instruction
into chat. The clipboard handoff still in dashboard_template.html is the deliberate fallback
for that host and is not leftover - do not remove it.)

The template holds the entire layout and all behaviour. This script only ever
replaces the data block between the sentinels. Nothing here generates HTML, so
the dashboard cannot drift between runs.

Usage:  python3 publish_dashboard.py [<output path>]
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "_procore_review_log.json")
#__SHARED:pub-log-migration__
_LEGACY = os.path.join(HERE, "_review_log.json")
# Both skills used to name this file _review_log.json, differing only by parent folder,
# with both folders under the same Downloads parent. An agent resolving it by bare name
# could read or write the other system's state - which happened. Distinct names make that
# impossible rather than unlikely. Migrate in place on first sight of the old name.
if not os.path.exists(LOG) and os.path.exists(_LEGACY):
    try:
        os.rename(_LEGACY, LOG)
    except OSError:
        LOG = _LEGACY  # cloud-synced folders can refuse the move; keep working
TPL = os.path.join(HERE, "dashboard_template.html")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html")

S, E = "/*__REVIEW_DATA__*/", "/*__END__*/"

# The template is a *cache* in the workspace folder, refreshed by the skill's Step 0. When
# that sync cannot run - the Cowork sandbox does not mount the plugin directory - the copy
# here silently lags the installed plugin, and a missing feature reads as a design choice.
# So the template carries a version marker and this script checks it.
#
# Warn, never abort. A lagging template still renders correct verdicts: the review procedure
# ships in SKILL.md with the plugin, and only the layout can fall behind. Aborting would kill
# a run that is fine.
#__END_SHARED:pub-log-migration__
TEMPLATE_VERSION = "v6"

#__SHARED:pub-version-check__
def check_template_version(tpl):
    m = re.search(r"layout template (v\d+)", tpl)
    found = m.group(1) if m else None
    if found == TEMPLATE_VERSION:
        return
    print("WARNING: dashboard template is %s, this script expects %s - the workspace copy is "
          "stale and Step 0's sync did not run. Re-sync from a surface whose shell can see the "
          "plugin, or this dashboard will be missing recent changes."
          % (found or "unversioned", TEMPLATE_VERSION), file=sys.stderr)
#__END_SHARED:pub-version-check__


VERDICTS = ("clear", "flagged", "skipped", "ungated")
# The type the workflows/instances endpoint wants, which is NOT always the queue's item_type.
# A CCO's workflow hangs off the underlying commitment change order, not the package, and that
# object has its own id - carried per item as wfId. See Step 2 of SKILL.md.
WF = {"icr": "GenericToolItem", "inv": "Billings::Requisition", "cco": "CommitmentChangeOrder"}


def split_project(name):
    """Procore names projects '<Campus> - <Building>'. Campus is the outer axis:
    every campus has its own Building 1, so a bare building name collides across
    campuses. A campus-level item becomes 'Campus-wide'."""
    if not name:
        return ("", "")
    parts = re.split(r"\s+-\s+", name, maxsplit=1)
    if len(parts) == 2:
        campus, bldg = parts[0].strip(), parts[1].strip()
    else:
        campus, bldg = parts[0].strip(), "Campus-wide"
    if bldg.lower() in ("campus", "campus-wide", ""):
        bldg = "Campus-wide"
    return (campus, bldg)


def main():
    log = json.load(open(LOG, encoding="utf-8"))
    tpl = open(TPL, encoding="utf-8").read()

    # Warns on a stale workspace copy; deliberately does not stop the run.
    check_template_version(tpl)

    if tpl.count(S) != 1 or tpl.count(E) != 1:
        sys.exit("ABORT: template sentinels missing or duplicated. Do not "
                 "regenerate the template - restore it from the plugin assets and retry.")

    cfg = log.get("config") or {}
    for key, hint in (("company", "your Procore company id"),
                      ("icrToolId", "the tool_id of the change-risk custom tool")):
        if not cfg.get(key):
            sys.exit("ABORT: config.%s missing from _review_log.json (%s). "
                     "Run the first-time setup before publishing." % (key, hint))

    items, bad, ungated = [], [], []
    for key, it in (log.get("items") or {}).items():
        kind = it.get("kind", "icr")
        verdict = it.get("verdict", "skipped")
        if verdict not in VERDICTS:
            bad.append("%s has verdict %r" % (key, verdict))
        campus, bldg = split_project(it.get("project", ""))
        amt = it.get("amount", None)
        # A CCO can only be gated through its commitment change order id. Without one there is no
        # query that works, and guessing the package id is worse than not offering the buttons:
        # workflows/instances 400s on it, and the execute instruction reads "no instance" as
        # "already actioned elsewhere", so a live item would be silently logged as done.
        wf_id = str(it.get("wfId", "") or "")
        if kind == "cco" and not wf_id:
            if verdict not in ("skipped", "ungated"):
                ungated.append(key)
            verdict = "ungated"
        items.append({
            "key": key,
            "id": str(it.get("itemId", "")),
            "pid": str(it.get("projectId", "")),
            "cid": str(it.get("commitmentId", "") or ""),
            "kind": kind,
            "wf": it.get("wfType") or WF.get(kind, "GenericToolItem"),
            "wfId": wf_id or str(it.get("itemId", "")),
            "type": it.get("type", kind.upper()),
            "doc": it.get("docNo", ""),
            "vendor": it.get("counterparty", ""),
            "campus": campus,
            "bldg": bldg,
            "projLabel": ("%s · %s" % (campus, bldg)).strip(" ·"),
            "amt": (abs(float(amt)) if amt not in (None, "") else None),
            "due": it.get("dueDate") or None,
            "step": it.get("step", ""),
            "resp": it.get("responses", []) if verdict != "ungated" else [],
            "verdict": verdict,
            "head": it.get("head", ""),
            "facts": it.get("facts", []),
            "po": it.get("context", ""),
            "poWarn": it.get("warning", ""),
            "detail": it.get("detail", ""),
        })

    if bad:
        sys.exit("ABORT: unknown verdict(s) - " + "; ".join(bad) +
                 ". Allowed: " + ", ".join(VERDICTS))

    if ungated:
        print("WARNING: no wfId, so demoted to ungated with no response buttons: " +
              ", ".join(ungated) + ". Resolve each one's commitment change order id "
              "from line_items[].holder.id on the package payload (Step 2) and "
              "re-publish to make them respondable.")

    thin = [i["doc"] for i in items if not i["head"] or not i["facts"]]
    if thin:
        print("WARNING: no head/facts for: " + ", ".join(thin) +
              " - these rows will render thin", file=sys.stderr)

    no_resp = [i["doc"] for i in items
               if i["verdict"] in ("clear", "flagged", "skipped") and not i["resp"]]
    if no_resp:
        print("WARNING: no response verbs captured for: " + ", ".join(no_resp) +
              " - those rows will offer no buttons. Capture available_responses "
              "from the workflow step.", file=sys.stderr)

    payload = {
        "lastRun": log.get("lastRunTime") or log.get("lastCompletedRun", ""),
        "lastRunISO": log.get("lastRunISO", "") or (
            (log.get("lastRunTime") or "").replace(" ", "T")),
        "suppressed": log.get("suppressed", 0),
        "config": {"company": str(cfg["company"]), "icrToolId": str(cfg["icrToolId"])},
        "items": items,
    }

    a = tpl.index(S) + len(S)
    b = tpl.index(E)
    blob = json.dumps(payload, ensure_ascii=False, indent=1)
    out = tpl[:a] + blob + tpl[b:]

    # the injected block must be the only difference
    assert len(out) - len(tpl) == len(blob) - (b - a)

    open(OUT, "w", encoding="utf-8").write(out)

    # A widget carries its HTML inline through a tool call, so the whole dashboard has to be
    # reproduced byte for byte to render. Past roughly 90 KB that stops being reliable and the
    # render gets refused, which costs one-click execute entirely. So write a second, smaller
    # file carrying only what the user can actually act on: items with a verdict of clear or
    # flagged, which are the ones with a cost and a response to give. Everything else becomes a
    # count and a one-line row, and index.html keeps the complete record.
    ACTIONABLE = ("clear", "flagged")
    slim, folded = [], []
    for i in items:
        if i.get("verdict") in ACTIONABLE:
            slim.append(i)
        else:
            # display-only: enough for a one-line row and a link, nothing more. No resp, so
            # they carry no buttons here - an item with no cost at a step that demands one is
            # not something to action from a trimmed view. index.html keeps the full record.
            folded.append({k: i.get(k) for k in
                           ("key", "id", "pid", "cid", "kind", "wf", "type", "doc", "vendor",
                            "projLabel", "amt", "due", "verdict")})
    wpayload = dict(payload)
    wpayload["items"] = slim + folded
    wout = tpl[:a] + json.dumps(wpayload, ensure_ascii=False, indent=1) + tpl[b:]
    WIDGET = os.path.join(os.path.dirname(os.path.abspath(OUT)), "widget.html")
    open(WIDGET, "w", encoding="utf-8").write(wout)
    print("wrote %s  (fallback only; %d KB vs %d KB full; %d actionable, %d folded)" % (
        WIDGET, len(wout) // 1024, len(out) // 1024, len(slim), len(folded)))

    #__SHARED:pub-render-archive__
    # Keep a short rolling archive of what was actually rendered. Two uses: diff a bad render
    # against the last good one to see what changed, and re-render from disk without re-running
    # the whole review, which costs connector queries and attachment downloads.
    #
    # Seven weekday slots, overwritten in place, rather than dated files. The workspace folder is
    # usually cloud-synced, where creating and overwriting work but deleting is typically blocked,
    # so anything that accumulates can never be cleaned up. Best-effort: never fail a publish.
    try:
        arc = os.path.join(HERE, "renders")
        os.makedirs(arc, exist_ok=True)
        slot = datetime.date.today().strftime("%a").lower()
        with open(os.path.join(arc, slot + ".html"), "w", encoding="utf-8") as fh:
            fh.write(out)
    except OSError as exc:
        print("note: render archive not written (%s)" % exc, file=sys.stderr)
    #__END_SHARED:pub-render-archive__

    n = len(items)
    flagged = sum(1 for i in items if i["verdict"] == "flagged")
    skipped = sum(1 for i in items if i["verdict"] == "skipped")
    ungated = sum(1 for i in items if i["verdict"] == "ungated")
    print("wrote %s" % OUT)
    print("%d items (%d flagged, %d skipped, %d ungated) as of %s"
          % (n, flagged, skipped, ungated, payload["lastRun"]))
    print("headline: %d awaiting you · %d flagged · %d skipped · dashboard updated"
          % (n, flagged, skipped))
    print("suppressed (cannot respond): %s" % payload["suppressed"])


if __name__ == "__main__":
    main()
