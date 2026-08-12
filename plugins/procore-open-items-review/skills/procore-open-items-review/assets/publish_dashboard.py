#!/usr/bin/env python3
"""Publish the Procore open items dashboard.

Reads _review_log.json, injects it into dashboard_template.html, and writes
index.html ready to hand to update_artifact.

The template holds the entire layout and all behaviour. This script only ever
replaces the data block between the sentinels. Nothing here generates HTML, so
the dashboard cannot drift between runs.

Usage:  python3 publish_dashboard.py [<output path>]
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "_procore_review_log.json")
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

VERDICTS = ("clear", "flagged", "skipped", "ungated")
WF = {"icr": "GenericToolItem", "inv": "Billings::Requisition", "cco": "ChangeOrderPackage"}


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

    if tpl.count(S) != 1 or tpl.count(E) != 1:
        sys.exit("ABORT: template sentinels missing or duplicated. Do not "
                 "regenerate the template - restore it from the plugin assets and retry.")

    cfg = log.get("config") or {}
    for key, hint in (("company", "your Procore company id"),
                      ("icrToolId", "the tool_id of the change-risk custom tool")):
        if not cfg.get(key):
            sys.exit("ABORT: config.%s missing from _review_log.json (%s). "
                     "Run the first-time setup before publishing." % (key, hint))

    items, bad = [], []
    for key, it in (log.get("items") or {}).items():
        kind = it.get("kind", "icr")
        verdict = it.get("verdict", "skipped")
        if verdict not in VERDICTS:
            bad.append("%s has verdict %r" % (key, verdict))
        campus, bldg = split_project(it.get("project", ""))
        amt = it.get("amount", None)
        items.append({
            "key": key,
            "id": str(it.get("itemId", "")),
            "pid": str(it.get("projectId", "")),
            "cid": str(it.get("commitmentId", "") or ""),
            "kind": kind,
            "wf": WF.get(kind, "GenericToolItem"),
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
