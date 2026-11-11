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
- Ruling 2026-11-11: CDN URLs anywhere in a shell are checked, including inside a <script> body. A
  shell's external <script src> and <link href> must be the pin URL, or the placeholder @__PIN_SHA__
  with integrity __PIN_CSS_SRI__ (link) or __PIN_JS_SRI__ (script). The placeholder passes with a note
  containing "unpinned". A CSS @import in a shell is refused always, pinned or placeholder (ruling
  2026-11-11): the shells never use one. Refusal keywords:
    a URL that is not the pin form (no ref, //, http://, other repo, other host, leading space)
                              "pinned form"
    a branch ref (@main) ..... "40 hex"
    a CSS @import ............ "@import"
- assets/dashboard.js or dashboard.css holding a URL on cdn.jsdelivr.net, unpkg.com, cdnjs.cloudflare.com
  or esm.sh is refused with "from a CDN".
- `shared_blocks.py --pin <sha>` fills every placeholder in a tag, keeps exactly one integrity attribute on
  an unquoted tag, and exits non-zero with "No pinned or placeholder tag found" on a page with no tag.
- A pin path is URL-decoded: %20 is a space in the file name.
- A shell tag (placeholder or pinned) whose path is not a file in that shell's own assets directory is
  refused with "own assets": a path to another plugin's file, or to a missing file.
- Any @import in an assets .css file is refused with "@import". So is a minified @import"x.css" (no
  space) in a shell <style>.
- validate.py runs the pin check: a bad pin makes it exit 1 and name the cause.
"""
import base64
import hashlib
import io
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import uuid
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)  # the checkout this file lives in: its HEAD is what validate.py reads
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
PLACEHOLDER = "__PIN_SHA__"


def _asset(plugin, name):
    return "plugins/%s/skills/s/assets/%s" % (plugin, name)


def _url(sha, rel):
    return "https://cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables@%s/%s" % (sha, rel)


def _sri(data):
    return "sha384-" + base64.b64encode(hashlib.sha384(data).digest()).decode("ascii")


def _link_at(url, sri, co=True):
    return '<link rel="stylesheet" href="%s" integrity="%s"%s>' % (url, sri, CO if co else "")


def _script_at(url, sri, co=True):
    return '<script src="%s" integrity="%s"%s></script>' % (url, sri, CO if co else "")


def _link(sha, rel, sri, co=True):
    return _link_at(_url(sha, rel), sri, co)


def _script(sha, rel, sri, co=True):
    return _script_at(_url(sha, rel), sri, co)


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


def _no_ref(_sha, rel):
    return "https://cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables/%s" % rel


def _other_repo(sha, rel):
    return "https://cdn.jsdelivr.net/gh/ssemwal-cdc/other-repo@%s/%s" % (sha, rel)


def _other_host(sha, rel):
    return "https://unpkg.com/ssemwal-cdc/claude-sharables@%s/%s" % (sha, rel)


def _protocol_relative(sha, rel):
    return "//cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables@%s/%s" % (sha, rel)


def _plain_http(sha, rel):
    return "http://cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables@%s/%s" % (sha, rel)


def _leading_space(sha, rel):
    return " " + _url(sha, rel)


def _branch(_sha, rel):
    return _url("main", rel)


def _placeholder(_sha, rel):
    return _url(PLACEHOLDER, rel)


def _import(url):
    return '<style>@import url("%s");</style>' % url


def _bad_script(repo, sha, url_of):
    """A script tag for plugin p's dashboard.js. Only the url is broken; the integrity is correct."""
    js = _asset("p", JS)
    return _script_at(url_of(sha, js), _sri(_blob(repo, sha, js)))


def _bad_link(repo, sha, url_of):
    """A link tag for plugin p's dashboard.css. Only the url is broken; the integrity is correct."""
    css = _asset("p", CSS)
    return _link_at(url_of(sha, css), _sri(_blob(repo, sha, css)))


def c_no_ref(run):
    return _pinned(run, "no-ref", lambda r, s: [_bad_script(r, s, _no_ref)])


def c_leading_space(run):
    return _pinned(run, "leading-space", lambda r, s: [_bad_script(r, s, _leading_space)])


def c_protocol_relative(run):
    return _pinned(run, "protocol-relative", lambda r, s: [_bad_script(r, s, _protocol_relative)])


def c_plain_http(run):
    return _pinned(run, "plain-http", lambda r, s: [_bad_link(r, s, _plain_http)])


def c_other_repo(run):
    return _pinned(run, "other-repo", lambda r, s: [_bad_script(r, s, _other_repo)])


def c_other_host(run):
    return _pinned(run, "other-host", lambda r, s: [_bad_script(r, s, _other_host)])


def c_import_branch(run):
    return _pinned(run, "import-branch", lambda r, s: [_import(_branch(s, _asset("p", CSS)))])


def c_import_no_ref(run):
    return _pinned(run, "import-no-ref", lambda r, s: [_import(_no_ref(s, _asset("p", CSS)))])


def c_import_pinned(run):
    """A CSS @import with the correct pin. Refused anyway: a shell never carries one (ruling 2026-11-11)."""
    return _pinned(run, "import-pinned", lambda r, s: [_import(_url(s, _asset("p", CSS)))])


def c_hidden_by_attr(run):
    """A comment opener inside a quoted attribute of a tag that is not script or link. The bad tag
    after it sits between that opener and the next comment closer, so a scan that starts a comment
    there hides the bad tag."""
    return _pinned(run, "hidden-by-attr",
                   lambda r, s: ['<div title="<!--">x</div>', _bad_script(r, s, _branch), "<!-- end -->"])


def _asset_case(name, rel, body):
    """A shell with no tags beside one asset file whose body is given. The asset is committed, so
    it is the file at HEAD as well as in the working copy."""
    def build(run):
        repo, _sha = _base(run, name)
        _write(repo, rel, body)
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "asset with a URL")
        _template_on(repo, {"p": ["<p>shell</p>"]})
        return repo
    return build


