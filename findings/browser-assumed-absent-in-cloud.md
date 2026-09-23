---
id: pending
slug: browser-assumed-absent-in-cloud
kind: finding
status: observed
date: 2026-09-23
---
# A session assumed no browser

**Outcome protected.** A capability is measured before a run claims it cannot run.

**Argument.**

`D70`, measure position in a browser, wants the float measurement by hand after a layout change.

A session briefed a worker to skip that measurement. It stated that the container had no browser.

The container had one. Chromium ships in the base image at `/opt/pw-browsers`. Playwright resolves from the global module root.

Two lines invited the reading. This file said "by hand. Needs a browser." The header of `scripts/measure_float.js` said that `validate.py` may assume neither Chromium nor Playwright.

Both sentences are true of the build gate. Neither says anything about the session running them.

The prose was a contributing cause. The claim itself was the failure. Nothing was probed.

A capability is a read. `D41`, three states never a boolean, already covers it. A read that never ran is unknown, never absent.

**Evidence.**

- Observed 2026-09-23, in a cloud session on this repo.
- The worker brief said to skip `measure_float.js` and to report it as not run.
- Probed in the same session afterwards. `/opt/pw-browsers/chromium` present, node v22.22.2, `playwright` in the global module root.
- The brief was corrected in the same session, and the measurement ran.
- The session-start capability probe lives in the global settings, out of this repo's reach.

**Checks.** none in this repo. The two prose lines above are the fallback.
