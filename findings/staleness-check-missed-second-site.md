---
id: pending
slug: staleness-check-missed-second-site
kind: finding
status: settled
date: 2026-08-24
---
# Staleness fix was itself stale

**Outcome protected.** A version check compares every site that carries the version, not just
the first.

**Argument.** The staleness check added the previous turn was itself stale.
Procore's Step 0 stated it ships `v5` and then tested for `v4`.
The check written to detect a stale workspace would have called a current one
stale, and would have passed a genuinely stale one.

`check_template_versions()` missed it because `re.search` stops at the first match.
There were two sites carrying the version string.
The check now compares every site.

That is the third instance of one shape.
A check whose inputs fail together only ever looks at one of them.

**Evidence.** Found 2026-08-24, in a nine-agent prose audit.
See `F‹checks-whose-inputs-fail-together›`, the same shape one turn earlier.

**Checks.** none.
