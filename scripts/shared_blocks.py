#!/usr/bin/env python3
"""Canonical source for the blocks both plugins carry verbatim.

The two plugins cannot share code at run time: ${CLAUDE_PLUGIN_ROOT} resolves per
plugin, and a git-subdir install ships only plugins/<name>/, so every shipped file has
to be complete on its own. What they can share is a *maintainer-side* canonical copy
plus a check that the shipped copies still match it.

That matters because the drift is not hypothetical. As of 2026-08-24 the two dashboard
templates were 54.5% line-identical and the two publish scripts 54.9%, kept in step by
hand, and 10 of the 22 commits that ever touched a SKILL.md had to touch both. Six
defects had accumulated in the gap - a fail-open verdict, a never-pruned mark store, a
money card with no rollover - each one a case where one copy learned something and the
other never did. This turns that class of drift into a failed build.

  plugins/_shared/<name>.block   canonical content, exactly as it appears in both files
  <any plugin file>              the same content, fenced by markers naming the block

Markers are matched by name, not by comment syntax, so each site uses whatever comment
is valid there - // in a script block, # in Python, <!-- --> in markup:

    //__SHARED:dash-nav__
    ...content...
    //__END_SHARED:dash-nav__

plugins/_shared/ is invisible to validate.py (it skips names starting with "_") and is
not part of any plugin, so it never ships. Usage:

    python3 scripts/shared_blocks.py --check    # what validate.py runs
    python3 scripts/shared_blocks.py --sync     # push canonical into every marked site
"""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = os.path.join(REPO, "plugins", "_shared")
PLUGINS = os.path.join(REPO, "plugins")
SCAN_EXT = (".html", ".py", ".md", ".css", ".js")

BEGIN = re.compile(r"^(?P<indent>[ \t]*)(?P<pre>.*?)__SHARED:(?P<name>[a-z0-9][a-z0-9-]*)__")
END = re.compile(r"__END_SHARED:(?P<name>[a-z0-9][a-z0-9-]*)__")


def canonical_path(name):
    return os.path.join(SHARED, name + ".block")


def plugin_files():
    """Every candidate file inside a real (non-underscore) plugin."""
    for entry in sorted(os.listdir(PLUGINS)):
        if entry.startswith("_"):
            continue
        root = os.path.join(PLUGINS, entry)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in sorted(filenames):
                if fn.endswith(SCAN_EXT):
                    yield os.path.join(dirpath, fn)


def find_blocks(text, path):
    """Yield (name, start_line, end_line) for each marked region; body is the lines between."""
    lines = text.split("\n")
    open_at = {}
    out = []
    for i, line in enumerate(lines):
        e = END.search(line)
        if e:
            name = e.group("name")
            if name not in open_at:
                raise SystemExit("ABORT: %s line %d closes block %r that was never opened"
                                 % (path, i + 1, name))
            out.append((name, open_at.pop(name), i))
            continue
        b = BEGIN.match(line)
        if b:
            name = b.group("name")
            if name in open_at:
                raise SystemExit("ABORT: %s line %d reopens block %r" % (path, i + 1, name))
            open_at[name] = i
    if open_at:
        raise SystemExit("ABORT: %s never closes block(s): %s"
                         % (path, ", ".join(sorted(open_at))))
    return lines, out


def run(sync=False):
    problems, synced, seen = [], [], {}
    for path in plugin_files():
        rel = os.path.relpath(path, REPO)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if "__SHARED:" not in text:
            continue
        lines, blocks = find_blocks(text, rel)
        changed = False
        for name, a, b in sorted(blocks, key=lambda t: -t[1]):
            cp = canonical_path(name)
            if not os.path.isfile(cp):
                problems.append("%s: block %r has no canonical file at %s"
                                % (rel, name, os.path.relpath(cp, REPO)))
                continue
            with open(cp, encoding="utf-8") as fh:
                want = fh.read()
            want_lines = want.split("\n")
            if want_lines and want_lines[-1] == "":
                want_lines.pop()
            have_lines = lines[a + 1:b]
            seen.setdefault(name, []).append(rel)
            if have_lines == want_lines:
                continue
            if sync:
                lines[a + 1:b] = want_lines
                changed = True
                synced.append("%s: %s" % (rel, name))
            else:
                problems.append(
                    "%s: block %r has drifted from %s\n      %s"
                    % (rel, name, os.path.relpath(cp, REPO),
                       _first_diff(have_lines, want_lines)))
        if sync and changed:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
    return problems, synced, seen


