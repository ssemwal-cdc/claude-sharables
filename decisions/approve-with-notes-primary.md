---
id: D28
slug: approve-with-notes-primary
kind: decision
status: settled
date: 2026-08-15
---
# Approve With Notes stays primary

**Rule.** Route every NetSuite approval through Approve With Notes. Reach plain Approve only as the stated fallback.

**Outcome protected.** Every approval carries its attribution note.

**Argument.**

Approve With Notes is the only path that can attach the note. D20, default the approval comment, requires one.

This is a deliberate exception to clicking only the button named in the instruction.

Reject is never substituted for either button, in any direction.

Do not promote the direct approval URL to the primary route. See F33, plain Approve can no-op.

**Evidence.**

- Recorded 2026-08-15 with the plain-Approve recovery.
- The freeze fallback is F27, the notes click is a navigation.

**Checks.** none
