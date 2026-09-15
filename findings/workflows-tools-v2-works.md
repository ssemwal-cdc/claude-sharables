---
id: pending
slug: workflows-tools-v2-works
kind: finding
status: observed
date: 2026-08-15
---
# The tools endpoint needs v2

**Outcome protected.** A new item type is looked up instead of guessed.

**Argument.**

The 400 body names a company-level workflow tools endpoint. That pointer is real and version-shifted.

Version 1.0 of that endpoint returns a 403 for an ordinary account, which is what made it read as a permissions wall.

Version 2.0 of the same endpoint works and lists the valid workflowable type strings.

That is the tool to reach for if another item type ever appears, instead of guessing candidates.

**Evidence.**

- Observed 2026-08-15. The working path is `/rest/v2.0/companies/<company>/workflows/tools`.

**Checks.** none
