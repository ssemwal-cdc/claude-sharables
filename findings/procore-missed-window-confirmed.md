---
id: F147
slug: procore-missed-window-confirmed
kind: finding
status: observed
date: 2026-09-16
---
# Procore missed window confirmed

**Outcome protected.** A scheduled Procore window reviews the queue once, not repeatedly.

**Argument.** The Procore scheduled prompt was derived from the NetSuite one.
It was checked against the skill for the state filename, the report format and the GET-only rule.

**Evidence.** Reported by the maintainer, date unrecorded.
A missed window did not queue up or run later.
The run is unmeasured.
F77, a NetSuite schedule fired and onboarded itself, is the nearest other observation.

**Checks.** none.
