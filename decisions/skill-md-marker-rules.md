---
id: D61
slug: skill-md-marker-rules
kind: decision
status: settled
date: 2026-08-24
---
# Place SKILL.md markers on boundaries

**Rule.** Start and end every `SKILL.md` block on a paragraph boundary, and never inside a fenced code block.

**Outcome protected.** A synced block leaves both skills readable and both code fences runnable.

**Argument.**

A marker is a line. In Markdown a comment line dropped inside a paragraph splits that paragraph in two.

So a block must never begin or end mid-sentence, and never inside a numbered list item.

A marker must never land inside a fenced code block. The bash and javascript fences are content.

`scripts/test_skill_code.py` extracts the javascript fences and evaluates them, so a stray marker breaks a test rather than a layout.

**Evidence.**

- Both rules were learned by breaking them in 2026-08.
- The eligibility cost is in F68, only 34 eligible lines.

**Checks.** `shared_blocks.py --check` and `scripts/test_skill_code.py`.
