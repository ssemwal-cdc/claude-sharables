---
id: F96
slug: render-read-wall-serialise
kind: finding
status: observed
date: 2026-09-01
---
# Read-side wall, fixed by serialise

**Outcome protected.** A 62-item dashboard fits in one file read.

**Argument.**

A fourth run declined a render, and this one had a real mechanical wall under it.

The excuse was not that the render might truncate on the way out. It was that the harness would not hand over a file that size intact in the first place.

That is a claim about reading the page, before the render tool is reached. The render step argues the output side only, so the run broke a rule that did not cover it.

The claim substantially holds. An indented JSON payload published past the line limit of a default file read, so the tail was not visible.

The fix is cosmetic and the effect is not. Nothing reads that JSON by eye, so the indentation bought nothing while costing the lines that mattered.

`serialise()` is now a shared block in both publish scripts. It emits one compact line per item.

A single line for the whole payload is smaller again and puts most of the file on one line. Per item is bounded on both axes, which is why it is a join and not one dump call.

The run still predicted the wall from a byte count rather than observing a short read. It also handed the file over as the deliverable and never rendered the specified fallback.

**Evidence.**

- Measured 2026-09-01 against a 62-item fixture, 164 KB in the run and 174 KB over 2,834 lines when published with indentation. A default file read shows 2,000 lines.
- The run arithmetic checked out. The template is 55,118 bytes before any data.
- The compact form is 886 lines and 161 KB, longest line 1,780 characters. One single line is 63 bytes smaller and puts 110 KB on one line.
- Restoring indentation fails the build at 3,013 lines.

**Checks.** `test_render_fits_one_read` in `scripts/test_skill_code.py`, mutation-tested in both plugins.
