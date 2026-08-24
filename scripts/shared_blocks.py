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


if __name__ == "__main__":
    main()
