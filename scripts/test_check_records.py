#!/usr/bin/env python3
"""Exercise check_records.claim_ids() against throwaway git repos. Stdlib only.

Each case builds its own repo with a main branch, so this does not depend on
this repo's history (CI checkouts are shallow). The incident: claim_ids picks
the lowest id free in the CURRENT tree and never looks at retired ids, so a
deleted record's id gets handed to a new record, breaking cite-by-id.
"""
import os
import shutil
import stat
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_records as cr  # noqa: E402


def _rmtree(repo):
    def _on_rm_error(func, path, _exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(repo, onexc=_on_rm_error) if sys.version_info >= (3, 12) \
        else shutil.rmtree(repo, onerror=_on_rm_error)


def _sh(repo, *args):
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo, check=True, capture_output=True,
    )


def _record(repo, folder, letter, n, slug, status="open"):
    d = os.path.join(repo, folder)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, slug + ".md")
    rid = "pending" if n is None else "%s%d" % (letter, n)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(
            "---\nid: %s\nslug: %s\nkind: x\nstatus: %s\ndate: 2026-01-0%d\n---\n"
            "# Title\n\n**Outcome protected.** Thing.\n" % (rid, slug, status, (n or 9) % 9 + 1)
        )
    return path


def _init(repo):
    _sh(repo, "init", "-q", "-b", "main")
    for folder in cr.FOLDERS:
        os.makedirs(os.path.join(repo, folder), exist_ok=True)


def _commit(repo, msg):
    _sh(repo, "add", "-A")
    _sh(repo, "commit", "-q", "-m", msg)


def _claim(repo):
    cr.REPO = repo
    cr.claim_ids(dry_run=False)


def _id_of(repo, folder, slug):
    with open(os.path.join(repo, folder, slug + ".md"), encoding="utf-8") as fh:
        text = fh.read()
    keys, _ = cr._frontmatter(text)
    return keys["id"]


def case_deleted_top_id_not_reused(folder, letter):
    """G1, G2 committed; G1 deleted in a later commit; a pending record is
    claimed. The new id must be one above the highest ever held (G3), never
    the retired G1."""
    repo = tempfile.mkdtemp()
    try:
        _init(repo)
        _record(repo, folder, letter, 1, "first")
        _record(repo, folder, letter, 2, "second")
        _commit(repo, "base")
        os.remove(os.path.join(repo, folder, "first.md"))
        _commit(repo, "retire first")
        _record(repo, folder, letter, None, "third")
        _commit(repo, "add pending")
        _claim(repo)
        got = _id_of(repo, folder, "third")
        want = "%s3" % letter
        ok = got == want
        return ok, got, want
    finally:
        _rmtree(repo)


def case_no_deletion_next_is_max_plus_one(folder, letter):
    """Today's behaviour: with no deletion, the next id is max present + 1."""
    repo = tempfile.mkdtemp()
    try:
        _init(repo)
        _record(repo, folder, letter, 1, "first")
        _record(repo, folder, letter, 2, "second")
        _commit(repo, "base")
        _record(repo, folder, letter, None, "third")
        _commit(repo, "add pending")
        _claim(repo)
        got = _id_of(repo, folder, "third")
        want = "%s3" % letter
        return got == want, got, want
    finally:
        _rmtree(repo)


def case_two_pending_get_distinct_ids_above_max_ever_held():
    """Two pending gaps claimed together get two distinct ids, both above the
    highest id ever held (G1 deleted, G2 present -> highest ever held is G2)."""
    repo = tempfile.mkdtemp()
    try:
        _init(repo)
        _record(repo, "gaps", "G", 1, "first")
        _record(repo, "gaps", "G", 2, "second")
        _commit(repo, "base")
        os.remove(os.path.join(repo, "gaps", "first.md"))
        _commit(repo, "retire first")
        _record(repo, "gaps", "G", None, "third")
        _record(repo, "gaps", "G", None, "fourth")
        _commit(repo, "add pendings")
        _claim(repo)
        got_third = _id_of(repo, "gaps", "third")
        got_fourth = _id_of(repo, "gaps", "fourth")
        distinct = got_third != got_fourth
        above = all(int(x[1:]) > 2 for x in (got_third, got_fourth))
        return distinct and above, (got_third, got_fourth), "both > G2, distinct"
    finally:
        _rmtree(repo)


CASES = [
    ("a: gap, deleted top id not reused", lambda: case_deleted_top_id_not_reused("gaps", "G")),
    ("b: finding, deleted top id not reused", lambda: case_deleted_top_id_not_reused("findings", "F")),
    ("b: decision, deleted top id not reused", lambda: case_deleted_top_id_not_reused("decisions", "D")),
    ("c: no deletion, next is max+1", lambda: case_no_deletion_next_is_max_plus_one("gaps", "G")),
    ("d: two pending, distinct ids above max ever held", case_two_pending_get_distinct_ids_above_max_ever_held),
]


def main():
    failures = 0
    for name, fn in CASES:
        ok, got, want = fn()
        status = "PASS" if ok else "FAIL"
        print("%s: %s (got %r, want %r)" % (status, name, got, want))
        if not ok:
            failures += 1
    if failures:
        print("FAILED (%d/%d case(s))" % (failures, len(CASES)))
        return 1
    print("OK: %d case(s)" % len(CASES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
