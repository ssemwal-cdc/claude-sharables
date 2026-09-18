---
id: G2
slug: freeze-fallback-unfired
kind: gap
status: unobserved
date: 2026-08-15
---
# Freeze fallback never fired

**Outcome protected.** A frozen tab never causes a second click on an approved record.

**Argument.** The recovery path has never fired.
That path abandons the tab and re-reads from a fresh page load.
It falls back to plain Approve only if the record is still pending.
The path cannot easily be forced.
You probably cannot fire it on purpose.
Know that it is untested.
If a freeze happens, watch what the run does rather than assuming it handled it.
The fallback's terminal action has since shown a silent no-op of its own.
Plain Approve's handler loads a script asynchronously, then calls `win.open`.
By then the click's user activation has expired.
So the ladder now ends in navigating the button's own URL in Step 8.6, not in a click.

To clear it: watch a real freeze, which nobody can schedule.

**Evidence.** This claim is guessed, not proven.
It is tested against mocks or fixtures and shipped.
Nobody has watched the fallback fire.
Do not cite it as established.
`python3 scripts/test_skill_code.py` covers the logic against mocks.
It cannot cover this gap, because this gap is about a real system.
Update 2026-08-15: the URL leg is live-confirmed on record 2534442.
The freeze fallback as a whole has still never fired.
One freeze was observed once, immediately after an Approve With Notes click.
The renderer locked, the tab left the automation group, and the note was never typed.
F144, the notes page now seen once, is where that freeze happened.
One clean read does not confirm the page behaves the same after a freeze.

**Checks.** none.
