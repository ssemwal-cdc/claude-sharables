"""The plugin.json tail and README row rules of D43, four synced version sites.

validate.py imports these. scripts/test_validate_versions.py tests them.
A single-skill plugin keeps the one tail `Skill version N — DATE.` and a `vN`
row. A plugin with several skills lists every skill (G17, multi-skill unbuilt).
"""
import re


def plugin_tail_problems(desc, tails):
    """tails: [(skill, n, date)] in sorted skill order. Returns problem strings."""
    desc = desc.rstrip()
    if len(tails) == 1:
        skill, n, vdate = tails[0]
        tail = "Skill version %d — %s." % (n, vdate)
        if desc.endswith(tail):
            return []
        return [f"plugin.json description must end with {tail!r} to match "
                f"{skill}/SKILL.md — bump both in the same commit."]
    each = [(t[0], "%s skill version %d — %s." % t) for t in tails]
    want = " ".join(tail for _, tail in each)
    if desc.endswith(want):
        return []
    out = [f"plugin.json description lacks {tail!r} to match {skill}/SKILL.md "
           f"— bump both in the same commit."
           for skill, tail in each if tail not in desc]
    return out or [f"plugin.json description must end with every skill's tail, in "
                   f"sorted skill order: {want!r}"]


def readme_row_problems(rows, versions):
    """rows: the README table lines for one plugin. versions: [(skill, n)]."""
    if len(versions) == 1:
        skill, n = versions[0]
        if any(f"v{n}" in l for l in rows):
            return []
        return [f"does not say v{n}, but {skill}/SKILL.md says skill version {n}"
                f" — bump both in the same commit"]
    return [f"does not say '{skill} v{n}', but {skill}/SKILL.md says skill version {n}"
            f" — bump both in the same commit"
            for skill, n in versions
            if not any(re.search(rf"(?<![\w-]){re.escape(skill)} v{n}(?!\d)", l) for l in rows)]
