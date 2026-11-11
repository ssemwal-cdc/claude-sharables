#!/usr/bin/env python3
"""Exercise the asset-pin check against throwaway git repos. Stdlib and git only.

The check is check_asset_pins(repo_root) in scripts/shared_blocks.py, and `shared_blocks.py --check`
runs it. Each case builds a temp repo and runs that command inside it, as CI does. So a check that is
not there yet shows as a bad pin that passed, which is an assert, and never as a crash or an import
error.

Contract the builder implements:
- Only real tags count: <script src> and <link href> in plugins/*/skills/*/assets/*.html. Text in an
  HTML comment, in a JS string, or after a lone quote is not a tag. Attributes may come in any order,
  with either quote, across lines.
- A pin URL is https://cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables@<sha>/<repo path>.
- A refusal names its cause with this keyword in the message:
    sha not 40 hex ............ "40 hex"
    sha absent, full clone .... "does not exist"
    sha not an ancestor of HEAD "ancestor"
    blob at sha differs HEAD .. "differ"
    integrity not sha384 ...... "sha384" (sha384- plus base64 of the digest of the stored blob,
                                read with git cat-file, never the working file)
    crossorigin missing ....... "crossorigin"
- A shallow clone that cannot read the sha reports "unknown" as a note and exits 0. It is never ok
  and never fail. validate.yml's shots job checks out shallow and runs validate.py, so this is routine.
- Controls pass on the old code by design. They hold the no-false-alarm side, so a naive scan fails them.
"""
import base64
import hashlib
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "shared_blocks.py")  # copied into each temp repo: it finds its repo from its own path

# Temp files follow the run-folder standard (test-temp-standard: one temp root per repo, one run
# folder per run, siblings over a day old swept). This repo keeps its own copy of that helper.
TEMP_ROOT = os.path.join(tempfile.gettempdir(), "claude-sharables-test-temp")
RUN_RE = re.compile(r"[0-9]+-[0-9a-f]{32}")
MAX_AGE = 24 * 60 * 60
DAY = 24 * 60 * 60
FIXED_NOW = 1_800_000_000.0  # the sweep cases use this clock, never the real one
_RUN = None


def _clear_readonly(func, path, _exc):
    """Windows keeps .git objects read-only. Clear the bit and retry the one call."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _remove(path):
    shutil.rmtree(path, onerror=_clear_readonly)


def _sweep(root, own, now):
    """Remove each sibling run folder under root whose mtime is over a day before now. own stays."""
    try:
        names = os.listdir(root)
    except OSError:
        return
    for name in names:
        path = os.path.join(root, name)
        if path == own or not RUN_RE.fullmatch(name) or not os.path.isdir(path):
            continue
        if now - os.path.getmtime(path) > MAX_AGE:
            _remove(path)


def _new_run_folder(root, now=None):
    os.makedirs(root, exist_ok=True)
    own = os.path.join(root, "%d-%s" % (os.getpid(), uuid.uuid4().hex))
    os.makedirs(own)
    _sweep(root, own, time.time() if now is None else now)
    return own


def run_folder():
    """This run's folder. The first request sweeps old siblings; later requests reuse the folder."""
    global _RUN
    if _RUN is None:
        _RUN = _new_run_folder(TEMP_ROOT)
    return _RUN


def _git(cwd, *args):
    """Run git and return stdout. A failure raises with git's own stderr in the message."""
    p = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                        *args], cwd=cwd, capture_output=True)
    if p.returncode:
        raise RuntimeError("git %s: %s" % (" ".join(args), p.stderr.decode("utf-8", "replace").strip()))
    return p.stdout


def _head(repo):
    return _git(repo, "rev-parse", "HEAD").decode("ascii").strip()


def _blob(repo, rev, rel):
    return _git(repo, "cat-file", "blob", "%s:%s" % (rev, rel))


def _is_ancestor(repo, a, b):
    return subprocess.run(["git", "merge-base", "--is-ancestor", a, b], cwd=repo,
                          capture_output=True).returncode == 0


def _write(repo, rel, data):
    path = os.path.join(repo, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data.encode("utf-8") if isinstance(data, str) else data)


def _working(repo, rel):
    with open(os.path.join(repo, *rel.split("/")), "rb") as fh:
        return fh.read()


def _expect(cond, why):
    """A fixture precondition. Plain raise, not assert, so python -O cannot strip it."""
    if not cond:
        raise AssertionError(why)