CDN_HOSTS = [
    ("jsdelivr", "https://cdn.jsdelivr.net/npm/left-pad@1.3.0/index.js"),
    ("unpkg", "https://unpkg.com/left-pad@1.3.0/index.js"),
    ("cdnjs", "https://cdnjs.cloudflare.com/ajax/libs/left-pad/1.3.0/index.js"),
    ("esm", "https://esm.sh/left-pad@1.3.0"),
]


# ----------------------------------------------------------------- placeholders (ok with a note)

def c_placeholder_tags(run):
    return _pinned(run, "placeholder-tags", lambda r, s: [
        _link_at(_placeholder(s, _asset("p", CSS)), "__PIN_CSS_SRI__"),
        _script_at(_placeholder(s, _asset("p", JS)), "__PIN_JS_SRI__")])


def c_placeholder_import(run):
    return _pinned(run, "placeholder-import",
                   lambda r, s: [_import(_placeholder(s, _asset("p", CSS)))])


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
    """A short-sha URL inside a <script> body. The 2026-11-11 ruling checks CDN URLs anywhere in a
    shell, so this is refused, not passed as a non-tag."""
    def lines(repo, sha):
        return ['<script>const old = "%s";</script>' % _url(_short7(sha), _asset("p", JS))] + _pair(repo, sha)
    return _pinned(run, "js-string-url", lines)


def c_pct20(run):
    """A pin whose path holds %20: the file is named with a space, so the URL must decode to resolve."""
    repo, _base_sha = _base(run, "pct20")
    rel = _asset("p", "my dashboard.js")
    _write(repo, rel, JS_BYTES)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "asset with a space in its name")
    sha = _head(repo)
    url = _url(sha, rel.replace(" ", "%20"))
    _template_on(repo, {"p": [_script_at(url, _sri(_blob(repo, sha, rel)))]})
    return repo


def c_cross_placeholder(run):
    """A placeholder tag whose path is plugin q's dashboard.js, in plugin p's shell."""
    return _pinned(run, "cross-placeholder", lambda r, s: [
        _script_at(_placeholder(s, _asset("q", JS)), "__PIN_JS_SRI__")])


def c_cross_pinned(run):
    """A correct pin, but to plugin q's dashboard.js, in plugin p's shell."""
    return _pinned(run, "cross-pinned", lambda r, s: [
        _script_at(_url(s, _asset("q", JS)), _sri(_blob(r, s, _asset("q", JS))))])


