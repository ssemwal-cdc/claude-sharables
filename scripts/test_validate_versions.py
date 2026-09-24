#!/usr/bin/env python3
"""Check the plugin.json tail and README row rules in validate.py (D43, G17).

    python3 scripts/test_validate_versions.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from version_tails import plugin_tail_problems, readme_row_problems

A, B = ("alpha", 2, "2026-09-01"), ("beta", 5, "2026-09-10")
BOTH = "Does a thing. alpha skill version 2 — 2026-09-01. beta skill version 5 — 2026-09-10."

# (a) two skills, both tails present and in order
assert plugin_tail_problems(BOTH, [A, B]) == [], plugin_tail_problems(BOTH, [A, B])

# (b) one tail missing: the problem names that skill
p = plugin_tail_problems("Does a thing. alpha skill version 2 — 2026-09-01.", [A, B])
assert p and all("beta" in m for m in p), p

# (c) one tail stale
p = plugin_tail_problems(BOTH.replace("beta skill version 5", "beta skill version 4"), [A, B])
assert p and any("beta" in m for m in p), p

# out of order
p = plugin_tail_problems(
    "Does a thing. beta skill version 5 — 2026-09-10. alpha skill version 2 — 2026-09-01.", [A, B])
assert p, p

# (d) single-skill form unchanged
assert plugin_tail_problems("Does a thing. Skill version 2 — 2026-09-01.", [A]) == []
assert plugin_tail_problems("Does a thing. Skill version 1 — 2026-09-01.", [A])
assert readme_row_problems(["| `p` | v2 | x |"], [("alpha", 2)]) == []

# (e) README row for a multi-skill plugin
row = ["| `p` | alpha v2, beta v5 | x |"]
assert readme_row_problems(row, [("alpha", 2), ("beta", 5)]) == []
p = readme_row_problems(["| `p` | alpha v2 | x |"], [("alpha", 2), ("beta", 5)])
assert p and all("beta" in m for m in p), p
p = readme_row_problems(["| `p` | alpha v2, beta v4 | x |"], [("alpha", 2), ("beta", 5)])
assert p and all("beta" in m for m in p), p

print("OK: version tail and README row checks passed")
