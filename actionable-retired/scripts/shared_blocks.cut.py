Cut from `scripts/shared_blocks.py` by review-only-mode. Verbatim; do not edit.

===== scripts/shared_blocks.py lines 288-302 =====
# Tokens that mean the composed execute message has started specifying PROCEDURE rather than
# authority. Each one is drawn from a real defect: the endpoint/parameter forms because Procore's
# prompt omitted per_page=100 from a gate query it had no business carrying, the verification
# verbs because NetSuite's prompt shipped the retired queue re-query that CLAUDE.md says invites
# a double approval, and the button rule because it contradicted Step 8's Approve With Notes
# routing. Identifiers the agent needs in order to FIND a record are fine and deliberately absent
# from this list; query shapes and verification methods are not.
PROCEDURE_TOKENS = (
    "per_page", "page=", "view=action_card", "filters[", "GET /", "/rest/v",
    "re-query", "approvalstatus", "available_responses", "can_respond",
    "workflows/instances", "click the named button", "the named button only",
)
PROMPT_STMT = re.compile(r"^  var prompt\s*=(.*?);\s*$", re.M | re.S)



===== scripts/shared_blocks.py lines 346-391 =====
def check_execute_prompt_purity():
    """The message the Execute button posts into chat authorises; it must not also specify.

    This is the least-governed text in either plugin - a JavaScript string inside an HTML
    template, read by no test and covered by no shared block - and it is the text closest to a
    real approve click. Both copies independently drifted into carrying procedure, and both got
    it wrong in the same week: NetSuite's contradicted Step 8, Procore's omitted one of its
    gates. Settled with the maintainer 2026-08-24: Step 8 is the specification, the prompt is
    the authorisation, and they may not overlap. Execute is always pressed in the session that
    ran the review, so the skill is in context; the run is unwatched, which is the reason the
    gates belong in the governed text rather than here.
    """
    problems = []
    for entry in sorted(os.listdir(PLUGINS)):
        if entry.startswith("_"):
            continue
        skills = os.path.join(PLUGINS, entry, "skills")
        if not os.path.isdir(skills):
            continue
        for skill in sorted(os.listdir(skills)):
            tpl = os.path.join(skills, skill, "assets", "dashboard_template.html")
            if not os.path.isfile(tpl):
                continue
            with open(tpl, encoding="utf-8") as fh:
                body = fh.read()
            m = PROMPT_STMT.search(body)
            if not m:
                problems.append("%s/%s: dashboard_template.html has no recognisable "
                                "`var prompt = ...;` statement to check" % (entry, skill))
                continue
            stmt = m.group(1)
            for tok in PROCEDURE_TOKENS:
                if tok in stmt:
                    problems.append(
                        "%s/%s: the composed execute message contains %r - that is procedure, "
                        "and procedure belongs in SKILL.md Step 8, never in this string. It is "
                        "read by no test and is the text closest to a real click."
                        % (entry, skill, tok))
            if "Step 8" not in stmt:
                problems.append(
                    "%s/%s: the composed execute message must point at Step 8 of the skill as "
                    "the procedure - without that pointer it is an authorisation with no "
                    "specification attached." % (entry, skill))
    return problems



===== scripts/shared_blocks.py lines 552-663 =====
# Every record type a skill's queue may contain, which is also every type its execute step
# must be able to act on. Hardcoded for the same reason as REGISTRY_MANIFEST: both lists are
# prose, and prose can gain a type on one side and not the other with nothing noticing.
#
# That is not hypothetical either. NetSuite's Step 1 reviewed purchase orders from the day it
# shipped and its Step 8 named bills and change orders only, so five reviewed purchase orders
# with clear verdicts were refused at the click - twice, on consecutive runs, before it was
# called a defect (2026-09-01). The review half knew about a type the execute half did not, and
# nothing compared the two lists. This is the comparison.
ITEM_TYPE_MANIFEST = {
    "netsuite-approval-double-check": {"Bill", "Purchase Order", "Change Order"},
}

# Step 6's schema line, which is the log's - and therefore the dashboard's - type vocabulary.
_TYPE_VOCAB = re.compile(r'"type":\s*"([^"]+)"')
_ROUTE_HEADING = "### Record types and their routes"


