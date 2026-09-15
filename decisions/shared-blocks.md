---
id: pending
slug: shared-blocks
kind: decision
status: settled
date: 2026-08-24
---
# Sync shared blocks from canonical

**Rule.** Edit the canonical file in `plugins/_shared/`, then run the sync and the check.

**Outcome protected.** A fix reaches both plugins, or the build fails.

**Argument.**

The two plugins carry byte-identical machinery and cannot share it at run time. `${CLAUDE_PLUGIN_ROOT}` resolves per plugin, and a `git-subdir` install ships one plugin folder. Every shipped file must be complete on its own.

What is shared is a maintainer-side canonical copy plus a check. `plugins/_shared/<name>.block` holds the content. Each plugin fences the same content with markers naming the block.

Markers match by name, not by comment syntax. Use `//` in a script block, `#` in Python and an HTML comment in markup.

Run `python3 scripts/shared_blocks.py --sync` to push the canonical content into every marked site. Run `--check` to verify, which is what the build runs.

Editing a shipped copy directly is not wrong. It fails the check until the change moves into the canonical file.

A block must already be byte-identical in both plugins. This mechanism enforces sameness. It does not create it.

A canonical file that nobody references fails the build. So does a marker naming a canonical file that does not exist.

`plugins/_shared/` never ships. `validate.py` skips a directory whose name starts with an underscore, and the folder sits inside no plugin. That underscore is load-bearing.

**Evidence.**

- Measured 2026-08-24. The two dashboard templates were 54.5% line-identical and the two publish scripts 54.9%.
- 10 of the 22 commits that ever touched a `SKILL.md` had to touch both. Every one was a mechanics or convention change.
- 6 defects had accumulated in that gap, each a fix that reached one plugin only. See F‹dashboard-drift-six-defects›, six one-sided defects.
- `SKILL.md` coverage is smaller than the duplication suggests. See F‹skill-md-block-eligibility›, only 34 eligible lines.

**Checks.** `scripts/validate.py` runs `shared_blocks.py --check` on every build.
