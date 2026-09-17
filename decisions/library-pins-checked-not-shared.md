---
id: D51
slug: library-pins-checked-not-shared
kind: decision
status: settled
date: 2026-08-24
---
# Check library pins, never share

**Rule.** Keep every cdnjs library version identical across plugins. Do not make the loader a shared block.

**Outcome protected.** A library bump reaches both plugins, or the build fails.

**Argument.**

`check_pins()` asserts that every cdnjs library reference agrees across all plugins.

The loaders sit inside javascript fences, which D61, markers on paragraph boundaries, rules out as block sites.

The two skills wrap the loaders in genuinely different prose for real reasons. NetSuite loads pdf.js in the record tab, where the media fetch needs the session cookie. Procore loads it in a scratch tab.

So the surrounding text differs on purpose. Only the version may not.

A one-sided bump is the drift worth catching. `check_pins()` catches it the moment the two plugins' versions disagree. A library both plugins load needs no registration to join this check. A library added to only one plugin is not caught by it.

**Evidence.**

- Today the pins are pdf.js 4.0.379 and xlsx 0.18.5.
- The xlsx pin predates the SheetJS prototype-pollution and ReDoS fixes. See F25, the cdnjs import works.
- Verified 2026-09-17 in a scratch copy, never the real repo tree. Adding a new library to only one plugin's `SKILL.md` left `check_pins()` green. Adding it back with a different version on each side turned it red.

**Checks.** `check_pins()` in `scripts/shared_blocks.py`.
