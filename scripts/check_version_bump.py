#!/usr/bin/env python3
"""Enforce the bump D43 cannot enforce: a skill that changes must raise its version.

D43 (decisions/skill-version-lines.md) makes validate.py assert the four version
sites agree with each other. It says outright: "It cannot enforce the bump." PR #19
(2026-09-16) proved the gap real - both skills gained a new Absolute rule and Step 9,
and the version line on each stayed exactly where it was.

This compares the current tree against a base ref (the branch's merge-base with
main, or the ref VALIDATE_BASE_REF names). For every skill whose files changed
since that base, the version number on HEAD must be higher than the version on the
base. A skill whose SKILL.md git sees as renamed (its skill or plugin folder moved)
is compared against its old path on the base, so a move does not escape the rule. A
skill absent from the base, and not the target of a rename, is new: it must carry
version 1 (D43, "A new skill starts at version 1.").

Run standalone:

    python3 scripts/check_version_bump.py [base-ref]

validate.py imports run() and folds any problems into the build gate.
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_RE = re.compile(r"^\*\*Skill version (\d+) — \d{4}-\d{2}-\d{2}\.\*\*", re.M)
SKILL_PATH_RE = re.compile(r"^plugins/([^/]+)/skills/([^/]+)/")


def _git(*args):
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, check=False
    )


def _resolve_base(explicit):
    candidates = [explicit] if explicit else []
    candidates += [os.environ.get("VALIDATE_BASE_REF"), "origin/main", "main"]
    for ref in candidates:
        if ref and _git("rev-parse", "--verify", "--quiet", ref).returncode == 0:
            return ref
    return None


def _version_at(ref, path):
    """Return the skill version number SKILL.md carries at ref, or None."""
    if ref is None:
        full = os.path.join(REPO, path)
        if not os.path.isfile(full):
            return None
        with open(full, encoding="utf-8") as fh:
            text = fh.read()
    else:
        shown = _git("show", f"{ref}:{path}")
        if shown.returncode != 0:
            return None  # path did not exist at ref - a new skill
        text = shown.stdout
    m = VERSION_RE.search(text)
    return int(m.group(1)) if m else None


def run(base_ref=None):
    """Return (problems, note). One or the other is always empty."""
    base = _resolve_base(base_ref)
    if base is None:
        return [], "no base ref to diff against (no origin/main, no main) - bump check skipped"

    merge_base = _git("merge-base", base, "HEAD")
    if merge_base.returncode != 0:
        return [], f"no merge-base with {base} - bump check skipped"
    range_spec = f"{merge_base.stdout.strip()}..HEAD"

    diff = _git("diff", "--name-status", "--find-renames", range_spec)
    if diff.returncode != 0:
        return [], f"'git diff {range_spec}' failed - bump check skipped"
    changed = [line.split("\t") for line in diff.stdout.splitlines()]
    if not changed:
        return [], "no commits ahead of %s - bump check skipped" % base

    touched_skills = {}
    renamed_from = {}  # new path -> its path at the merge base
    for status, *paths in changed:
        path = paths[-1]
        if status.startswith("R"):
            renamed_from[path] = paths[0]
        m = SKILL_PATH_RE.match(path)
        if m:
            touched_skills.setdefault((m.group(1), m.group(2)), []).append(path)

    problems = []
    for (plugin, skill), paths in sorted(touched_skills.items()):
        skill_md = f"plugins/{plugin}/skills/{skill}/SKILL.md"
        new = _version_at(None, skill_md)
        if new is None:
            continue  # validate.py's own frontmatter check already fails this
        old = _version_at(merge_base.stdout.strip(), renamed_from.get(skill_md, skill_md))
        if old is None:
            if new != 1:  # new skill - D43, "A new skill starts at version 1."
                problems.append(
                    f"{plugin}/{skill} is new but carries skill version {new} - a new "
                    f"skill starts at version 1. See D43, four synced version sites."
                )
            continue
        if new <= old:
            problems.append(
                f"{plugin}/{skill} changed ({len(paths)} file(s), e.g. {paths[0]}) but "
                f"the skill version stayed at {old} - bump it past {old} in this commit. "
                f"See D43, four synced version sites."
            )
    return problems, ""


if __name__ == "__main__":
    _problems, _note = run(sys.argv[1] if len(sys.argv) > 1 else None)
    if _note:
        print(f"note: {_note}")
    if _problems:
        print(f"FAILED ({len(_problems)}):")
        for p in _problems:
            print(f"  - {p}")
        sys.exit(1)
    print("OK: every changed skill raised its version")
