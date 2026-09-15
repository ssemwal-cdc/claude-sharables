---
id: D12
slug: port-skill-verbatim
kind: decision
status: settled
date: 2026-08-11
---
# Port a skill verbatim

**Rule.** Copy a ported skill unchanged. Raise anything that looks wrong instead of editing it.

**Outcome protected.** A skill that worked before the port still works after it.

**Argument.**

Do not edit a ported `SKILL.md` prose to match house style unless asked.

The frontmatter description carries the trigger phrases. Rewriting it changes whether the skill fires.

Prove the copy is faithful with `diff -r <source> plugins/<name>`, which must print nothing.

Strip archive junk before copying. That is `__MACOSX/`, `.DS_Store` and `._*` files.

If a ported skill deviates from house shape, say so rather than normalising it quietly.

**Evidence.**

- Both shipped plugins were ported this way in 2026-08.

**Checks.** `diff -r` by hand. No script compares a port to its source.
