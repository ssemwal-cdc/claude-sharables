#!/usr/bin/env python3
"""Publish the NetSuite approval queue dashboard.

Reads the review log beside this script, injects it into dashboard_template.html, and writes
index.html, whose contents are then rendered inline with show_widget.

(An earlier design published this to an artifact. That path was dropped on 2026-08-11: the
artifact host exposes no sendPrompt, so a dashboard there cannot put the execute instruction
into chat. The clipboard handoff still in dashboard_template.html is the deliberate fallback
for that host and is not leftover - do not remove it.)

The template holds the entire layout and all behaviour. This script only ever
replaces the data block between the sentinels. Nothing here regenerates HTML,
so the dashboard cannot drift between runs.

Usage:  python3 publish_dashboard.py [<output path>]
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "_netsuite_review_log.json")
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
TEMPLATE_VERSION = "v12"

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


# The only two verdicts this review produces (Step 6 of SKILL.md). An unknown value used to
# fall straight through the template's pill logic into "Clear" - a fail-open on the one field
# that decides what gets approved - so it aborts the publish instead. Procore's script has
# had this guard since it shipped; this side never got it.
VERDICTS = ("clear", "flagged")


def main():
    log = json.load(open(LOG, encoding="utf-8"))
    tpl = open(TPL, encoding="utf-8").read()

    # Warns on a stale workspace copy; deliberately does not stop the run.
    check_template_version(tpl)

    if tpl.count(S) != 1 or tpl.count(E) != 1:
        sys.exit("ABORT: template sentinels missing or duplicated. Do not "
                 "regenerate the template - restore it and retry.")

    items, bad = [], []
    for tid, it in log.get("items", {}).items():
        # No default. The allowlist below catches a WRONG verdict but a MISSING one used to
        # default to "clear" and sail through it - fail-open on the field that decides what gets
        # approved. Procore's sibling defaults to "skipped", i.e. non-actionable; the equivalent
        # here is to have no default at all and let the allowlist abort.
        verdict = it.get("verdict") or ""
        if verdict not in VERDICTS:
            bad.append("%s has verdict %r" % (tid, verdict))
        items.append({
            "id": int(tid),
            "type": it.get("type", "Bill"),
            "doc": it.get("docNo", ""),
            "vendor": it.get("vendor", ""),
            "amt": abs(float(it.get("amount", 0) or 0)),
            "trandate": it.get("trandate", ""),
            "verdict": verdict,
            "head": it.get("head", ""),
            "facts": it.get("facts", []),
            "po": it.get("poContext", ""),
            "poWarn": it.get("poWarning", ""),
            # The PO the bill is actually applied to, resolved from the transaction
            # linkage - never from the typed custbody3 reference. poLink says which of
            # linked/unlinked/failed produced it, so the dashboard can never present an
            # unconfirmed PO as confirmed.
            "poRef": it.get("poRef", ""),
            "poLink": it.get("poLink", ""),
            "detail": it.get("detail", ""),
            # The one field that evidences the verdict rather than asserting it. Rendered
            # inside Show detail, so a clear item can be asked what was actually read.
            "att": it.get("attachmentFile", ""),
        })

    if bad:
        sys.exit("ABORT: unknown verdict(s) - " + "; ".join(bad) +
                 ". Allowed: " + ", ".join(VERDICTS))

    order = {"flagged": 0, "clear": 1}
    items.sort(key=lambda i: (order.get(i["verdict"], 2), -i["amt"]))

    missing = [i["doc"] for i in items if not i["head"] or not i["facts"]]
    if missing:
        print("WARNING: no head/facts for: " + ", ".join(missing) +
              " - these rows will render thin", file=sys.stderr)

    cfg = log.get("config") or {}
    # `account` builds every record URL, so it is required on both routes. `me` and `tool` are
    # connector-only: Step 0 omits them in browser mode by design, because the bill portlets are
    # per-user saved searches already scoped to whoever is signed in, so there is no id to
    # configure and nothing to confuse with someone else's. Requiring all three unconditionally
    # made the documented no-connector route impossible to finish - the review completed and then
    # aborted, telling the user to redo a first-run setup they had done correctly.
    required = [("account", "the NetSuite account id")]
    if cfg.get("mode") == "connector" or cfg.get("tool"):
        required += [("me", "your NetSuite employee internal id"),
                     ("tool", "the NetSuite connector tool name")]
    for key, hint in required:
        if not cfg.get(key):
            # Name the file that is actually read; the literal used to say _review_log.json,
            # which is only the pre-migration name, so it sent people to a file that is not there.
            sys.exit("ABORT: config.%s missing from %s (%s). "
                     "Run the first-time setup before publishing - never fall back "
                     "to another person's identity." % (key, os.path.basename(LOG), hint))

    payload = {
        "lastRun": log.get("lastRunTime") or log.get("lastCompletedRun", ""),
        "lastRunISO": log.get("lastRunISO", "") or (
            (log.get("lastRunTime") or "").replace(" ", "T")),
        "config": {"me": cfg.get("me", ""), "tool": cfg.get("tool", ""),
                   "account": cfg["account"]},
        "items": items,
    }

    a = tpl.index(S) + len(S)
    b = tpl.index(E)
    out = tpl[:a] + json.dumps(payload, ensure_ascii=False, indent=1) + tpl[b:]

    # the injected block must be the only difference
    assert len(out) - len(tpl) == len(json.dumps(payload, ensure_ascii=False, indent=1)) - (b - a)

    open(OUT, "w", encoding="utf-8").write(out)

    #__SHARED:pub-render-archive__
    # Keep a short rolling archive of what was actually rendered. Two uses: diff a bad render
    # against the last good one to see what changed, and re-render from disk without re-running
    # the whole review, which costs a fresh queue read and re-reading every attachment.
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
    flagged = sum(1 for i in items if i["verdict"] == "flagged")
    print("wrote %s" % OUT)
    print("%d items (%d flagged) as of %s" % (len(items), flagged, payload["lastRun"]))
    print("headline: %d pending · %d flagged · dashboard updated" % (len(items), flagged))
    if cfg.get("tool"):
        print("identity: employee %s via %s" % (cfg["me"], cfg["tool"]))
    else:
        print("identity: browser route, portlet-scoped queue (no connector)")

if __name__ == "__main__":
    main()
