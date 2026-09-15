---
id: G10
slug: procore-scheduled-prompt-unfired
kind: gap
status: unobserved
date: 2026-08-24
---
# Procore scheduled prompt unfired

**Outcome protected.** A scheduled Procore window reviews the queue once, not repeatedly.

**Argument.** The Procore scheduled prompt was derived from the NetSuite one.
It was checked against the skill for the state filename, the report format and the GET-only rule.
It has never actually fired.

To clear it: trigger the scheduled task manually once.
Then fire it a second time.
Confirm the idempotency gate reports "already completed today" on the second fire.

**Evidence.** This claim is guessed, not proven.
It is checked against the skill text and shipped.
Nobody has watched the Procore schedule fire.
Do not cite it as established.
`python3 scripts/test_skill_code.py` covers the logic against mocks.
It cannot cover this gap, because this gap is about a real system.
F77, a NetSuite schedule fired and onboarded itself, is the nearest observation.

**Checks.** none.