def check_execute_type_coverage():
    """Every record type the queue can hold must have a route in the execute step.

    Three sources have to agree: the `type` vocabulary in SKILL.md's state-file schema, the
    record-type table in its execute step, and ITEM_TYPE_MANIFEST here. A type in the first
    and not the second is a reviewed item nobody can action; a type in the second and not the
    first is a route for something the queue never produces. Both are silent - the first
    surfaces only at the moment of a click, on a queue the user has already worked through.

    Deliberately narrow, like the rest of these: it compares three sets of strings, and says
    nothing about whether a route is any good.
    """
    problems = []
    for entry in sorted(os.listdir(PLUGINS)):
        if entry.startswith("_"):
            continue
        skills = os.path.join(PLUGINS, entry, "skills")
        if not os.path.isdir(skills):
            continue
        for skill in sorted(os.listdir(skills)):
            expected = ITEM_TYPE_MANIFEST.get(skill)
            if expected is None:
                continue
            fp = os.path.join(skills, skill, "SKILL.md")
            if not os.path.isfile(fp):
                continue
            text = open(fp, encoding="utf-8").read()

            # D62/ruling 4: a spine may point at a references/ file instead of carrying a
            # section inline. The route table can live in either place, so the heading
            # search looks in both. The type-vocabulary check stays on the spine alone,
            # because Step 6's schema line never moves.
            route_text = text
            refs_dir = os.path.join(skills, skill, "references")
            if os.path.isdir(refs_dir):
                for ref_name in sorted(os.listdir(refs_dir)):
                    ref_path = os.path.join(refs_dir, ref_name)
                    if os.path.isfile(ref_path):
                        route_text += "\n" + open(ref_path, encoding="utf-8").read()

            vocab = _TYPE_VOCAB.findall(text)
            if len(vocab) != 1:
                problems.append(
                    "%s/%s: SKILL.md must declare the item-type vocabulary exactly once, as a "
                    '`"type": "A|B|C"` line in the state-file schema (found %d). That line is '
                    "what the execute step's routes are checked against."
                    % (entry, skill, len(vocab)))
            else:
                declared = {t.strip() for t in vocab[0].split("|") if t.strip()}
                for bad in sorted(declared - expected):
                    problems.append(
                        "%s/%s: the state-file schema allows type %r, which is not in "
                        "ITEM_TYPE_MANIFEST in scripts/shared_blocks.py. Add it there, and give "
                        "it a row in the execute step, in the same commit."
                        % (entry, skill, bad))
                for bad in sorted(expected - declared):
                    problems.append(
                        "%s/%s: ITEM_TYPE_MANIFEST expects type %r and the state-file schema no "
                        "longer allows it. A type dropped from the schema still arrives in the "
                        "queue - it just stops being written down."
                        % (entry, skill, bad))

            m = re.search(r"^%s$(.*?)^(?:#{2,3} |\d+\. )" % re.escape(_ROUTE_HEADING),
                          route_text, re.M | re.S)
            if not m:
                problems.append(
                    "%s/%s: SKILL.md has no '%s' section. Without it there is nothing saying "
                    "which types the execute step can act on, which is how a reviewed type "
                    "stays unactionable." % (entry, skill, _ROUTE_HEADING))
                continue
            rows = _table_rows(m.group(1), 3)
            routed = {r[0] for r in rows}
            for bad in sorted(expected - routed):
                problems.append(
                    "%s/%s: record type %r has no row in the execute step's route table, so a "
                    "run that reviews one cannot action it and will stop at the click. Add the "
                    "row, or drop the type from the queue - not clicking is correct behaviour "
                    "for a missing route, which is exactly why the gap is invisible."
                    % (entry, skill, bad))
            for bad in sorted(routed - expected):
                problems.append(
                    "%s/%s: the execute step routes record type %r, which is not in "
                    "ITEM_TYPE_MANIFEST. A route for a type the queue never produces is dead "
                    "prose; add the type to the manifest and the schema, or delete the row."
                    % (entry, skill, bad))
            for cells in rows:
                if not cells[1].strip() or not cells[2].strip():
                    problems.append(
                        "%s/%s: record type %r declares an empty gate or verification cell. A "
                        "route with a blank gate is worse than no route: it reads as covered."
                        % (entry, skill, cells[0]))
    return problems



===== scripts/shared_blocks.py lines 513-514 =====
    problems += check_execute_type_coverage()
    problems += check_execute_prompt_purity()