def c_missing_placeholder(run):
    """A placeholder tag whose path names a file that is not in plugin p's assets."""
    return _pinned(run, "missing-placeholder", lambda r, s: [
        _script_at(_placeholder(s, _asset("p", "nope.js")), "__PIN_JS_SRI__")])


def c_missing_pinned(run):
    """A pin to a path that is no file at that sha, in plugin p's assets."""
    return _pinned(run, "missing-pinned", lambda r, s: [
        _script_at(_url(s, _asset("p", "nope.js")), _sri(b""))])


def c_import_minified(run):
    """A minified @import with no space after the keyword, in a shell's own style body."""
    return _pinned(run, "import-minified", lambda r, s: ['<style>@import"x.css";</style>'])


def c_style_plain(run):
    """A shell style body with no @import: the control for the minified case."""
    return _pinned(run, "style-plain", lambda r, s: ["<style>body { margin: 0 }</style>"])


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


def _first_refusal(out):
    """The first refusal line the check printed, so a failure names what it refused."""
    for line in out.splitlines():
        if line.startswith("  - "):
            return line[4:]
    return "no refusal line in the output"


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
        return None if rc == 0 else "refused a correct page: exit %d (%s)" % (rc, _first_refusal(out))
    if kind == "unpinned":
        if rc != 0:
            return "refused a placeholder pin: exit %d (%s)" % (rc, _first_refusal(out))
        return None if "unpinned" in out else "the placeholder pin gives no note that says unpinned"
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
    ("a bad URL inside a JS string in the shell is refused (ruling 2026-11-11: CDN URLs anywhere)",
     c_js_string_url, ("refuse", "40 hex")),
    ("script src with no ref is refused", c_no_ref, ("refuse", "pinned form")),
    ("script src with a leading space in its URL is refused", c_leading_space, ("refuse", "pinned form")),
    ("script src that is protocol-relative (//) is refused", c_protocol_relative, ("refuse", "pinned form")),
    ("link href on http:// is refused", c_plain_http, ("refuse", "pinned form")),
    ("script src pinned in another repo is refused", c_other_repo, ("refuse", "pinned form")),
    ("script src on another CDN host (unpkg.com) is refused", c_other_host, ("refuse", "pinned form")),
    ("CSS @import on a branch ref (@main) in a style body is refused", c_import_branch, ("refuse", "40 hex")),
    ("CSS @import with no ref in a style body is refused", c_import_no_ref, ("refuse", "pinned form")),
    ("CSS @import with a correct pin is refused", c_import_pinned, ("refuse", "@import")),
    ("a <!-- inside a quoted attribute does not hide a later bad tag", c_hidden_by_attr,
     ("refuse", "40 hex")),
    ("placeholder pin on script and link is ok with an unpinned note", c_placeholder_tags, ("unpinned",)),
    ("placeholder pin in a CSS @import is refused", c_placeholder_import, ("refuse", "@import")),
    ("dashboard.js with a jsdelivr URL string is refused", _asset_case("js-jsdelivr", _asset("p", JS),
     'fetch("%s");\n' % CDN_HOSTS[0][1]), ("refuse", "from a CDN")),
    ("dashboard.js with an unpkg URL string is refused", _asset_case("js-unpkg", _asset("p", JS),
     'fetch("%s");\n' % CDN_HOSTS[1][1]), ("refuse", "from a CDN")),
    ("dashboard.js with a cdnjs URL string is refused", _asset_case("js-cdnjs", _asset("p", JS),
     'fetch("%s");\n' % CDN_HOSTS[2][1]), ("refuse", "from a CDN")),
    ("dashboard.js with an esm.sh URL string is refused", _asset_case("js-esm", _asset("p", JS),
     'fetch("%s");\n' % CDN_HOSTS[3][1]), ("refuse", "from a CDN")),
    ("dashboard.css with a jsdelivr URL string is refused", _asset_case(
        "css-jsdelivr", _asset("p", CSS),
        '@import url("https://cdn.jsdelivr.net/npm/normalize.css@8.0.1/normalize.css");\n'),
     ("refuse", "from a CDN")),
    ("asset path with %20 resolves to the file with a space in its name", c_pct20, ("pass",)),
    ("control: template with no CDN tags passes (today's state)", c_no_tags, ("pass",)),
    ("control: full-size template, two plugins, script and link pins, passes", c_full_size, ("pass",)),
    ("control: correct pin on a CRLF working copy passes (blob is hashed)", c_crlf_correct, ("pass",)),
    ("control: a bad URL inside an HTML comment is not a tag and passes", c_comment_url, ("pass",)),
    ("control: correct pin in a multi-line single-quoted tag passes", c_quirky_good_lines, ("pass",)),
    ("control: dashboard.js with no CDN URL string passes", _asset_case(
        "js-no-url", _asset("p", JS), 'const note = "loads nothing from a CDN";\nfetch("records.json");\n'),
     ("pass",)),
    ("placeholder tag on another plugin's dashboard.js is refused (not in this shell's own assets)",
     c_cross_placeholder, ("refuse", "own assets")),
    ("pinned tag on another plugin's dashboard.js is refused (not in this shell's own assets)",
     c_cross_pinned, ("refuse", "own assets")),
    ("placeholder tag on a missing file is refused (not in this shell's own assets)",
     c_missing_placeholder, ("refuse", "own assets")),
    ("pinned tag on a missing file is refused (not in this shell's own assets)",
     c_missing_pinned, ("refuse", "own assets")),
    ("dashboard.css with a quoted @import is refused", _asset_case(
        "css-import-quoted", _asset("p", CSS), '@import "base.css";\nbody { margin: 0 }\n'),
     ("refuse", "@import")),
    ("dashboard.css with a url() @import is refused", _asset_case(
        "css-import-url", _asset("p", CSS), '@import url(base.css);\n'), ("refuse", "@import")),
    ("control: dashboard.css with no @import passes", _asset_case(
        "css-plain", _asset("p", CSS), "body { margin: 1px }\n"), ("pass",)),
    ("minified @import\"x.css\" in a shell style is refused", c_import_minified, ("refuse", "@import")),
    ("control: a shell style body with no @import passes", c_style_plain, ("pass",)),
    ("shallow clone that cannot read the pinned sha reports unknown, not fail", c_shallow,
     ("unknown",)),
]


