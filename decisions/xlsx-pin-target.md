---
id: D86
slug: xlsx-pin-target
kind: decision
status: settled
date: 2026-09-15
---
# SheetJS pin target

**Rule.** Target SheetJS 0.20.2, and keep the 0.18.5 pin until the new host executes.

**Outcome protected.** A workbook parsed inside an authenticated tab cannot be used against the session.

**Argument.**

SheetJS 0.19.3 fixes the prototype pollution, CVE-2023-30533.

SheetJS 0.20.2 fixes the ReDoS, CVE-2024-22363.

So 0.20.2 is the first version that fixes both. The mandate says to bump to the first fixing version and never to the latest.

Both plugins pin xlsx 0.18.5 today. That version predates both fixes.

The pin was accepted on one argument. That argument is that parsing happens in the S3 scratch tab, which holds no Procore session.

That argument holds for Procore only. NetSuite loads its libraries in the record tab, because the `media.nl` fetch needs the session cookie. So a workbook parsed on the NetSuite side is parsed inside an authenticated tab.

The blocker is the host. npm stopped at 0.18.5, and cdnjs mirrors npm, so cdnjs cannot serve 0.20.2.

SheetJS serves 0.20.2 from `cdn.sheetjs.com`. Executing a script from that host in these two tabs is unprobed.

So nothing is bumped today. Bump only after a `script-src` probe passes for the new host. An unexecutable library is worse than an old one.

**Evidence.**

- `GHSA-4r6h-8v6p-xvw6` states affected `< 0.19.3` for the npm package `xlsx`. Read 2026-09-15.
- `GHSA-5pgg-2g8v-p4x9` states affected `< 0.20.2` for the npm package `xlsx`. Read 2026-09-15.
- `registry.npmjs.org/xlsx` reports 108 versions and `dist-tags.latest` 0.18.5. Read 2026-09-15.
- cdnjs's own highest version is `unmeasured`. The egress proxy blocks `api.cdnjs.com`, `cdnjs.com` and `cdnjs.cloudflare.com`.
- The `script-src` probe for `cdn.sheetjs.com` is unprobed. The egress proxy also blocks that host, and reachability is not executability.
- `nvd.nist.gov` and `cdn.sheetjs.com/advisories/` were blocked, so the version figures come from the GitHub Advisory Database.

**Checks.** `check_pins()` in `scripts/shared_blocks.py` asserts the version agrees across plugins. The target version has no check, because no code reads it yet.
