#!/usr/bin/env python3
"""Checks on the record folders, the three indexes and the prose that cites them.

The global mandate says a file is the fallback, not the enforcement. `D82`, hooks and
checks pass, turns the prose rules into these five checks. validate.py imports this
module and calls each one, the same way it calls shared_blocks.

  check_frontmatter()      every record carries the five keys, an H1 and an outcome
  check_citations()        every citation resolves, carries a gloss and is not a path
  check_index_fresh()      each _index.md matches what the frontmatter generates
  check_index_size()       CLAUDE.md stays an index and names both plugins
  check_sentence_length()  no sentence in the prose exceeds 30 words

Two maintainer commands write instead of checking:

    python3 scripts/check_records.py --write-index          regenerate the 3 indexes
    python3 scripts/check_records.py --claim-ids [--apply]  number the pending records

Run with no argument to print every problem the five checks find.
"""

import collections
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKETPLACE = os.path.join(REPO, ".claude-plugin", "marketplace.json")

# folder -> (kind, id letter, index title)
FOLDERS = {
    "decisions": ("decision", "D", "Decisions"),
    "findings": ("finding", "F", "Findings"),
    "gaps": ("gap", "G", "Gaps"),
}
REQUIRED_KEYS = ("id", "slug", "kind", "status", "date")
STATUSES = ("open", "settled", "superseded", "abandoned", "observed", "unobserved")
OUTCOME_MARKER = "**Outcome protected.**"

CLAUDE_MD_MAX_LINES = 150
MAX_SENTENCE_WORDS = 30

INDEX_BLURB = (
    "Generated from the frontmatter and the first outcome sentence of every record in "
    "this folder, sorted by `date` then `slug`."
)
INDEX_COLUMNS = "| id | slug | title | status | date | outcome |"
INDEX_RULE = "|---|---|---|---|---|---|"

# A citation is an id plus a gloss. On a branch the id is the slug in guillemets.
CITATION = re.compile(
    r"`?\b(?P<letter>[DFG])"
    r"(?:(?P<num>[0-9]+)\b|‹(?P<slug>[a-z0-9-]+)›)`?")
SLUG_CITATION = re.compile(r"`?\b([DFG])‹([a-z0-9-]+)›`?")
PATH_CITATIONS = ("prose.md", "CLAUDE.md#", "see Step", "See Step")

# What looks like a citation but is not one.
#   form_names: G702 and G703 are AIA payment-application forms, not gap ids.
#   notation_lines: `D84`, the prose compliance plan, states the citation notation
#       itself. Its `D‹slug›` lines and the `D12` example on the Ids-and-citation
#       bullet are notation. Its migration map, lane table and done-when list cite
#       `prose.md` by path on purpose, as the record of a file that was removed.
NotCitations = collections.namedtuple("NotCitations", "form_names notation_file notation_marks")
NOT_CITATIONS = NotCitations(
    form_names=("G702", "G703"),
    notation_file=os.path.join("decisions", "prose-compliance-plan.md"),
    notation_marks=("‹", "`D12`"),
)