def _first_diff(have, want):
    for i in range(max(len(have), len(want))):
        h = have[i] if i < len(have) else "<missing>"
        w = want[i] if i < len(want) else "<missing>"
        if h != w:
            return "first difference at block line %d:\n        shipped:   %s\n        canonical: %s" % (
                i + 1, h.strip()[:96], w.strip()[:96])
    return "lengths differ"


CDN_PIN = re.compile(r"cdnjs\.cloudflare\.com/ajax/libs/([A-Za-z0-9._-]+)/([0-9][0-9A-Za-z.-]*)")


def check_pins():
    """Both skills load the same libraries from cdnjs; the pinned versions must agree.

    This is deliberately not a shared block. The loaders sit inside ```javascript fences that
    scripts/test_skill_code.py extracts and evaluates, and the two skills wrap them in different
    prose because NetSuite loads pdf.js in the record tab (the media.nl fetch needs the session
    cookie) while Procore loads it in an S3 scratch tab. The surrounding text differs for real
    reasons; only the version may not. A one-sided bump is the drift that matters here - the
    xlsx pin is 0.18.5 specifically, a version whose known CVEs were accepted on the reasoning
    that parsing happens in a session-less tab, and that reasoning is per-plugin.
    """
    pins = {}
    for path in plugin_files():
        rel = os.path.relpath(path, REPO)
        with open(path, encoding="utf-8") as fh:
            for lib, ver in CDN_PIN.findall(fh.read()):
                pins.setdefault(lib, {}).setdefault(ver, set()).add(rel)
    problems = []
    for lib, vers in sorted(pins.items()):
        if len(vers) > 1:
            detail = "; ".join("%s in %s" % (v, ", ".join(sorted(f)))
                               for v, f in sorted(vers.items()))
            problems.append("cdnjs %s is pinned to more than one version - %s. Bump it in both "
                            "plugins or neither." % (lib, detail))
    return problems, {lib: next(iter(v)) for lib, v in pins.items() if len(v) == 1}


SKILL_TPL_VER = re.compile(r"ships layout template `(v\d+)`")
TPL_MARKER = re.compile(r"layout template (v\d+)")
SCRIPT_TPL_VER = re.compile(r'^TEMPLATE_VERSION = "(v\d+)"', re.M)


def check_template_versions():
    """The template version has three sites per plugin and all of them must agree.

    SKILL.md states the expected version; the template carries it as a marker; the publish
    script pins it as a constant. The script/template pair only catches a *torn* sync - both
    files are copied together, so a uniformly stale workspace has them agreeing and publishes
    silently (verified 2026-08-24). SKILL.md is the fixed point that catches that, because it
    always ships with the plugin. Which only works if the number it states is right, hence this.
    """
    problems = []
    for entry in sorted(os.listdir(PLUGINS)):
        if entry.startswith("_"):
            continue
        root = os.path.join(PLUGINS, entry)
        skills = os.path.join(root, "skills")
        if not os.path.isdir(skills):
            continue
        for skill in sorted(os.listdir(skills)):
            sd = os.path.join(skills, skill)
            found = {}
            for label, rel, rx in (
                ("SKILL.md", "SKILL.md", SKILL_TPL_VER),
                ("template", os.path.join("assets", "dashboard_template.html"), TPL_MARKER),
                ("script", os.path.join("assets", "publish_dashboard.py"), SCRIPT_TPL_VER),
            ):
                fp = os.path.join(sd, rel)
                if not os.path.isfile(fp):
                    continue
                with open(fp, encoding="utf-8") as fh:
                    m = rx.search(fh.read())
                if m:
                    found[label] = m.group(1)
            if len(found) < 3:
                if "template" in found or "script" in found:
                    missing = {"SKILL.md", "template", "script"} - set(found)
                    problems.append(
                        "%s/%s: template version stated in %d of 3 sites - missing %s. "
                        "SKILL.md must say \"ships layout template `vN`\" so a stale "
                        "workspace can be detected." % (entry, skill, len(found),
                                                        ", ".join(sorted(missing))))
                continue
            if len(set(found.values())) > 1:
                problems.append(
                    "%s/%s: template version disagrees across its three sites - %s. "
                    "Bump all three together." % (entry, skill,
                        ", ".join("%s=%s" % kv for kv in sorted(found.items()))))
    return problems


