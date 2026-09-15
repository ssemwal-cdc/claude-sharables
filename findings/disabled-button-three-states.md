---
id: pending
slug: disabled-button-three-states
kind: finding
status: observed
date: 2026-08-24
---
# One disabled style, two meanings

**Outcome protected.** A blocked execute button reads as blocked, not as broken.

**Argument.**

One disabled rule served two meanings. Nothing marked and one sentence away from ready were pixel-identical, so the second read as a broken button.

There are three states now. Grey for idle. An amber outline with a full-contrast label for blocked. The solid dark primary when it can run.

The clear-all-marks control went from a full-contrast bordered button to a text link.

At the blocked moment the loudest control on offer was the one that discards every decision.

**Evidence.**

- Landed 2026-08-24.
- The header mirror change is in D‹execute-bar-always-rendered›, render the execute bar always.

**Checks.** `test_dashboard_view` in `scripts/test_skill_code.py`.
