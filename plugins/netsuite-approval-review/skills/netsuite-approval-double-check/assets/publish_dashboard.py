#!/usr/bin/env python3
"""Publish the NetSuite approval queue dashboard.

Reads _review_log.json, injects it into dashboard_template.html, and writes
index.html ready to hand to update_artifact.

The template holds the entire layout and all behaviour. This script only ever
replaces the data block between the sentinels. Nothing here regenerates HTML,
so the dashboard cannot drift between runs.

Usage:  python3 publish_dashboard.py [<output path>]
"""
import json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "_review_log.json")
TPL = os.path.join(HERE, "dashboard_template.html")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html")

S, E = "/*__REVIEW_DATA__*/", "/*__END__*/"

def main():
    log = json.load(open(LOG, encoding="utf-8"))
    tpl = open(TPL, encoding="utf-8").read()

    if tpl.count(S) != 1 or tpl.count(E) != 1:
        sys.exit("ABORT: template sentinels missing or duplicated. Do not "
                 "regenerate the template - restore it and retry.")

    items = []
    for tid, it in log.get("items", {}).items():
        items.append({
            "id": int(tid),
            "type": it.get("type", "Bill"),
            "doc": it.get("docNo", ""),
            "vendor": it.get("vendor", ""),
            "amt": abs(float(it.get("amount", 0) or 0)),
            "trandate": it.get("trandate", ""),
            "verdict": it.get("verdict", "clear"),
            "head": it.get("head", ""),
            "facts": it.get("facts", []),
            "po": it.get("poContext", ""),
            "poWarn": it.get("poWarning", ""),
            "detail": it.get("detail", ""),
        })

    order = {"flagged": 0, "clear": 1}
    items.sort(key=lambda i: (order.get(i["verdict"], 2), -i["amt"]))

    missing = [i["doc"] for i in items if not i["head"] or not i["facts"]]
    if missing:
        print("WARNING: no head/facts for: " + ", ".join(missing) +
              " - these rows will render thin", file=sys.stderr)

    cfg = log.get("config") or {}
    for key, hint in (("me", "your NetSuite employee internal id"),
                      ("tool", "the NetSuite connector tool name"),
                      ("account", "the NetSuite account id")):
        if not cfg.get(key):
            sys.exit("ABORT: config.%s missing from _review_log.json (%s). "
                     "Run the first-time setup before publishing - never fall back "
                     "to another person's identity." % (key, hint))

    payload = {
        "lastRun": log.get("lastRunTime") or log.get("lastCompletedRun", ""),
        "config": {"me": cfg["me"], "tool": cfg["tool"], "account": cfg["account"]},
        "items": items,
    }

    a = tpl.index(S) + len(S)
    b = tpl.index(E)
    out = tpl[:a] + json.dumps(payload, ensure_ascii=False, indent=1) + tpl[b:]

    # the injected block must be the only difference
    assert len(out) - len(tpl) == len(json.dumps(payload, ensure_ascii=False, indent=1)) - (b - a)

    open(OUT, "w", encoding="utf-8").write(out)
    flagged = sum(1 for i in items if i["verdict"] == "flagged")
    print("wrote %s" % OUT)
    print("%d items (%d flagged) as of %s" % (len(items), flagged, payload["lastRun"]))
    print("headline: %d pending · %d flagged · dashboard updated" % (len(items), flagged))
    print("identity: employee %s via %s" % (cfg["me"], cfg["tool"]))

if __name__ == "__main__":
    main()
