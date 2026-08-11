#!/usr/bin/env python3
"""Validate the marketplace, every plugin in it, and the docs that describe them.

Run from the repo root:

    python3 scripts/validate.py

Exits non-zero on the first category of failure. Every rule here exists because
breaking it produced a real, observed failure — see CLAUDE.md for the traps.
"""

import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKETPLACE = os.path.join(REPO, ".claude-plugin", "marketplace.json")
PLUGINS_DIR = os.path.join(REPO, "plugins")

failures = []
notes = []


def fail(msg):
    failures.append(msg)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def frontmatter(path):
    """Return the YAML frontmatter block of a SKILL.md as a dict of top-level keys."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None, text
    keys = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            keys[km.group(1)] = km.group(2)
    return keys, text


# ---------------------------------------------------------------- marketplace
if not os.path.isfile(MARKETPLACE):
    print("FATAL: .claude-plugin/marketplace.json is missing")
    sys.exit(1)

mkt = load(MARKETPLACE)

if "metadata" in mkt and "pluginRoot" in mkt.get("metadata", {}):
    fail(
        "marketplace.json sets metadata.pluginRoot. It does not work: sources "
        "resolve from the repo root regardless, and the install fails with "
        "'Source path does not exist'. Spell each source out as ./plugins/<name>."
    )

entries = mkt.get("plugins", [])
if not entries:
    fail("marketplace.json has no plugins array, or it is empty")

REPO_URL = "https://github.com/ssemwal-cdc/claude-sharables.git"

registered = {}
for e in entries:
    name = e.get("name")
    src = e.get("source")
    if not name:
        fail(f"marketplace entry missing 'name': {e}")
        continue

    if "version" in e:
        fail(
            f"[{name}] marketplace entry sets 'version'. Remove it: version must "
            f"resolve from the commit SHA or pushes stop shipping."
        )

    # Sources must be git-subdir objects. A bare relative-path string still installs
    # from the CLI, but only because the CLI clones the whole repo; surfaces that
    # hold marketplace.json alone cannot resolve it. See CLAUDE.md.
    if isinstance(src, str):
        fail(
            f"[{name}] source is the relative-path string {src!r}. Use a git-subdir "
            f"object instead — a relative path only resolves where the whole repo has "
            f"been cloned, so the desktop/settings install path cannot use it."
        )
        continue
    if not isinstance(src, dict):
        fail(f"[{name}] 'source' must be a git-subdir object, got {type(src).__name__}")
        continue
    if src.get("source") != "git-subdir":
        fail(f"[{name}] source type is {src.get('source')!r}; this repo uses 'git-subdir'")
        continue
    if src.get("url") != REPO_URL:
        fail(f"[{name}] source url is {src.get('url')!r}; expected {REPO_URL}")
    path = src.get("path", "")
    if not path or path.startswith("/") or path.startswith("./"):
        fail(
            f"[{name}] source path {path!r} must be a bare repo-relative path "
            f"like 'plugins/<name>' — no leading './' or '/'"
        )
        continue
    if "version" in src or "sha" in src:
        fail(
            f"[{name}] source pins a version/sha. Leave it unpinned so the plugin "
            f"tracks the default branch and every push ships."
        )
    registered[name] = "./" + path

# ------------------------------------------------------------------- plugins
on_disk = sorted(
    d for d in os.listdir(PLUGINS_DIR)
    if os.path.isdir(os.path.join(PLUGINS_DIR, d)) and not d.startswith("_")
)

for name, src in registered.items():
    root = os.path.normpath(os.path.join(REPO, src))
    if not os.path.isdir(root):
        fail(f"[{name}] source {src} does not resolve to a directory")
        continue

    manifest = os.path.join(root, ".claude-plugin", "plugin.json")
    if not os.path.isfile(manifest):
        fail(f"[{name}] missing {src}/.claude-plugin/plugin.json — the install will fail")
        continue

    pj = load(manifest)
    if pj.get("name") != name:
        fail(
            f"[{name}] plugin.json name is {pj.get('name')!r}; it must match the "
            f"marketplace entry name {name!r}"
        )
    if "version" in pj:
        fail(
            f"[{name}] plugin.json sets 'version'. Remove it: version must resolve "
            f"from the commit SHA or teammates keep their cached copy forever."
        )
    if not pj.get("description"):
        fail(f"[{name}] plugin.json has no description")

    skills_dir = os.path.join(root, "skills")
    if not os.path.isdir(skills_dir):
        fail(f"[{name}] has no skills/ directory")
        continue

    skills = sorted(
        d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))
    )
    if not skills:
        fail(f"[{name}] skills/ is empty")

    for skill in skills:
        sp = os.path.join(skills_dir, skill, "SKILL.md")
        if not os.path.isfile(sp):
            fail(f"[{name}/{skill}] missing SKILL.md")
            continue
        keys, text = frontmatter(sp)
        if keys is None:
            fail(f"[{name}/{skill}] SKILL.md has no YAML frontmatter block")
            continue
        if keys.get("name") != skill:
            fail(
                f"[{name}/{skill}] frontmatter name is {keys.get('name')!r}; it must "
                f"match the directory name {skill!r}"
            )
        if not keys.get("description"):
            fail(f"[{name}/{skill}] frontmatter has no description")

        # Assets must be referenced through ${CLAUDE_PLUGIN_ROOT} and must exist.
        # A reference may point at a file or, in prose, at a directory.
        for ref in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"'`\s)]+)", text):
            target = os.path.join(root, ref)
            if not (os.path.isfile(target) or os.path.isdir(target.rstrip("/"))):
                fail(f"[{name}/{skill}] SKILL.md references missing path: {ref}")

        assets = os.path.join(skills_dir, skill, "assets")
        if os.path.isdir(assets):
            for a in sorted(os.listdir(assets)):
                rel = f"skills/{skill}/assets/{a}"
                if rel not in text:
                    notes.append(f"[{name}/{skill}] asset {a} is never referenced in SKILL.md")

        # A bare relative asset path (no ${CLAUDE_PLUGIN_ROOT}) breaks once installed,
        # because the cwd at run time is the user's workspace, not the plugin.
        for bad in re.findall(r"(?<!\{CLAUDE_PLUGIN_ROOT\}/)(?<![\w/${])assets/[\w.-]+", text):
            fail(
                f"[{name}/{skill}] SKILL.md uses bare path {bad!r}. Asset paths must be "
                f"${{CLAUDE_PLUGIN_ROOT}}/skills/{skill}/{bad} or they break once installed."
            )

# ------------------------------------------------------------------- orphans
for d in on_disk:
    if d not in registered:
        fail(
            f"plugins/{d}/ exists but is not registered in marketplace.json — "
            f"nobody can install it"
        )
for name, src in registered.items():
    folder = src.split("/")[-1]
    if folder not in on_disk:
        fail(f"marketplace registers {name} at {src}, but that folder is not in plugins/")

# ---------------------------------------------------------------- doc drift
# The docs must not disagree with the manifest about which plugins exist.
for doc in ("README.md", "CLAUDE.md"):
    path = os.path.join(REPO, doc)
    if not os.path.isfile(path):
        fail(f"{doc} is missing")
        continue
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    for name in registered:
        if name not in body:
            fail(f"{doc} does not mention plugin {name!r} — docs have drifted from the manifest")
    for mentioned in set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", body)):
        looks_like_plugin = os.path.isdir(os.path.join(PLUGINS_DIR, mentioned))
        if looks_like_plugin and mentioned not in registered:
            fail(f"{doc} references {mentioned!r}, which is not registered in marketplace.json")

# -------------------------------------------------------------------- report
for n in notes:
    print(f"note: {n}")

if failures:
    print(f"\nFAILED ({len(failures)}):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print(f"OK: marketplace {mkt['name']!r}, {len(registered)} plugin(s) validated")
for name, src in sorted(registered.items()):
    skills_dir = os.path.join(REPO, src, "skills")
    skills = sorted(
        d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))
    )
    print(f"  {name}  ->  {src}  (skills: {', '.join(skills)})")