VERDICT_ALLOWLIST = re.compile(r'^VERDICTS = \((.*?)\)', re.M | re.S)
VERDICT_TEST = re.compile(r'verdict\s*===?\s*"([a-z]+)"')


def check_verdict_vocabulary():
    """A template may only test verdicts its own publish script can emit.

    Found 2026-08-24 by reading docs against code: Procore's template filtered an "actioned
    bin" on `verdict === "gone"`, which Step 6 never defines and the publish script's VERDICTS
    allowlist would abort on - so the bin had never rendered in any run, and the skill's
    carry-forward rule was retaining items for a UI that could not exist. NetSuite's
    equivalent was dead for a different reason (a never-assigned live-queue variable).

    Both were invisible to every gate: nothing checked that the page's branches were reachable.
    This is that check. It is deliberately narrow - one string compared against one allowlist,
    in the same skill folder - because that is the part a machine can settle.
    """
    problems = []
    for entry in sorted(os.listdir(PLUGINS)):
        if entry.startswith("_"):
            continue
        skills = os.path.join(PLUGINS, entry, "skills")
        if not os.path.isdir(skills):
            continue
        for skill in sorted(os.listdir(skills)):
            assets = os.path.join(skills, skill, "assets")
            script = os.path.join(assets, "publish_dashboard.py")
            tpl = os.path.join(assets, "dashboard_template.html")
            if not (os.path.isfile(script) and os.path.isfile(tpl)):
                continue
            with open(script, encoding="utf-8") as fh:
                m = VERDICT_ALLOWLIST.search(fh.read())
            if not m:
                continue
            allowed = set(re.findall(r'"([a-z]+)"', m.group(1)))
            with open(tpl, encoding="utf-8") as fh:
                tested = set(VERDICT_TEST.findall(fh.read()))
            for bad in sorted(tested - allowed):
                problems.append(
                    "%s/%s: dashboard_template.html branches on verdict %r, which "
                    "publish_dashboard.py's VERDICTS allowlist (%s) can never emit - that "
                    "branch is unreachable. Either add the verdict to the allowlist and to "
                    "SKILL.md's Step 6 vocabulary, or delete the branch."
                    % (entry, skill, bad, ", ".join(sorted(allowed))))
    return problems


def orphan_canonicals(seen):
    if not os.path.isdir(SHARED):
        return []
    return [f for f in sorted(os.listdir(SHARED))
            if f.endswith(".block") and f[:-len(".block")] not in seen]


def main():
    sync = "--sync" in sys.argv
    if not sync and "--check" not in sys.argv:
        sys.exit(__doc__)
    problems, synced, seen = run(sync=sync)
    for name in orphan_canonicals(seen):
        problems.append("plugins/_shared/%s is not referenced by any plugin file" % name)
    pin_problems, pins = check_pins()
    problems += pin_problems
    problems += check_template_versions()
    problems += check_verdict_vocabulary()
    if sync:
        for s in synced:
            print("synced " + s)
        print("%d block(s) written" % len(synced) if synced
              else "nothing to sync - every shipped copy already matches canonical")
    if problems:
        print("\nFAIL: shared blocks out of step\n", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        print("\nFix the canonical file in plugins/_shared/ and run "
              "`python3 scripts/shared_blocks.py --sync`, so the fix reaches both "
              "plugins instead of one.", file=sys.stderr)
        sys.exit(1)
    total = sum(len(v) for v in seen.values())
    print("OK: %d shared block(s) across %d site(s), all matching canonical"
          % (len(seen), total))
    if pins:
        print("    cdnjs pins agree: " + ", ".join("%s %s" % kv for kv in sorted(pins.items())))


if __name__ == "__main__":
    main()
