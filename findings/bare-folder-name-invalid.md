---
id: pending
slug: bare-folder-name-invalid
kind: finding
status: observed
date: 2026-08-11
---
# A bare folder name fails

**Outcome protected.** A marketplace entry that passes JSON review also installs.

**Argument.**

A bare folder name as the source passes a JSON syntax check.

It then fails at install with `This plugin's marketplace entry is invalid: source: Invalid input`.

So a valid JSON file is not evidence that an entry resolves.

**Evidence.**

- Reproduced against Claude Code v2.1.227 with `"source": "netsuite-approval-review"`.

**Checks.** `scripts/validate.py` requires a `git-subdir` source object.
