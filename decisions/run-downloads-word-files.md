---
id: pending
slug: run-downloads-word-files
kind: decision
status: settled
date: 2026-10-05
---
# A run downloads Word files itself

**Rule.** The user opted in on 2026-10-05. A Procore run may open a Word attachment's link, so Chrome saves it into Downloads. The run then reads it there. The files stay. Spreadsheets keep the manual download fallback until the user rules on them.

**Outcome protected.** Word support gets read without the user downloading files by hand.

**Argument.**

Chrome cannot display a `.docx`. A Procore attachment record carries only an id, a name and a signed link. So no read of a Word file avoids a download. The user's earlier rule kept files out of Downloads unless they opted in. This is that opt-in, for Word files only.

**Evidence.**

- Checked live 2026-10-05: a `.docx` attachment record holds the keys `id`, `name` and `url`, and nothing else.
- Whether Chrome saves the file silently or asks where to save it is `unmeasured`. The first run that tries it measures that.

**Checks.** `test_read_docx` in `scripts/test_skill_code.py` runs the Word reader.