# ------------------------------------------------------------------ record model
Record = collections.namedtuple(
    "Record", "path rel folder kind letter keys title outcome body text")


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _frontmatter(text):
    """Return (keys dict, body) for a record file, or (None, text) with no block."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None, text
    keys = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            keys[km.group(1)] = km.group(2).strip()
    return keys, text[m.end():]


def _first_sentence(text):
    m = re.match(r"(.*?[.!?])(\s|$)", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


def record_files():
    """Every record file, as (folder, filename), in folder then filename order."""
    for folder in sorted(FOLDERS):
        d = os.path.join(REPO, folder)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".md") and fn != "_index.md":
                yield folder, fn


def load_records():
    """Read every record. A file with no frontmatter still comes back, keys None."""
    out = []
    for folder, fn in record_files():
        path = os.path.join(REPO, folder, fn)
        text = _read(path)
        keys, body = _frontmatter(text)
        kind, letter, _ = FOLDERS[folder]
        title = None
        tm = re.search(r"^#\s+(.*)$", body, re.M)
        if tm:
            title = tm.group(1).strip()
        outcome = None
        om = re.search(
            re.escape(OUTCOME_MARKER) + r"\s*(.*?)(?:\n\s*\n|\Z)", body, re.DOTALL)
        if om:
            outcome = _first_sentence(" ".join(om.group(1).split()))
        out.append(Record(path, os.path.join(folder, fn), folder, kind, letter,
                          keys, title, outcome, body, text))
    return out


def record_count():
    return sum(1 for _ in record_files())


def scanned_prose():
    """Every file the citation and path-citation checks read."""
    files = [os.path.join(REPO, "CLAUDE.md"), os.path.join(REPO, "README.md")]
    plugins = os.path.join(REPO, "plugins")
    if os.path.isdir(plugins):
        for entry in sorted(os.listdir(plugins)):
            if entry.startswith("_"):
                continue
            p = os.path.join(plugins, entry, "README.md")
            if os.path.isfile(p):
                files.append(p)
    for folder in sorted(FOLDERS):
        d = os.path.join(REPO, folder)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".md"):
                files.append(os.path.join(d, fn))
    return [f for f in files if os.path.isfile(f)]


def _rel(path):
    return os.path.relpath(path, REPO)


def _frontmatter_span(lines):
    """Return the 1-based last line number of a frontmatter block, or 0."""
    if not lines or lines[0].strip() != "---":
        return 0
    for i, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return i
    return 0


# ------------------------------------------------------------- check 1, records
def check_frontmatter():
    """Every record carries the five keys, a matching id, an H1 and an outcome."""
    problems = []
    seen = {}  # letter -> {id: rel}
    for rec in load_records():
        if rec.keys is None:
            problems.append("%s has no YAML frontmatter block" % rec.rel)
            continue
        missing = [k for k in REQUIRED_KEYS if not rec.keys.get(k)]
        if missing:
            problems.append("%s frontmatter is missing %s" % (rec.rel, ", ".join(missing)))
        stem = os.path.basename(rec.path)[:-3]
        if rec.keys.get("slug") != stem:
            problems.append(
                "%s slug is %r; it must equal the filename stem %r"
                % (rec.rel, rec.keys.get("slug"), stem))
        if rec.keys.get("kind") != rec.kind:
            problems.append(
                "%s kind is %r; a record in %s/ must be kind %r"
                % (rec.rel, rec.keys.get("kind"), rec.folder, rec.kind))
        status = rec.keys.get("status")
        if status not in STATUSES:
            problems.append(
                "%s status is %r; use one of %s" % (rec.rel, status, ", ".join(STATUSES)))
        date = rec.keys.get("date", "")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            problems.append("%s date is %r; write it as YYYY-MM-DD" % (rec.rel, date))
        rid = rec.keys.get("id", "")
        if rid != "pending":
            if not re.match(r"^[DFG][0-9]+$", rid):
                problems.append(
                    "%s id is %r; use 'pending' on a branch or %s<number>"
                    % (rec.rel, rid, rec.letter))
            elif rid[0] != rec.letter:
                problems.append(
                    "%s id is %r; a %s takes the letter %s"
                    % (rec.rel, rid, rec.kind, rec.letter))
            else:
                first = seen.setdefault(rec.letter, {}).get(rid)
                if first:
                    problems.append("%s reuses id %s, already held by %s" % (rec.rel, rid, first))
                else:
                    seen[rec.letter][rid] = rec.rel
        if rec.title is None:
            problems.append("%s has no H1 title line" % rec.rel)
        if OUTCOME_MARKER not in rec.body:
            problems.append("%s has no '%s' line" % (rec.rel, OUTCOME_MARKER))
    return problems


# ----------------------------------------------------------- check 2, citations
def _citation_targets():
    """(ids by letter, pending slugs by letter) for citation resolution."""
    ids = collections.defaultdict(set)
    pending = collections.defaultdict(set)
    for rec in load_records():
        if not rec.keys:
            continue
        rid = rec.keys.get("id", "")
        slug = rec.keys.get("slug", "")
        if rid == "pending":
            pending[rec.letter].add(slug)
        elif re.match(r"^[DFG][0-9]+$", rid):
            ids[rid[0]].add(rid)
    return ids, pending


def _is_notation(rel, line):
    if rel != NOT_CITATIONS.notation_file:
        return False
    return any(mark in line for mark in NOT_CITATIONS.notation_marks)


def check_citations():
    """Every citation resolves and carries a gloss. No citation is a path."""
    problems = []
    ids, pending = _citation_targets()
    for path in scanned_prose():
        rel = _rel(path)
        lines = _read(path).splitlines()
        fm_end = _frontmatter_span(lines)
        in_index = os.path.basename(path) == "_index.md"
        for n, line in enumerate(lines, start=1):
            if n <= fm_end:
                continue  # frontmatter holds the record's own id, not a citation
            if _is_notation(rel, line):
                continue
            for text in PATH_CITATIONS:
                if text in line and rel != NOT_CITATIONS.notation_file:
                    problems.append(
                        "%s:%d cites a path (%r). Cite the record id and a gloss."
                        % (rel, n, text))
            if in_index and line.lstrip().startswith("|"):
                continue  # an index row is a table cell, so the gloss is a column
            for m in CITATION.finditer(line):
                token = m.group(0).strip("`")
                if token in NOT_CITATIONS.form_names:
                    continue
                letter = m.group("letter")
                if m.group("slug"):
                    slug = m.group("slug")
                    if slug not in pending[letter]:
                        problems.append(
                            "%s:%d cites %s, and no record in %s/ has slug %r with "
                            "id: pending" % (rel, n, token, _folder_of(letter), slug))
                elif token not in ids[letter]:
                    problems.append(
                        "%s:%d cites %s, and no record carries that id" % (rel, n, token))
                # A citation is 'id, gloss'. The gloss may wrap to the next line.
                rest = line[m.end():]
                if rest.startswith(", ") and rest[2:].strip():
                    continue
                if rest.rstrip() == "," and n < len(lines) and lines[n].strip():
                    continue
                problems.append(
                    "%s:%d cites %s with no gloss. Write 'id, short gloss'."
                    % (rel, n, token))
    return problems


def _folder_of(letter):
    for folder, (_, l, _t) in FOLDERS.items():
        if l == letter:
            return folder
    return "?"


# -------------------------------------------------------------- check 3, indexes
def generate_index(folder):
    """Build an _index.md for one folder from its records' frontmatter."""
    _kind, _letter, title = FOLDERS[folder]
    rows = []
    for rec in load_records():
        if rec.folder != folder or not rec.keys:
            continue
        rows.append((
            rec.keys.get("date", ""),
            rec.keys.get("slug", ""),
            rec.keys.get("id", ""),
            rec.title or "",
            rec.keys.get("status", ""),
            rec.outcome or "",
        ))
    rows.sort(key=lambda r: (r[0], r[1]))
    out = ["# %s" % title, "", INDEX_BLURB, "", INDEX_COLUMNS, INDEX_RULE]
    for date, slug, rid, rtitle, status, outcome in rows:
        out.append("| %s | `%s` | %s | %s | %s | %s |"
                   % (rid, slug, rtitle, status, date, outcome))
    return "\n".join(out) + "\n"


