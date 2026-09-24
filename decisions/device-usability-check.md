---
id: D81
slug: device-usability-check
kind: decision
status: settled
date: 2026-09-15
---
# Device usability check

**Rule.** Check every screen at three widths and in both themes.

**Outcome protected.** The page works on the device the reader actually holds.

**Argument.**

This is a usability check across devices. It is not a documentation exception.

Three screens exist. They are the two dashboards and the onboarding sheet.

`scripts/measure_float.js --shots [dir]` is the mechanism. It captures all three screens at 390px, 1200px and 1600px, in light and in dark.

That is 18 files. The harness already publishes both dashboards from fixtures, so the capture pass costs one extra page per file.

The onboarding sheet is one self-contained file, so the fixture server copies it and serves it beside the dashboards.

Every capture also reports `scrollWidth` against the viewport width, into `summary.txt`. A horizontal overflow at 390px is then a number and not a judgement.

The images are not committed. `.gitignore` excludes `.claude/shots/`, because a binary baseline rots and nothing reads it.

The command runs by hand and not in CI, because `validate.py` may not assume a browser. It reuses the float measurement's browser, so one run does both.

A metric is not appearance. A person still has to look at typography, spacing and hierarchy in the images.

**Evidence.**

- Widths covered by a repeatable command: three. Schemes: two. Screens: three.
- The first run is `Fdevice-shots-first-run`, 18 captures and no overflow.
- The onboarding sheet was measured once before, on 2026-08-28. F89, measured at three widths in both schemes, is that one-off.
- F‹dashboard-widget-host-confirmed›, fixtures never committed, is why a one-off measurement
  was not enough.

**Checks.** `NODE_PATH=$(npm root -g) node scripts/measure_float.js --shots .claude/shots`, by hand or in the `shots` CI job. The default run without `--shots` prints the float measurements only. `check_device_shots()` in `scripts/check_records.py` reads `.claude/shots/summary.txt`. It fails the build on any capture with an overflow, or on fewer than 18 captures. It is silent, not failing, when the file is absent. `device_shots_note()` prints that absence as a note.
