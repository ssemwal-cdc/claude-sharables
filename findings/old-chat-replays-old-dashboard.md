---
id: F30
slug: old-chat-replays-old-dashboard
kind: finding
status: observed
date: 2026-08-15
---
# Old chats replay old dashboards

**Outcome protected.** A maintainer does not blame an install for a button rendered weeks ago.

**Argument.**

A rendered dashboard is a snapshot of the template. An old conversation keeps offering its old instruction forever.

A resolve-the-gate button was quoted with wording that had been removed. So the install was called out as predating that commit. It was not. The install already contained the fix.

The button sat in a dashboard rendered before the update.

A re-render fixes it. Running the review again is enough, and updating the plugin changes nothing about the old widget.

Clicking a button in an old chat is not evidence about the installed plugin at all.

**Evidence.**

- Cost a wrong diagnosis 2026-08-15. The removed wording came out in commit `7100c5d`, which dropped the alternative-type-strings advice from the gate button.
- The install was commit `5767839`, the release that already contained `7100c5d`.

**Checks.** none
