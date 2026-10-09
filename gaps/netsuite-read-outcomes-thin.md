---
id: pending
slug: netsuite-read-outcomes-thin
kind: gap
status: unobserved
date: 2026-10-09
---
# NetSuite has no named outcome for a thrown parse

**Outcome protected.** A read that threw is named, never filed as unread or absent.

**Argument.** A thrown PDF parse in NetSuite has no named outcome. The attachment rule says it is named by what the bytes were. That fits a mislabelled file. It does not fit a CDN import failure or a body-read error. The outcome `expired` has no code path in NetSuite either. Nothing in `window.__open` returns it.

**Evidence.** Read from the SKILL.md code, not seen in a run. `unmeasured`. The Procore skill names this case `read failed`. See D`retry-only-expired-name-skip`, retry only an expired link.

**Checks.** None. Decide whether NetSuite takes a `read failed` outcome.
