---
id: pending
slug: withdrawn-uncommitted-fixtures
kind: finding
status: abandoned
date: 2026-08-24
---
# Uncommitted fixtures were withdrawn, not faked

**Outcome protected.** A certification that cannot be reproduced is withdrawn, not
patched with an after-the-fact fixture.

**Argument.** The 2026-08-20 dashboard fixtures were not committed.
The measurements behind them were never reproducible.
The honest fix was to withdraw the certification rather than fabricate
fixtures after the fact.

The `zip` against `xl/` sniff distinction is documented as a rule rather than
implemented.
The sniff reads four bytes and cannot see inside the container.
SheetJS yielding no sheets is the real signal, and that is what the rule says.

**Evidence.** Pass dated 2026-08-24, immediately after the audit.
G12, the uncommitted 2026-08-20 fixtures, carries the withdrawn certification.

**Checks.** none.
