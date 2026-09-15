---
id: pending
slug: no-run-without-browser
kind: finding
status: observed
date: 2026-08-24
---
# Nothing runs without Chrome

**Outcome protected.** A missed window is covered by a later one instead of being lost.

**Argument.**

Both plugins drive the real browser session.

So nothing runs with the machine off or with Chrome closed.

A missed scheduled window does not queue up.

Hence more than one fire time, with the idempotency gate stopping the later ones once a day has succeeded.

**Evidence.**

- Stated in `docs/onboarding.html`. The rate of missed windows is `unmeasured`.

**Checks.** none