ONBOARDING = '<!doctype html>\n<html><head><meta charset="utf-8"></head><body>x</body></html>\n'
CSS, JS, TPL = "dashboard.css", "dashboard.js", "dashboard_template.html"
CSS_BYTES = b"body { margin: 0 }\n"
JS_BYTES = b"const dash = 'ok';\n"
CO = ' crossorigin="anonymous"'
FAKE_SHA = "f" * 40


def _asset(plugin, name):
    return "plugins/%s/skills/s/assets/%s" % (plugin, name)


def _url(sha, rel):
    return "https://cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables@%s/%s" % (sha, rel)


def _sri(data):
    return "sha384-" + base64.b64encode(hashlib.sha384(data).digest()).decode("ascii")


def _link(sha, rel, sri, co=True):
    return '<link rel="stylesheet" href="%s" integrity="%s"%s>' % (_url(sha, rel), sri, CO if co else "")


def _script(sha, rel, sri, co=True):
    return '<script src="%s" integrity="%s"%s></script>' % (_url(sha, rel), sri, CO if co else "")


def _pair(repo, sha, plugin="p", *, css_sha=None, js_sha=None, js_sri=None, co=True):
    """The link and script pins for one plugin. Defaults are correct: the pinned sha and the
    integrity of the blob at that sha. Each keyword breaks one thing."""
    css, js = _asset(plugin, CSS), _asset(plugin, JS)
    return [_link(css_sha or sha, css, _sri(_blob(repo, sha, css)), co),
            _script(js_sha or sha, js, js_sri or _sri(_blob(repo, sha, js)), co)]


def _quirky(repo, sha, url_sha):
    """One script tag over several lines, single quotes, attributes out of the usual order."""
    js = _asset("p", JS)
    return ["<script",
            "  crossorigin='anonymous'",
            "  integrity='%s'" % _sri(_blob(repo, sha, js)),
            "  src='%s'></script>" % _url(url_sha, js)]


def _base(run, name, crlf=False):
    """One repo: the onboarding page, the checker copy, and both plugins' asset files, committed.
    With crlf, plugin p's dashboard.js is written with CRLF line endings. autocrlf stores it as LF.
    Returns (repo, asset sha)."""
    repo = os.path.join(run, name)
    os.makedirs(repo)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "core.autocrlf", "true")
    _write(repo, "docs/onboarding.html", ONBOARDING)
    with open(CHECKER, "rb") as fh:
        _write(repo, "scripts/shared_blocks.py", fh.read())
    for plugin in ("p", "q"):
        _write(repo, _asset(plugin, CSS), CSS_BYTES)
        js = JS_BYTES.replace(b"\n", b"\r\n") if crlf and plugin == "p" else JS_BYTES
        _write(repo, _asset(plugin, JS), js)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "assets")
    return repo, _head(repo)