def check_index_fresh():
    """Each _index.md matches what the frontmatter generates."""
    problems = []
    for folder in sorted(FOLDERS):
        path = os.path.join(REPO, folder, "_index.md")
        want = generate_index(folder)
        if not os.path.isfile(path):
            problems.append("%s/_index.md is missing. Run check_records.py --write-index."
                            % folder)
            continue
        have = _read(path)
        if have != want:
            have_lines, want_lines = have.splitlines(), want.splitlines()
            detail = "%d line(s) against %d" % (len(have_lines), len(want_lines))
            for i, (a, b) in enumerate(zip(have_lines, want_lines), start=1):
                if a != b:
                    detail = "first difference at line %d: %s" % (i, b[:90])
                    break
            problems.append(
                "%s/_index.md is stale (%s). Run check_records.py --write-index."
                % (folder, detail))
    return problems


def write_indexes():
    written = []
    for folder in sorted(FOLDERS):
        path = os.path.join(REPO, folder, "_index.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(generate_index(folder))
        written.append(os.path.join(folder, "_index.md"))
    return written


# ----------------------------------------------------------- check 4, the index
def registered_plugins():
    """Plugin names from the marketplace manifest, so this check needs no import."""
    if not os.path.isfile(MARKETPLACE):
        return []
    with open(MARKETPLACE, encoding="utf-8") as fh:
        mkt = json.load(fh)
    return [e["name"] for e in mkt.get("plugins", []) if e.get("name")]


def check_index_size():
    """CLAUDE.md stays an index, at the line ceiling, and names both plugins."""
    problems = []
    path = os.path.join(REPO, "CLAUDE.md")
    if not os.path.isfile(path):
        return ["CLAUDE.md is missing"]
    body = _read(path)
    lines = body.splitlines()
    if len(lines) > CLAUDE_MD_MAX_LINES:
        problems.append(
            "CLAUDE.md is %d lines. The index rule is %d or fewer, so move the prose "
            "into a record." % (len(lines), CLAUDE_MD_MAX_LINES))
    for name in registered_plugins():
        if name not in body:
            problems.append("CLAUDE.md does not name the registered plugin %r" % name)
    return problems


# --------------------------------------------------- check 5, sentence length
ABBREVIATION = re.compile(r"(?:e\.g|i\.e|etc|vs|approx|no|fig|Mr|Mrs|Dr)\.$", re.I)


def split_sentences(text):
    """Split a paragraph into sentences. An abbreviation does not end one."""
    out, cur = [], ""
    for token in re.split(r"(\s+)", text):
        cur += token
        bare = token.strip()
        if not bare:
            continue
        if not re.search(r"[.!?][\"')\]]?$", bare):
            continue
        if ABBREVIATION.search(bare) or re.match(r"^\d+\.$", bare):
            continue
        out.append(cur.strip())
        cur = ""
    if cur.strip():
        out.append(cur.strip())
    return out


def _measured_prose():
    files = [os.path.join(REPO, "CLAUDE.md"), os.path.join(REPO, "README.md")]
    plugins = os.path.join(REPO, "plugins")
    if os.path.isdir(plugins):
        for entry in sorted(os.listdir(plugins)):
            if entry.startswith("_"):
                continue
            p = os.path.join(plugins, entry, "README.md")
            if os.path.isfile(p):
                files.append(p)
    for folder, fn in record_files():
        files.append(os.path.join(REPO, folder, fn))
    return [f for f in files if os.path.isfile(f)]


def check_sentence_length():
    """No sentence passes the word ceiling. Code, tables and URLs are skipped."""
    problems = []
    for path in _measured_prose():
        rel = _rel(path)
        lines = _read(path).splitlines()
        fm_end = _frontmatter_span(lines)
        in_fence = False
        para, start = [], None

        def flush(para, start):
            if not para:
                return
            text = " ".join(para)
            text = re.sub(r"`[^`]*`", "X", text)          # a code span is one token
            text = re.sub(r"https?://\S+", "U", text)      # a URL is one token
            text = re.sub(r"[*_>]", "", text)
            for sentence in split_sentences(text):
                words = sentence.split()
                if len(words) > MAX_SENTENCE_WORDS:
                    problems.append(
                        "%s:%d has a %d-word sentence, over the %d-word ceiling: %s"
                        % (rel, start, len(words), MAX_SENTENCE_WORDS, sentence[:120]))

        for n, line in enumerate(lines, start=1):
            if n <= fm_end:
                continue
            if line.lstrip().startswith("```"):
                flush(para, start)
                para, start = [], None
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            s = line.strip()
            if not s or s.startswith("|") or s.startswith("#"):
                flush(para, start)
                para, start = [], None
                continue
            if s.startswith(("- ", "* ")) or re.match(r"^\d+\. ", s):
                flush(para, start)
                para, start = [s], n
                continue
            if start is None:
                start = n
            para.append(s)
        flush(para, start)
    return problems


# ------------------------------------------------------ check 6, waiter loops
# The mandate: "Never write a waiter loop." A waiter loop is an unbounded
# wait-and-retry: text that tells a run to sit and recheck with no stated limit.
WAITER_PATTERNS = (
    re.compile(r"wait and re-", re.I),
    re.compile(r"wait,\s*then re-", re.I),
    re.compile(r"re-check until", re.I),
    re.compile(r"retry until", re.I),
    re.compile(r"poll until", re.I),
    re.compile(r"keep checking", re.I),
    re.compile(r"\bsleep\b[^.!?]{0,40}\bretry\b", re.I),
    re.compile(r"\bretry\b[^.!?]{0,40}\bsleep\b", re.I),
    re.compile(r"every\s+\d+\s+(second|seconds|minute|minutes|hour|hours)\b", re.I),
)

# A retry that names its own bound in the same sentence is not a waiter loop.
BOUND_PATTERNS = (
    re.compile(r"\bat most\b", re.I),
    re.compile(r"\bonce\b", re.I),
    re.compile(r"\btwice\b", re.I),
    re.compile(r"\bone more time\b", re.I),
)

# A line that quotes a forbidden phrase as a negative example, not an instruction.
# Keep this list short: every entry names the one line and carries its own comment.
WaiterExclusion = collections.namedtuple("WaiterExclusion", "rel needle comment")
WAITER_EXCLUSIONS = (
    WaiterExclusion(
        os.path.join("decisions", "prose-compliance-plan.md"),
        '"wait and re-check"',
        "the plan's own worked example quotes the forbidden phrase to name it, "
        "inside a table cell; it does not instruct a wait.",
    ),
)


def _is_waiter_exclusion(rel, line):
    return any(rel == ex.rel and ex.needle in line for ex in WAITER_EXCLUSIONS)


def _waiter_scanned_files():
    """CLAUDE.md, the three READMEs, every record, both SKILL.md and every shared block."""
    files = [os.path.join(REPO, "CLAUDE.md"), os.path.join(REPO, "README.md")]
    plugins = os.path.join(REPO, "plugins")
    if os.path.isdir(plugins):
        for entry in sorted(os.listdir(plugins)):
            if entry.startswith("_"):
                continue
            root = os.path.join(plugins, entry)
            p = os.path.join(root, "README.md")
            if os.path.isfile(p):
                files.append(p)
            skills_dir = os.path.join(root, "skills")
            if os.path.isdir(skills_dir):
                for skill in sorted(os.listdir(skills_dir)):
                    sp = os.path.join(skills_dir, skill, "SKILL.md")
                    if os.path.isfile(sp):
                        files.append(sp)
        shared = os.path.join(plugins, "_shared")
        if os.path.isdir(shared):
            for fn in sorted(os.listdir(shared)):
                if fn.endswith(".block"):
                    files.append(os.path.join(shared, fn))
    for folder, fn in record_files():
        files.append(os.path.join(REPO, folder, fn))
    return [f for f in files if os.path.isfile(f)]


def check_waiter_loops():
    """No sentence instructs an unbounded wait-and-retry. Code fences are skipped."""
    problems = []
    for path in _waiter_scanned_files():
        rel = _rel(path)
        lines = _read(path).splitlines()
        fm_end = _frontmatter_span(lines)
        in_fence = False
        for n, raw in enumerate(lines, start=1):
            if n <= fm_end:
                continue
            s = raw.strip()
            if s.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or not s:
                continue
            if _is_waiter_exclusion(rel, raw):
                continue
            text = re.sub(r"`[^`]*`", "X", s)
            for sentence in split_sentences(text) or [text]:
                if not any(p.search(sentence) for p in WAITER_PATTERNS):
                    continue
                if any(b.search(sentence) for b in BOUND_PATTERNS):
                    continue
                problems.append("%s:%d %s" % (rel, n, sentence[:160]))
    return problems


# ------------------------------------------------------------------- claim ids
def claim_ids(dry_run=True):
    """Number every pending record, rewrite its slug citations, refresh the indexes.

    An existing id is never renumbered. Returns the lines of what was, or would be,
    done.
    """
    log = []
    records = load_records()
    taken = collections.defaultdict(set)
    for rec in records:
        if rec.keys and re.match(r"^[DFG][0-9]+$", rec.keys.get("id", "")):
            taken[rec.letter].add(int(rec.keys["id"][1:]))

    pending = [r for r in records if r.keys and r.keys.get("id") == "pending"]
    pending.sort(key=lambda r: (r.keys.get("date", ""), r.keys.get("slug", "")))
    if not pending:
        log.append("no record has id: pending. Nothing to claim.")
        return log

    assigned = {}  # (letter, slug) -> new id
    for rec in pending:
        n = 1
        while n in taken[rec.letter]:
            n += 1
        taken[rec.letter].add(n)
        new_id = "%s%d" % (rec.letter, n)
        assigned[(rec.letter, rec.keys["slug"])] = new_id
        log.append("%s takes id %s" % (rec.rel, new_id))
        text = re.sub(r"^id:\s*pending\s*$", "id: " + new_id, rec.text, count=1, flags=re.M)
        if not dry_run:
            with open(rec.path, "w", encoding="utf-8") as fh:
                fh.write(text)

    slug_to_id = {slug: rid for (_letter, slug), rid in assigned.items()}

    for path in scanned_prose():
        rel = _rel(path)
        text = _read(path)
        out_lines = []
        changed = 0
        for line in text.splitlines(True):
            if _is_notation(rel, line):
                out_lines.append(line)
                continue

            def swap(m, _line=line):
                letter, slug = m.group(1), m.group(2)
                new = assigned.get((letter, slug))
                if not new:
                    return m.group(0)
                return m.group(0).replace(letter + "‹" + slug + "›", new)

            new_line, count = SLUG_CITATION.subn(swap, line)
            # supersedes: takes an id once the number exists
            sm = re.match(r"^(supersedes:\s*)([a-z0-9-]+)\s*$", new_line)
            if sm and sm.group(2) in slug_to_id:
                new_line = "%s%s\n" % (sm.group(1), slug_to_id[sm.group(2)])
                count += 1
            if count:
                changed += count
            out_lines.append(new_line)
        if changed:
            log.append("%s: %d citation(s) rewritten" % (rel, changed))
            if not dry_run:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("".join(out_lines))

    if dry_run:
        log.append("dry run. Pass --apply to write, which also refreshes the indexes.")
    else:
        for name in write_indexes():
            log.append("%s regenerated" % name)
    return log


# -------------------------------------------------------- check 7, device shots
# D81, device usability check, asks for every screen at three widths and in both
# themes. `scripts/measure_float.js --shots` writes the captures and this file.
SHOTS_DIR = os.path.join(REPO, ".claude", "shots")
SHOTS_SUMMARY = os.path.join(SHOTS_DIR, "summary.txt")
MIN_SHOT_ROWS = 18  # 3 screens x 3 widths x 2 themes
SHOTS_COUNTS = re.compile(r"captures:\s*(\d+)\.\s*captures with overflow:\s*(\d+)\.")


def check_device_shots():
    """Fail on any capture overflow, or fewer than 18 rows. Silent when the file
    is absent — that case is a note, from device_shots_note(), not a failure."""
    problems = []
    if not os.path.isfile(SHOTS_SUMMARY):
        return problems
    text = _read(SHOTS_SUMMARY)
    m = SHOTS_COUNTS.search(text)
    if not m:
        problems.append(
            ".claude/shots/summary.txt has no 'captures: N. captures with overflow: "
            "M.' line. Re-run scripts/measure_float.js --shots.")
        return problems
    total, over = int(m.group(1)), int(m.group(2))
    if total < MIN_SHOT_ROWS:
        problems.append(
            ".claude/shots/summary.txt has %d capture(s); the device usability "
            "check (D81) wants at least %d" % (total, MIN_SHOT_ROWS))
    if over > 0:
        rows = [l for l in text.splitlines() if l.startswith("overflow: ")]
        problems.append(
            ".claude/shots/summary.txt reports %d capture(s) with horizontal "
            "overflow: %s" % (over, "; ".join(rows) or "see the file"))
    return problems


def device_shots_note():
    """A note, not a failure, when the shots have not been captured here."""
    if os.path.isfile(SHOTS_SUMMARY):
        return None
    return (
        "the device usability shots have not been captured in this environment. "
        "Run NODE_PATH=$(npm root -g) node scripts/measure_float.js --shots "
        ".claude/shots by hand, or in the 'shots' CI job.")


# -------------------------------------------------- check 8, id claim gated
# The mandate: "Never allocate a numbered record on a branch. Write a slug. Claim
# the number at merge." A record keeps id: pending until the maintainer claims it.
def check_no_pending_on_main():
    """On `main`, no record may still carry id: pending. Off main, this is silent —
    see pending_records_note() for the listing."""
    problems = []
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        return problems
    for rec in load_records():
        if rec.keys and rec.keys.get("id") == "pending":
            problems.append(
                "%s has id: pending on main. Claim ids before merge: "
                "python3 scripts/check_records.py --claim-ids --apply" % rec.rel)
    return problems


def pending_records_note():
    """A note, not a failure, listing records still pending off main."""
    if os.environ.get("GITHUB_REF") == "refs/heads/main":
        return None
    pending = [r for r in load_records() if r.keys and r.keys.get("id") == "pending"]
    if not pending:
        return None
    return "%d record(s) still carry id: pending: %s" % (
        len(pending), ", ".join(sorted(r.keys.get("slug", "?") for r in pending)))


def check_claim_dry_run():
    """A dry run of claim_ids(): fail if a slug citation would stay unresolved
    after every pending record is numbered. Runs on every ref, so a branch whose
    citations cannot resolve fails before merge, not after."""
    problems = []
    records = load_records()
    taken = collections.defaultdict(set)
    for rec in records:
        if rec.keys and re.match(r"^[DFG][0-9]+$", rec.keys.get("id", "")):
            taken[rec.letter].add(int(rec.keys["id"][1:]))

    pending = [r for r in records if r.keys and r.keys.get("id") == "pending"]
    pending.sort(key=lambda r: (r.keys.get("date", ""), r.keys.get("slug", "")))
    assigned = {}
    for rec in pending:
        n = 1
        while n in taken[rec.letter]:
            n += 1
        taken[rec.letter].add(n)
        assigned[(rec.letter, rec.keys["slug"])] = "%s%d" % (rec.letter, n)

    for path in scanned_prose():
        rel = _rel(path)
        for n, line in enumerate(_read(path).splitlines(), start=1):
            if _is_notation(rel, line):
                continue
            for m in SLUG_CITATION.finditer(line):
                letter, slug = m.group(1), m.group(2)
                if (letter, slug) not in assigned:
                    problems.append(
                        "%s:%d cites %s‹%s›, which would stay unresolved after "
                        "claim_ids runs — no pending record holds that slug"
                        % (rel, n, letter, slug))
    return problems


# ----------------------------------------------------------------------- main
CHECKS = (
    ("frontmatter", check_frontmatter),
    ("citations", check_citations),
    ("index freshness", check_index_fresh),
    ("index size", check_index_size),
    ("sentence length", check_sentence_length),
    ("waiter loops", check_waiter_loops),
    ("device shots", check_device_shots),
    ("no pending on main", check_no_pending_on_main),
    ("claim dry run", check_claim_dry_run),
)


def run():
    problems = []
    for _name, fn in CHECKS:
        problems += fn()
    return problems


def main(argv):
    if "--write-index" in argv:
        for name in write_indexes():
            print("wrote %s" % name)
        return 0
    if "--claim-ids" in argv:
        for line in claim_ids(dry_run="--apply" not in argv):
            print(line)
        return 0
    if "--check-claim" in argv:
        problems = check_claim_dry_run()
        for p in problems:
            print("  - %s" % p)
        if problems:
            print("FAILED (%d)" % len(problems))
            return 1
        print("OK: every slug citation would resolve after claim_ids runs")
        return 0
    for note in (device_shots_note(), pending_records_note()):
        if note:
            print("note: %s" % note)
    problems = run()
    for p in problems:
        print("  - %s" % p)
    if problems:
        print("FAILED (%d) across %d record(s)" % (len(problems), record_count()))
        return 1
    print("OK: %d record(s), %s checked"
          % (record_count(), ", ".join(name for name, _ in CHECKS)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
