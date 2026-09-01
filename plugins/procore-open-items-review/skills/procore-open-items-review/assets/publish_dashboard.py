#!/usr/bin/env python3
"""Publish the Procore open items dashboard.

Reads the review log beside this script, injects it into dashboard_template.html, and writes
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
TEMPLATE_VERSION = "v14"

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


#__SHARED:pub-payload-serialise__
def serialise(payload):
    """The data block, one compact line per item rather than a pretty-printed tree.

    Nothing reads this JSON by eye - the template parses it - so indentation buys nothing
    and costs both bytes and *lines*, and lines are what turned out to matter. Rendering
    the dashboard means reproducing the whole file through a tool call, so the file has to
    survive being read first, and a file that runs past a single read cannot be handed over
    byte for byte at all. Measured 2026-09-01 on a 62-item Procore queue: 174 KB over 2,834
    lines pretty-printed, past the 2,000-line default read, and the run refused to render
    it. The same payload compact-per-item is 886 lines and 6% smaller.

    Per item, not one blob: compacting the whole payload into a single line is 63 bytes
    smaller again and puts 110 KB on one line, trading the line count for a line long
    enough to be truncated on its own. One item per line is bounded on both axes - here
    the longest came to 1,774 characters.

    So this is load-bearing and not a style choice. Do not tidy it back to indent=.
    """
    parts = ['"%s":%s' % (k, json.dumps(v, ensure_ascii=False, separators=(",", ":")))
             for k, v in payload.items() if k != "items"]
    parts.append('"items":[\n%s\n]' % ",\n".join(
        json.dumps(i, ensure_ascii=False, separators=(",", ":"))
        for i in (payload.get("items") or [])))
    return "{" + ",".join(parts) + "}"
#__END_SHARED:pub-payload-serialise__

VERDICTS = ("clear", "flagged", "skipped", "ungated")
# The type the workflows/instances endpoint wants, which is NOT always the queue's item_type.
# A CCO's workflow hangs off the underlying commitment change order, not the package, and that
# object has its own id - carried per item as wfId. See Step 2 of SKILL.md.
# "com" has no single answer here: one kind covers PurchaseOrderContract and WorkOrderContract,
# and only the item's own wfType says which. This entry is the link's floor, not a gate default -
# a com with no wfType is demoted below rather than allowed to ride on it.
WF = {"icr": "GenericToolItem", "inv": "Billings::Requisition", "cco": "CommitmentChangeOrder",
      "com": "PurchaseOrderContract"}


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
    if not cfg.get("company"):
        sys.exit("ABORT: config.company missing from %s (your Procore company id). "
                 "Run the first-time setup before publishing." % os.path.basename(LOG))

    # A GenericToolItem belongs to a custom tool, and one queue can carry several of them -
    # observed 2026-09-01: Internal Change Risk (88) and Customer Change Request (77), the
    # second one 37 of 62 items and unknown to the config. config.customTools maps the queue's
    # item_subtype to that tool's id and its own cost-field mapping, because both differ per
    # tool. config.icrToolId is the floor for a config written before customTools existed,
    # where one tool really was all there was.
    tools = cfg.get("customTools") or {}
    floor = str(cfg.get("icrToolId", "") or "")
    if not tools and not floor:
        sys.exit("ABORT: neither config.customTools nor config.icrToolId is set in %s, so no "
                 "custom tool id is known and no change-risk record can be linked. Run the "
                 "first-time setup before publishing." % os.path.basename(LOG))

    items, bad, ungated, untyped, unmapped = [], [], [], [], []
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
        # Same shape one type along. A commitment's kind cannot say whether the workflow wants
        # PurchaseOrderContract or WorkOrderContract, and guessing is not safe: both are valid
        # workflowable types, so the wrong one with the right id returns 200 with zero rows rather
        # than a 400 - and Step 8 reads an empty instance as "already actioned elsewhere, skip it".
        # A live contract would be logged as done without a click. Fail closed instead.
        wf_type = str(it.get("wfType", "") or "")
        if kind == "com" and not wf_type:
            if verdict not in ("skipped", "ungated"):
                untyped.append(key)
            verdict = "ungated"
        # Which custom tool this item lives in decides its record link, and - through the cost
        # field mapping - which figures the ICR checks were able to read at all. Guessing is the
        # silent failure: a link built with the wrong tool id resolves to a page in the wrong
        # tool, and cost fields read from the wrong mapping are simply absent, which reads as a
        # blank field rather than as a check that never ran. So fail closed on both counts - no
        # link rather than a wrong one, and an item whose cost fields were never located cannot
        # be `clear`. Its response buttons are untouched: the workflow gate is per item and
        # independent of this, so responding is still safe. Only the reading is incomplete.
        subtype = str(it.get("subtype", "") or "")
        tool_id = ""
        if kind == "icr":
            tool_id = (str((tools.get(subtype) or {}).get("toolId", "") or "") if tools
                       else floor)
            if not tool_id:
                unmapped.append("%s (%s)" % (key, subtype or "no subtype recorded"))
                if verdict == "clear":
                    verdict = "skipped"
        items.append({
            "key": key,
            "id": str(it.get("itemId", "")),
            "pid": str(it.get("projectId", "")),
            "cid": str(it.get("commitmentId", "") or ""),
            "kind": kind,
            "subtype": subtype,
            "toolId": tool_id,
            "wf": wf_type or WF.get(kind, "GenericToolItem"),
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
            # The one field that evidences the verdict rather than asserting it. A list
            # here rather than NetSuite's single name: one Procore item can carry several
            # PCIs, each with its own attachment.
            "att": ", ".join(it.get("supportRead") or []),
        })

    if bad:
        sys.exit("ABORT: unknown verdict(s) - " + "; ".join(bad) +
                 ". Allowed: " + ", ".join(VERDICTS))

    if ungated:
        print("WARNING: no wfId, so demoted to ungated with no response buttons: " +
              ", ".join(ungated) + ". Resolve each one's commitment change order id "
              "from line_items[].holder.id on the package payload (Step 2) and "
              "re-publish to make them respondable.")

    if unmapped:
        print("WARNING: no custom tool mapped for: " + ", ".join(unmapped) +
              ". These rows render without an Open in Procore link, and any that were clear "
              "are demoted to skipped, because the cost fields the ICR checks read are mapped "
              "per tool and none was found for this subtype. Add the subtype to "
              "config.customTools with its toolId and costFields (Step 1) and re-publish. Do "
              "not point them at another tool's id - the link resolves to a real page in the "
              "wrong tool, which is indistinguishable from the right one.")

    if untyped:
        print("WARNING: no wfType on a commitment, so demoted to ungated with no response "
              "buttons: " + ", ".join(untyped) + ". Record the queue's item_type verbatim - "
              "PurchaseOrderContract or WorkOrderContract (Step 2) - and re-publish to make "
              "them respondable. It decides both the record link's collection and the type the "
              "execute step re-queries with, and the wrong one returns an empty instance rather "
              "than an error.")

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
        # icrToolId stays as the template's floor for items with no toolId of their own -
        # a render from a log written before subtypes were recorded. Per-item toolId wins.
        "config": {"company": str(cfg["company"]), "icrToolId": floor},
        "items": items,
    }

    a = tpl.index(S) + len(S)
    b = tpl.index(E)
    blob = serialise(payload)
    out = tpl[:a] + blob + tpl[b:]

    # the injected block must be the only difference
    assert len(out) - len(tpl) == len(blob) - (b - a)

    open(OUT, "w", encoding="utf-8").write(out)

    # A second, smaller file carrying only what the user can act on: items verdicted clear or
    # flagged, which are the ones with a cost and a response to give. Everything else becomes a
    # one-line row, and index.html keeps the complete record.
    #
    # Reached only when the template's integrity banner actually fires. There is no byte
    # threshold here, and the sentence that used to sit in this comment - "past roughly 90 KB
    # that stops being reliable" - was invented: nothing in show_widget documents a capacity,
    # and SKILL.md Step 7 calls a claim of exactly that form a prediction written as a fact. It
    # mattered because a run reads this file. On 2026-09-01 a 62-item queue was refused at
    # 164 KB, and the refusal was argued in this comment's own terms.
    #
    # It is also not a size fallback, measured: only two verdicts fold, so a live queue saves
    # 0-12%. A deliberately even 62-item fixture - half the queue foldable, which no real one is
    # - still only came down 129 KB from 174 KB. What made a large queue renderable was
    # serialise() above, not this.
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
                           ("key", "id", "pid", "cid", "kind", "subtype", "toolId", "wf",
                            "type", "doc", "vendor", "projLabel", "amt", "due", "verdict")})
    wpayload = dict(payload)
    wpayload["items"] = slim + folded
    wout = tpl[:a] + serialise(wpayload) + tpl[b:]
    WIDGET = os.path.join(os.path.dirname(os.path.abspath(OUT)), "widget.html")
    open(WIDGET, "w", encoding="utf-8").write(wout)
    print("wrote %s  (fallback only; %d KB vs %d KB full; %d actionable, %d folded)" % (
        WIDGET, len(wout) // 1024, len(out) // 1024, len(slim), len(folded)))

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