# ----------------------------------------------------------------- --pin and validate.py

def _pin(repo, sha):
    p = subprocess.run([sys.executable, os.path.join(repo, "scripts", "shared_blocks.py"), "--pin", sha],
                       cwd=repo, capture_output=True)
    return p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")


def _tpl(repo):
    return _working(repo, _asset("p", TPL)).decode("utf-8")


def _pin_then_check(run, name, lines_for):
    """Placeholders in plugin p's shell, then --pin the base sha, then --check. None or one cause."""
    repo, sha = _base(run, name)
    _template_on(repo, {"p": lines_for(sha)})
    _expect("__PIN_" in _tpl(repo), "the template has no placeholder to fill")
    rc, out = _pin(repo, sha)
    if "Traceback" in out:
        return "--pin crashed: " + out.strip().splitlines()[-1]
    if rc != 0:
        return "--pin exit %d, want 0" % rc
    left = sorted(set(re.findall(r"__PIN_[A-Z_]+__", _tpl(repo))))
    if left:
        return "--pin left placeholders unfilled: %s" % ", ".join(left)
    rc, out = _check(repo)
    return _verdict(rc, out, ("pass",))


def p_fills_tags(run):
    return _pin_then_check(run, "pin-fills-tags", lambda s: [
        _link_at(_placeholder(s, _asset("p", CSS)), "__PIN_CSS_SRI__"),
        _script_at(_placeholder(s, _asset("p", JS)), "__PIN_JS_SRI__")])


def p_unquoted_integrity(run):
    repo, sha = _base(run, "pin-unquoted")
    _template_on(repo, {"p": ['<script src="%s" integrity=__PIN_JS_SRI__ crossorigin="anonymous"></script>'
                              % _placeholder(sha, _asset("p", JS))]})
    _expect(_tpl(repo).count("integrity") == 1, "the unquoted tag does not carry exactly one integrity")
    rc, out = _pin(repo, sha)
    if "Traceback" in out:
        return "--pin crashed: " + out.strip().splitlines()[-1]
    if rc != 0:
        return "--pin exit %d, want 0" % rc
    n = _tpl(repo).count("integrity")
    return None if n == 1 else "%d integrity attributes after --pin, want 1" % n


