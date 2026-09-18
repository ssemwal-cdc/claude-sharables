---
id: F117
slug: second-source-found-what-self-check-couldnt
kind: finding
status: observed
date: 2026-08-24
---
# A second source found what self-checks could not

**Outcome protected.** A plugin's own drift is found by comparison, not by asking it about
itself.

**Argument.** Two independent sources said different things about the same
behaviour.
Neither copy could detect its own miss.
The difference here is that the second source was the other plugin, in the
same repo the whole time.
That is what made the six-defect drift findable at all.

**Evidence.** Audit dated 2026-08-24.
See `F120`, the six defects this found.

**Checks.** none.
