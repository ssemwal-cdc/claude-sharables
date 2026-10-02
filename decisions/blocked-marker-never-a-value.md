---
id: D21
slug: blocked-marker-never-a-value
kind: decision
status: settled
date: 2026-10-02
---
# Never trust a blocked marker

**Rule.** Never let a blocked marker reach a verdict, a comment or a dashboard, and never read it as empty. Compare the figure inside the page and return only the result. A match comes back as true or false, or the figure comes back parsed to a number. A field still blanked after that is unreadable. Report it by name as a failure.

**Outcome protected.** A redacted figure is read again instead of read as empty.

**Argument.**

A blocked marker is never a value.

The old remedy here was to re-return the redacted field in another shape and read it again. That remedy is retired. It is the disguise that D‹no-filter-evasion›, a skill never shapes its way past a filter, bars. The session's own safety check refused a call that did exactly this, tagged `[Auto-Mode Bypass]`. See F‹charcode-fetch-refused›, the safety check refused the reshaped return value.

The fix is not a reshaped return value. Compare the figure where it already sits, inside the page. Hand back only the comparison's result or the figure parsed to a number. Neither one crosses the filter as the raw redacted text.

Whether the filter still blanks a number parsed out of JSON is unmeasured. Say so plainly rather than assume that the parse escapes it.

A field still blocked after a plain, in-page comparison is unreadable. Name it as a failure.

Do not read it as the field being empty. That is the same silent misfile as the rest of these records.

**Evidence.**

- Recorded 2026-08-14 from F23, the filter has a second trigger.
- The first trigger is F15, stub rows trip the filter.
- See F‹charcode-fetch-refused›, measured live 2026-10-02: the safety check refused the reshaped return value, tagged `[Auto-Mode Bypass]`.

**Checks.** none