def p_no_tags(run):
    repo, sha = _base(run, "pin-no-tags")
    _template_on(repo, {"p": ["<p>No CDN tags here.</p>"]})
    rc, out = _pin(repo, sha)
    if "Traceback" in out:
        return "--pin crashed: " + out.strip().splitlines()[-1]
    if rc == 0:
        return "--pin exit 0 on a page with no pinned tag, want non-zero"
    return None if "No pinned or placeholder tag found" in out else (
        "refused for another cause: no 'No pinned or placeholder tag found' in the output")


VALIDATE_ASSETS = "plugins/netsuite-approval-review/skills/netsuite-approval-double-check/assets"


def _tree_copy(run, name):
    """This checkout's HEAD tree, as a repo of its own. validate.py finds its repo from its own path
    and reads the whole tree, so the cases run the real validate.py on a git archive of HEAD (a
    snapshot made per run, never a stored copy). The archive carries no .git; the copy gets one base commit."""
    dest = os.path.join(run, name)
    os.makedirs(dest)
    data = _git(REPO_ROOT, "archive", "--format=tar", "HEAD")
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        if hasattr(tarfile, "data_filter"):
            tf.extractall(dest, filter="data")
        else:
            tf.extractall(dest)
    _git(dest, "init", "-q", "-b", "main")
    _git(dest, "add", "-A")
    _git(dest, "commit", "-q", "-m", "tree")
    return dest


def _probe(run, name, short):
    """The HEAD tree with two probe assets in a real plugin, and a shell pinned to them. The pin is the
    short sha when short, else the full sha."""
    dest = _tree_copy(run, name)
    d = VALIDATE_ASSETS
    _write(dest, d + "/pin_probe.js", JS_BYTES)
    _write(dest, d + "/pin_probe.css", CSS_BYTES)
    _git(dest, "add", "-A")
    _git(dest, "commit", "-q", "-m", "probe assets")
    sha = _head(dest)
    pin = _short7(sha) if short else sha
    html = ('<!doctype html>\n<html><head><meta charset="utf-8"></head>\n<body>\n'
            + _link(pin, d + "/pin_probe.css", _sri(CSS_BYTES)) + "\n"
            + _script(pin, d + "/pin_probe.js", _sri(JS_BYTES)) + "\n</body></html>\n")
    _write(dest, d + "/pin_probe.html", html)
    _git(dest, "add", "-A")
    _git(dest, "commit", "-q", "-m", "probe template")
    return dest


def _validate(repo):
    p = subprocess.run([sys.executable, os.path.join(repo, "scripts", "validate.py")], cwd=repo,
                       capture_output=True)
    return p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")


def v_short_pin(run):
    rc, out = _validate(_probe(run, "validate-short", short=True))
    return _verdict(rc, out, ("refuse", "40 hex"))


def v_good_pin(run):
    rc, out = _validate(_probe(run, "validate-good", short=False))
    return _verdict(rc, out, ("pass",))


PINS = [
    ("control: --pin fills the tag placeholders, then --check passes", p_fills_tags),
    ("--pin keeps exactly one integrity attribute on an unquoted integrity", p_unquoted_integrity),
    ("--pin on a page with no pinned tag exits non-zero", p_no_tags),
    ("validate.py exits 1 on a short pin and names it", v_short_pin),
    ("control: validate.py passes a correct pin on the same tree", v_good_pin),
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
        for name, case in PINS:
            try:
                problem = case(run)
            except AssertionError as exc:
                failed.append("%s: fixture: %s" % (name, exc))
                continue
            except Exception as exc:
                failed.append("%s: fixture raised %r" % (name, exc))
                continue
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
    print("OK: %d asset-pin case(s), %d pin and validate case(s) and %d sweep case(s)"
          % (len(CASES), len(PINS), len(SWEEP)))


if __name__ == "__main__":
    main()
