#!/usr/bin/env python3
"""Tests for the backtick slug citation check in scripts/check_records.py.

    PYTHONUTF8=1 python3 scripts/test_check_records.py

A slug cited as D`slug` is never rewritten by the stamp. .github/stamp.json cite.pattern
rewrites only D‹slug›. The check named NAME must flag the backtick form on every ref and
name the D‹slug› form in its message. Stdlib only. Each case builds its own throwaway
tree. The four leftovers are pinned to their 41b96f9 lines, so this test does not depend
on the live records, which the fix rewrites.
"""
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_records as cr  # noqa: E402

NAME = "backtick slug citations"
REFS = (None, "refs/heads/main", "refs/heads/claude/some-branch")  # every ref runs the check


def _check():
    fns = dict(cr.CHECKS)
    assert NAME in fns, "check %r is not registered in check_records.CHECKS" % NAME
    return fns[NAME]


def _run(files, ref=None):
    """Write files under a throwaway REPO, run the check, return its problems."""
    root = tempfile.mkdtemp(prefix="cr-test-")
    saved_repo = cr.REPO
    saved_ref = os.environ.pop("GITHUB_REF", None)
    try:
        for rel, text in files.items():
            path = os.path.join(root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
        cr.REPO = root
        if ref is not None:
            os.environ["GITHUB_REF"] = ref
        return _check()()
    finally:
        cr.REPO = saved_repo
        os.environ.pop("GITHUB_REF", None)
        if saved_ref is not None:
            os.environ["GITHUB_REF"] = saved_ref
        shutil.rmtree(root, ignore_errors=True)


def _doc(*lines):
    return "\n".join(lines) + "\n"


def _os(rel):
    """A message names a path with the local separator (backslash on Windows)."""
    return rel.replace("/", os.sep)


DECISION = "decisions/some-decision.md"
SKILL = "plugins/some-plugin/skills/some-skill/SKILL.md"

# ---- 1. the backtick form is flagged, on every ref, naming the D‹slug› form
for ref in REFS:
    p = _run({DECISION: _doc("Intro.", "See D`some-slug`, the gloss.")}, ref)
    assert len(p) == 1, (ref, p)
    assert "D‹some-slug›" in p[0], (ref, p)
    assert _os(DECISION) + ":2" in p[0], (ref, p)

# every letter the stamp claims: F and G must name their own form
for letter, folder in (("F", "findings"), ("G", "gaps")):
    p = _run({"%s/some-note.md" % folder: _doc("Cited as %s`some-slug`, gloss." % letter)})
    assert len(p) == 1 and "%s‹some-slug›" % letter in p[0], (letter, p)

# a skill prompt is scanned too, not only records
p = _run({SKILL: _doc("Text.", "**Head.** (D`some-slug`, a gloss).")})
assert len(p) == 1 and _os(SKILL) + ":2" in p[0], p

# ---- 2. flagging is not hidden by the context around the citation
# a lone apostrophe in the text does not stop the scan
p = _run({DECISION: _doc("Don't cite D`some-slug` by slug.")})
assert len(p) == 1 and "D‹some-slug›" in p[0], p
# a backtick inside a double-quoted string does not pair across the real citation
p = _run({DECISION: _doc('Write "a`b" then D`some-slug`, gloss.')})
assert len(p) == 1 and "D‹some-slug›" in p[0], p
# the scan resumes after a fence closes, and skips the fence body
p = _run({DECISION: _doc("```text", "D`inside-fence` example", "```", "See D`some-slug`, gloss.")})
assert len(p) == 1 and _os(DECISION) + ":4" in p[0], p

# ---- 3. no false alarm on ordinary inline code, a lone backtick, quotes, or fences
CLEAN = (
    "**Evidence.** `unmeasured`. Nobody timed it.",
    "Read the PDF `x` file.",
    "Use the ID `abc` field.",
    "Lone opener: D` glyph, then plain text.",
    "Lone opener: type D`abc and never close it.",
    'Quoted: the token "D" then `code`.',
    'Backtick in a string: say "a`b" then `c`.',
    "Correct form, not flagged: See D‹some-slug›, the gloss.",
)
for ref in REFS:
    assert _run({DECISION: _doc(*CLEAN)}, ref) == [], ref
    assert _run({DECISION: _doc("```text", "D`some-slug` example", "```")}, ref) == [], ref

# ---- 4. the four leftovers on 41b96f9, pinned verbatim, each must be named
LEFTOVERS = (
    ("decisions/in-page-call-deadline.md", 29,
     "- The 20-second limit is unmeasured against real payloads. See G`fetch-limit-includes-body`, "
     "the 20 second limit counts the body."),
    ("findings/netsuite-verdict-vocabulary-blocks-fold.md", 33,
     "Rewritten 2026-10-12 for the third verdict (D`netsuite-history-open`, a third NetSuite verdict)."),
    ("gaps/fetch-limit-includes-body.md", 14,
     "**Evidence.** `unmeasured`. Nobody timed the largest invoice JSON or the largest attachment "
     "against 20 seconds. Nobody timed a whole read against 60. Do not cite 20 seconds as safe. "
     "The 2026-10-09 run is the only incident behind it. See D`in-page-call-deadline`, every "
     "in-page call stops itself."),
    ("plugins/netsuite-approval-review/skills/netsuite-approval-double-check/SKILL.md", 483,
     "**The third verdict, `history-open` (D`netsuite-history-open`, a third verdict).** It sits "
     "between `clear` and `flagged`. Name the evidence in `head`. It applies when **every check on "
     "the item itself passes**. Those checks are the math, adequate support, and the amount tying "
     "to NetSuite. Adequate support means a **full** `text` or `spreadsheet` read. It also needs "
     "this reconcile, with 5c billed-to-date, to leave an **unexplained remainder in dollars** that "
     "is not zero. Example: the item's own figures tie. The PO's approved billing history runs ahead "
     "of the vendor's previously-billed figure. Nothing explains the gap."),
)
files = {}
for rel, line_no, text in LEFTOVERS:
    files[rel] = "\n" * (line_no - 1) + text + "\n"
for ref in REFS:
    p = _run(files, ref)
    assert len(p) == 4, (ref, p)
    for rel, line_no, _text in LEFTOVERS:
        assert any(("%s:%d" % (_os(rel), line_no)) in m for m in p), (rel, line_no, p)

print("OK: backtick slug citation checks passed")
