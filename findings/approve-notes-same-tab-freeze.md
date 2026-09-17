---
id: F27
slug: approve-notes-same-tab-freeze
kind: finding
status: observed
date: 2026-08-15
---
# The notes click navigates

**Outcome protected.** A frozen tab never produces a second click on a bill already approved.

**Argument.**

Approve With Notes is a same-tab page navigation, not a popup.

A tab froze once immediately after that click. The renderer locked, the tab dropped out of the automation group, and the note was never typed.

The run verified two ways and refused to re-click. That was correct.

The freeze was diagnosed as a blocking native dialog, and a browser prompt override was designed on that reasoning. That reasoning was almost certainly wrong and the override was never built.

Note the standing of the claim. Nobody has seen the notes page and nobody has read the handler of that button, so the absence of a popup is inference from the UI.

So a freeze is an unknown outcome, never a failed one.

Recovery is a fallback to plain Approve, gated on a fresh page load and never on a connector query. Still pending means click Approve and log the note as lost. Already advanced means click nothing and log it as approved with no note.

Gating on a connector read would eventually click twice on a bill already approved, because of the connector lag.

**Evidence.**

- Observed once in 2026-08. The frequency is `unmeasured`.
- The lag is F10, verify the record not the queue.
- The once-unseen page is F‹netsuite-approval-note-confirmed›, the note read on the record.

**Checks.** none
