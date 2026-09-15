---
id: pending
slug: xlsx-pin-target
kind: decision
status: open
date: 2026-09-15
---
# SheetJS pin target

**Rule.** Name the first SheetJS version that fixes the accepted vulnerabilities.

**Outcome protected.** A workbook parsed inside an authenticated tab cannot be used against the session.

**Argument.** cdnjs pins SheetJS 0.18.5.
That version predates SheetJS's prototype-pollution and ReDoS fixes.
The pin was accepted on one argument.
That argument is that parsing happens in the S3 scratch tab, which holds no Procore session.
The output is data and is never executed.
That argument does not hold on the NetSuite side.
NetSuite loads its libraries in the record tab, because the `media.nl` fetch needs the session cookie.
So a workbook parsed there is parsed inside an authenticated tab.
The mandate says to bump to the first version that fixes the problem, never to the latest.
So the target version has to be named before anything is bumped.
`cdn.sheetjs.com` serves a current build and fetches fine.
Executing from that host is untested, because reachability is not executability.
Only cdnjs has evidence for executing code in these tabs.

**Options.**

A. Keep the pin. Record the NetSuite exposure as accepted.

B. Name the first fixing version. Keep the 0.18.5 pin until a `script-src` probe passes for the new host.

C. Bump to the current SheetJS build on cdnjs now.

**Recommendation.** B.
Name the target, so the bump is a decision and not a search.
Keep the pin until the probe passes, because an unexecutable library is worse than an old one.

**Evidence.** Deferred at the interview on 2026-09-15.
cdnjs pins xlsx 0.18.5 and pdf.js 4.0.379, asserted equal across plugins by `check_pins()`.
The first SheetJS version fixing the accepted vulnerabilities is not yet named. `unmeasured`.
The `script-src` probe for `cdn.sheetjs.com` has never been run.
A fetch of five CDNs returned 200 on all five, which says nothing about `script-src`.

**Checks.** `check_pins()` in `scripts/shared_blocks.py` asserts the version agrees across plugins.
