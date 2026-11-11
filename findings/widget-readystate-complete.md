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

A second probe on 2026-11-11 tested the hash check. A script and a stylesheet with the correct sha384 `integrity` value loaded. The same files with a wrong value were blocked.

A third probe on 2026-11-11 read the `--dash-css` marker that the dashboard code checks. The widget read it from a `<style>` block and from the pinned stylesheet. In that probe the send button did nothing when clicked; in the hash probe earlier that day it sent its text. The cause is unknown.

**Evidence.**

- Owner-run probe widget, Claude desktop app, 2026-10-21.
- Owner-run hash probe, 2026-11-11: correct hash loaded, wrong hash blocked, for a script and a stylesheet.
- Owner-run marker probe, 2026-11-11 13:17 CST: `--dash-css` read from a style block and from the pinned stylesheet.
- Fix landed in commit `c888908`: the guard now checks `readyState`.

**Checks.** none
