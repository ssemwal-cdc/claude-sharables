---
id: pending
slug: widget-readystate-complete
kind: finding
status: observed
date: 2026-10-21
---
# The widget runs scripts after DOMContentLoaded

**Outcome protected.** A reviewer sees a red warning when a dashboard page was cut off in transit.

**Argument.**

The owner ran a probe widget in the Claude desktop app on 2026-10-21.

When `show_widget` scripts run, `document.readyState` is already `complete`. A listener on `DOMContentLoaded` alone never fires. A guard that reads `readyState` first does fire.

So the integrity guard in both dashboards never fired in the widget before commit `c888908`, Procore v48 and NetSuite v46. A cut-off page showed no warning.

The same probe loaded a `<script src>` from `cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables@<full sha>`. An npm control loaded too. See D‹pinned-repo-cdn-assets›, pinned repo assets.

**Evidence.**

- Owner-run probe widget, Claude desktop app, 2026-10-21.
- Fix landed in commit `c888908`: the guard now checks `readyState`.

**Checks.** none