def _template_on(repo, lines_by_plugin):
    """Write each plugin's template from its lines, then commit on the current branch."""
    for plugin, lines in lines_by_plugin.items():
        _write(repo, _asset(plugin, TPL),
               '<!doctype html>\n<html><head><meta charset="utf-8"></head>\n<body>\n'
               + "\n".join(lines) + "\n</body></html>\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "template")


def _pinned(run, name, lines_for):
    """Base repo, then one template commit. lines_for(repo, sha) gives plugin p's lines."""
    repo, sha = _base(run, name)
    _template_on(repo, {"p": lines_for(repo, sha)})
    return repo


def _short7(sha):
    return sha[:7]


# ----------------------------------------------------------------- refusals (red on the old code)

def c_short(run):
    return _pinned(run, "short-sha", lambda r, s: _pair(r, s, css_sha=_short7(s), js_sha=_short7(s)))


def c_nonhex(run):
    return _pinned(run, "nonhex-sha", lambda r, s: _pair(r, s, css_sha="z" + s[1:], js_sha="z" + s[1:]))


def c_absent(run):
    return _pinned(run, "absent-sha", lambda r, s: _pair(r, s, css_sha=FAKE_SHA, js_sha=FAKE_SHA))


def c_link_only(run):
    return _pinned(run, "link-only", lambda r, s: _pair(r, s, css_sha=_short7(s)))


def c_apostrophe(run):
    return _pinned(run, "apostrophe",
                   lambda r, s: ["<p>Don't</p>"] + _pair(r, s, css_sha=_short7(s), js_sha=_short7(s)))


def c_comment_string(run):
    return _pinned(run, "comment-string",
                   lambda r, s: ['<script>var marker = "/* open";</script>']
                   + _pair(r, s, css_sha=_short7(s), js_sha=_short7(s)))


def c_template_literal(run):
    return _pinned(run, "template-literal",
                   lambda r, s: ["<script>", "const t = `", "/* never closed", "`;", "</script>"]
                   + _pair(r, s, css_sha=_short7(s), js_sha=_short7(s)))


def c_quirky_bad(run):
    return _pinned(run, "quirky-bad", lambda r, s: _quirky(r, s, _short7(s)))


def c_wrong_hash(run):
    return _pinned(run, "wrong-hash", lambda r, s: _pair(r, s, js_sri=_sri(b"not the stored file")))


def c_no_crossorigin(run):
    return _pinned(run, "no-crossorigin", lambda r, s: _pair(r, s, co=False))


def c_crlf_hash(run):
    repo, sha = _base(run, "crlf-hash", crlf=True)
    js = _asset("p", JS)
    working, stored = _working(repo, js), _blob(repo, sha, js)
    _expect(working != stored, "the working copy has no CRLF to differ from the stored blob")
    _template_on(repo, {"p": _pair(repo, sha, js_sri=_sri(working))})
    return repo


def c_not_ancestor(run):
    repo, _base_sha = _base(run, "not-ancestor")
    _git(repo, "checkout", "-q", "-b", "side")
    _write(repo, "plugins/p/skills/s/notes.txt", "side only\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "side")
    side = _head(repo)
    _git(repo, "checkout", "-q", "main")
    _expect(not _is_ancestor(repo, side, "HEAD"), "the side commit is reachable from HEAD")
    _template_on(repo, {"p": _pair(repo, side)})
    return repo


def c_differ(run):
    repo, base = _base(run, "differ")
    js = _asset("p", JS)
    _write(repo, js, "const dash = 'edited';\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "edit js")
    _expect(_is_ancestor(repo, base, "HEAD"), "the pinned commit is not an ancestor of HEAD")
    _expect(_blob(repo, base, js) != _blob(repo, "HEAD", js), "the edit did not change the blob")
    _template_on(repo, {"p": _pair(repo, base)})
    return repo


def c_quirky_good_lines(run):
    return _pinned(run, "quirky-good", lambda r, s: _quirky(r, s, s))


# ----------------------------------------------------------------- controls (green on the old code)

def c_no_tags(run):
    repo, _sha = _base(run, "no-tags")
    _template_on(repo, {"p": ["<p>No CDN tags here.</p>"]})
    return repo


def c_full_size(run):
    repo, sha = _base(run, "full-size")
    _template_on(repo, {"p": _pair(repo, sha), "q": _pair(repo, sha, "q")})
    return repo


def c_crlf_correct(run):
    repo, sha = _base(run, "crlf-correct", crlf=True)
    _template_on(repo, {"p": _pair(repo, sha)})
    return repo


def c_comment_url(run):
    def lines(repo, sha):
        js = _asset("p", JS)
        bad = _script(_short7(sha), js, _sri(_blob(repo, sha, js)))
        return ["<!-- " + bad + " -->"] + _pair(repo, sha)
    return _pinned(run, "comment-url", lines)


def c_js_string_url(run):
    def lines(repo, sha):
        return ['<script>const old = "%s";</script>' % _url(_short7(sha), _asset("p", JS))] + _pair(repo, sha)
    return _pinned(run, "js-string-url", lines)


# ----------------------------------------------------------------- shallow (unknown, not fail)

def c_shallow(run):
    origin, base = _base(run, "origin")
    _template_on(origin, {"p": _pair(origin, base)})
    shallow = os.path.join(run, "shallow")
    _git(run, "clone", "-q", "--depth", "1", Path(origin).as_uri(), shallow)
    _expect(_git(shallow, "rev-parse", "--is-shallow-repository").strip() == b"true",
            "the clone is not shallow")
    _expect(subprocess.run(["git", "cat-file", "-e", base + "^{commit}"], cwd=shallow,
                           capture_output=True).returncode != 0,
            "the pinned sha is readable in the shallow clone")
    return shallow


# ----------------------------------------------------------------- the runner

def _check(repo):
    p = subprocess.run([sys.executable, os.path.join(repo, "scripts", "shared_blocks.py"), "--check"],
                       cwd=repo, capture_output=True)
    return p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")


def _verdict(rc, out, want):
    """None when the case holds, else one line naming the cause."""
    if "Traceback" in out:
        return "crashed: " + out.strip().splitlines()[-1]
    kind = want[0]
    if kind == "refuse":
        if rc != 1:
            return "not refused: exit %d, want 1" % rc
        return None if want[1] in out else "refused for another cause: no %r in the output" % want[1]
    if kind == "pass":
        return None if rc == 0 else "refused a correct page: exit %d" % rc
    if rc != 0:
        return "failed where it should only note: exit %d, want 0" % rc
    return None if "unknown" in out else "the output does not say unknown"


CASES = [
    ("short sha (7 hex) on both tags is refused", c_short, ("refuse", "40 hex")),
    ("sha with one non-hex character is refused", c_nonhex, ("refuse", "40 hex")),
    ("sha absent from a full clone is refused as not existing", c_absent, ("refuse", "does not exist")),
    ("pin on a side commit that is not an ancestor of HEAD is refused", c_not_ancestor,
     ("refuse", "ancestor")),
    ("asset edited at HEAD after its pin is refused as differing", c_differ, ("refuse", "differ")),
    ("integrity that is not the sha384 of the stored blob is refused", c_wrong_hash, ("refuse", "sha384")),
    ("integrity taken from the CRLF working copy is refused (blob is LF)", c_crlf_hash,
     ("refuse", "sha384")),
    ("missing crossorigin is refused", c_no_crossorigin, ("refuse", "crossorigin")),
    ("short sha on a link tag alone is refused (link tags are scanned)", c_link_only,
     ("refuse", "40 hex")),
    ("bad pin after a lone apostrophe in text is still refused", c_apostrophe, ("refuse", "40 hex")),
    ("bad pin after a comment opener in a JS string is still refused", c_comment_string,
     ("refuse", "40 hex")),
    ("bad pin after a multi-line template literal with a comment opener is still refused",
     c_template_literal, ("refuse", "40 hex")),
    ("bad pin in a multi-line single-quoted tag with reordered attributes is refused", c_quirky_bad,
     ("refuse", "40 hex")),
    ("control: template with no CDN tags passes (today's state)", c_no_tags, ("pass",)),
    ("control: full-size template, two plugins, script and link pins, passes", c_full_size, ("pass",)),
    ("control: correct pin on a CRLF working copy passes (blob is hashed)", c_crlf_correct, ("pass",)),
    ("control: a bad URL inside an HTML comment is not a tag and passes", c_comment_url, ("pass",)),
    ("control: a bad URL inside a JS string is not a tag and passes", c_js_string_url, ("pass",)),
    ("control: correct pin in a multi-line single-quoted tag passes", c_quirky_good_lines, ("pass",)),
    ("shallow clone that cannot read the pinned sha reports unknown, not fail", c_shallow,
     ("unknown",)),
]


# ----------------------------------------------------------------- the sweep proof

def _sibling(root, mtime):
    path = os.path.join(root, "4242-%s" % uuid.uuid4().hex)
    os.makedirs(path)
    os.utime(path, (mtime, mtime))
    return path


def _sweep_root(run, name):
    root = os.path.join(run, name)
    os.makedirs(root)
    return root


def s_old_goes(run):
    root = _sweep_root(run, "sweep-old")
    old = _sibling(root, FIXED_NOW - 2 * DAY)
    _new_run_folder(root, now=FIXED_NOW)
    return None if not os.path.exists(old) else "a run folder two days old survived the sweep"


def s_new_stays(run):
    root = _sweep_root(run, "sweep-new")
    new = _sibling(root, FIXED_NOW - 60)
    _new_run_folder(root, now=FIXED_NOW)
    return None if os.path.isdir(new) else "a run folder one minute old was removed"


def s_own_stays(run):
    root = _sweep_root(run, "sweep-own")
    own = _new_run_folder(root, now=FIXED_NOW)
    return None if os.path.isdir(own) else "the sweep removed the run's own folder"


SWEEP = [
    ("sweep removes a run folder over a day old", s_old_goes),
    ("sweep keeps a run folder under a day old", s_new_stays),
    ("sweep never removes the folder the run owns", s_own_stays),
]


def main():
    run = run_folder()
    failed = []
    try:
        for name, build, want in CASES:
            try:
                repo = build(run)
            except AssertionError as exc:
                failed.append("%s: fixture: %s" % (name, exc))
                continue
            except Exception as exc:  # a setup crash is a failed case, and the run goes on
                failed.append("%s: fixture raised %r" % (name, exc))
                continue
            rc, out = _check(repo)
            problem = _verdict(rc, out, want)
            if problem:
                failed.append("%s: %s" % (name, problem))
        for name, case in SWEEP:
            problem = case(run)
            if problem:
                failed.append("%s: %s" % (name, problem))
    finally:
        _remove(run)
    if failed:
        print("FAILED (%d):" % len(failed))
        for line in failed:
            print("  - " + line)
        sys.exit(1)
    print("OK: %d asset-pin case(s) and %d sweep case(s)" % (len(CASES), len(SWEEP)))


if __name__ == "__main__":
    main()
