#!/usr/bin/env python3
"""Exercise check_version_bump.run() against throwaway git repos. Stdlib only.

Each case builds its own repo with a main branch and a feature branch, so this
does not depend on this repo's history (CI checkouts are shallow).
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_version_bump as cvb  # noqa: E402


def _sh(repo, *args):
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo, check=True, capture_output=True,
    )


def _skill_md(repo, plugin, skill, version, body="body"):
    d = os.path.join(repo, "plugins", plugin, "skills", skill)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(f"---\nname: {skill}\n---\n\n**Skill version {version} — 2026-09-24.**\n\n{body}\n"
                 + "".join(f"line {i}\n" for i in range(20)))


def _asset(repo, skill_dir, text):
    os.makedirs(os.path.join(repo, skill_dir, "assets"), exist_ok=True)
    with open(os.path.join(repo, skill_dir, "assets", "a.txt"), "w", encoding="utf-8") as fh:
        fh.write(text + "\n" + "".join(f"asset {i}\n" for i in range(20)))


def _case(feature, base=None):
    """Base: plugin p, skill s at version 3, plus base(repo). Apply feature(repo) on a
    branch, run the check."""
    repo = tempfile.mkdtemp()
    try:
        _sh(repo, "init", "-q", "-b", "main")
        _skill_md(repo, "p", "s", 3)
        _asset(repo, "plugins/p/skills/s", "base")
        if base:
            base(repo)
        _sh(repo, "add", "-A")
        _sh(repo, "commit", "-q", "-m", "base")
        _sh(repo, "checkout", "-q", "-b", "feat")
        feature(repo)
        _sh(repo, "add", "-A")
        _sh(repo, "commit", "-q", "-m", "feat")
        cvb.REPO = repo
        problems, note = cvb.run("main")
        assert not note, note
        return problems
    finally:
        shutil.rmtree(repo)


def _mv(repo, src, dst):
    _sh(repo, "mv", src, dst)


def rename_skill(version):
    def f(repo):
        _mv(repo, "plugins/p/skills/s", "plugins/p/skills/s2")
        _skill_md(repo, "p", "s2", version, body="changed")
    return f


def rename_plugin(version):
    def f(repo):
        _mv(repo, "plugins/p", "plugins/p2")
        _skill_md(repo, "p2", "s", version, body="changed")
    return f


def new_skill(version):
    return lambda repo: _skill_md(repo, "p", "fresh", version)


def in_place(version):
    return lambda repo: _skill_md(repo, "p", "s", version, body="changed")


def rename_plugin_asset_only(repo):
    _mv(repo, "plugins/p", "plugins/p2")  # SKILL.md moves as R100
    _asset(repo, "plugins/p2/skills/s", "changed")


def delete_skill(repo):
    _sh(repo, "rm", "-q", "-r", "plugins/p/skills/s")


def retired_skill(repo):  # base: a skill outside plugins/*/skills/*
    _skill_md(repo, "p", "r", 3)
    os.rename(os.path.join(repo, "plugins/p/skills/r"), os.path.join(repo, "actionable-retired"))


def move_in_retired(repo):
    _mv(repo, "actionable-retired", "plugins/p/skills/r")


# want_problem: False, True, or a substring the problems must contain
CASES = [
    ("a skill dir renamed + changed, no bump", rename_skill(3), "p/s -> p/s2 changed"),
    ("b skill dir renamed + changed, bumped", rename_skill(4), False),
    ("c plugin dir renamed + changed, no bump", rename_plugin(3), True),
    ("c' plugin dir renamed + changed, bumped", rename_plugin(4), False),
    ("d new skill at v1", new_skill(1), False),
    ("e new skill at v2", new_skill(2), "rename git could not detect"),
    ("f in-place change, no bump", in_place(3), True),
    ("f in-place change, bumped", in_place(4), False),
    ("g R100 plugin rename, only an asset changed, no bump", rename_plugin_asset_only, "p/s -> p2/s"),
    ("h skill deleted", delete_skill, False),
    ("i skill moved in from outside plugins/*/skills/*, no bump", move_in_retired,
     "actionable-retired/SKILL.md -> p/r changed", retired_skill),
]

if __name__ == "__main__":
    failed = []
    for name, feature, want_problem, *base in CASES:
        try:
            problems = _case(feature, *base)
        except Exception as e:  # a crash in run() is a failed case, not a traceback
            failed.append(f"{name}: raised {e!r}")
            continue
        ok = bool(problems) == bool(want_problem) and (
            not isinstance(want_problem, str) or want_problem in " ".join(problems))
        if not ok:
            failed.append(f"{name}: want problem={want_problem}, got {problems}")
    if failed:
        print(f"FAILED ({len(failed)}):")
        for f in failed:
            print(f"  - {f}")
        sys.exit(1)
    print(f"OK: {len(CASES)} version-bump cases")
