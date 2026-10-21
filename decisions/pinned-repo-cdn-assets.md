---
id: pending
slug: pinned-repo-cdn-assets
kind: decision
status: settled
date: 2026-10-21
---
# Dashboards may load fixed assets from a pinned repo copy

**Rule.** A dashboard may load its fixed CSS and JS from this repo through jsdelivr `/gh/`. The URL names a full commit sha. The tag carries an SRI `sha384` hash. Both are required. Not yet built.

The repo stays public on the `ssemwal-cdc` account under its current name. Merges keep the pinned commit: merge method `merge`, never squash or rebase.

**Outcome protected.** A dashboard stays small enough to render in one read. The code it runs is the code reviewed in this repo.

**Argument.**

D95, a skill never shapes its way past a filter, bars a run from hiding what it does. A pinned load is not that. This repo holds the reviewed code. The pin names one commit. The hash fails the load if one byte differs. Without the pin and the hash it would be unreviewed code. So both are the whole condition.

The pin only resolves while the repo is public and keeps its name and account. See D13, keep this repo public. A squash or rebase merge rewrites the commit, and the pinned sha would stop resolving.

Owner rulings, 2026-10-21. Status: settled, not built. The probe in F‹widget-readystate-complete›, the widget runs scripts late, showed a pinned `<script src>` loads in the widget.

**Evidence.**

- Probe, 2026-10-21: a `<script src>` from `cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables@<full sha>` loaded in the widget.

**Checks.** none
