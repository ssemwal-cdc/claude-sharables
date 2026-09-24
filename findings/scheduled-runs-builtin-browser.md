---
id: F165
slug: scheduled-runs-builtin-browser
kind: finding
status: observed
date: 2026-09-24
---
# Scheduled runs drive the built-in browser

**Outcome protected.** A scheduled run reaches the teammate's own signed-in session, not a
separate, unsigned-in browser.

**Argument.** A scheduled run now opens the built-in Claude browser, not Claude in Chrome.
Setting the default browser to Claude in Chrome does not fix this on scheduled runs.
That setting only takes on a run started directly, not one a schedule fires.
F77, folderless scheduled run works, reported a scheduled run completing cleanly before this.
So this is a regression, not how scheduling always behaved.
Which release, setting, or environment change caused the switch is `unmeasured`.

**Evidence.** Reported 2026-09-24 by the maintainer: scheduling worked, then stopped.
Every fire since kept opening the built-in browser instead of Claude in Chrome.
Changing the default-browser setting to Claude in Chrome did not change that on a scheduled fire.
The maintainer stopped scheduling on 2026-09-24 because of this.
The cause is `unmeasured`.
On 2026-09-24 both skills gained a first-call Claude in Chrome check, `skill-chrome-first-call`.
The block copies the shape of a working scheduled skill's own first-call check.
Whether this fixes scheduled runs is `unmeasured`, until one scheduled run is watched.

**Checks.** none.
