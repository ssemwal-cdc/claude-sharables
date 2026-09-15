---
id: pending
slug: plugin-validate-warning-expected
kind: decision
status: settled
date: 2026-09-15
---
# Record the no-version warning

**Rule.** Record the `No version specified` warning from `claude plugin validate` as expected, and carry on.

**Outcome protected.** A maintainer reads every line a command printed, and knows which line is expected.

**Argument.**

The warning is correct here. D‹no-version-field›, no version field, bans the field the warning asks for.

The instruction used to read `Ignore it`. That told a reader to discard a command output, which the global mandate forbids.

Recording the warning costs one line and keeps the output intact. A future warning that is not this one then stands out.

**Evidence.**

- Changed 2026-09-15 in the prose pass. The former wording sat in `CLAUDE.md` at line 146 as of commit `3775cc8`, the tip of `main` when the pass started.
- No other warning from that command has been observed, so the set of expected warnings is `unmeasured`.

**Checks.** none
