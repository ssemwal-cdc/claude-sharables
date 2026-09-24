---
id: F160
slug: netsuite-browser-mode
kind: finding
status: observed
date: 2026-09-24
---
# NetSuite browser mode confirmed

**Outcome protected.** A teammate with no connector still gets a complete review.

**Argument.** The skill runs without the MCP connector.
Browser mode takes the queue from the dashboard portlets.
It reads record fields with `get_page_text`.
It reads the attachment URL off the record page.
It does not perform Step 5's PO and billing-history cross-check.
The publish abort found in browser mode on 2026-08-24 was fixed the same day.
`account` is required on both routes. `me` and `tool` are required in connector mode only.

**The method mattered more than the bug.** This was the second defect found by reading the two
plugins against each other rather than by running either.
It survived since browser mode shipped, because nothing exercised the path before.

**Step 5 stays silent by design in browser mode.** No caveat prints for someone who cannot be
provisioned. See D69, silence for a capability nobody can obtain.

**Evidence.** Reported 2026-09-24 by the maintainer: browser mode is done.
Which record types were run through it, and whether the attachment selector held on every
type, is not itemized. That detail is `unmeasured`.
Browser mode was added 2026-08-15. The publish abort was reproduced from a fixture on
2026-08-24, then fixed.
`python3 scripts/test_skill_code.py` covers the publish guard against mocks only.

**Checks.** `scripts/test_skill_code.py` for the publish guard.
