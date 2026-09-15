---
id: pending
slug: output-filter-second-trigger
kind: finding
status: observed
date: 2026-08-14
---
# The filter has two triggers

**Outcome protected.** A dotted identifier in construction data reaches a verdict as itself.

**Argument.**

A library version string came back as a blocked JWT-token marker.

It was not secret and not a token. The dotted-numeric shape matched a credential classifier.

The earlier note covered the cookie and query-string marker and read as though that were the only filter on the path. It is not.

This matters because both skills return figures, and dotted identifiers are everywhere in construction data. Spec sections, phase codes and drawing revisions all have that shape.

**Evidence.**

- Observed 2026-08-14. The literal string `0.18.5` was replaced by a blocked-JWT marker.
- The rule it produced is D‹blocked-marker-never-a-value›, a blocked marker is never a value.

**Checks.** none
