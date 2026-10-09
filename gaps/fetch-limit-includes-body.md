---
id: pending
slug: fetch-limit-includes-body
kind: gap
status: unobserved
date: 2026-10-09
---
# The 20 second fetch limit includes the body download

**Outcome protected.** A large but healthy read is not reported as timed out.

**Argument.** `AbortSignal.timeout(20000)` runs from the start of the fetch. It counts the body download too, not only the first byte. A slow body can abort a read that was healthy. The whole-call deadline of 60 seconds is a second cause. A large healthy read that runs past it is reported as timed out too. The skill then names it "support read timed out" and skips the item.

**Evidence.** `unmeasured`. Nobody timed the largest invoice JSON or the largest attachment against 20 seconds. Nobody timed a whole read against 60. Do not cite 20 seconds as safe. The 2026-10-09 run is the only incident behind it. See D`in-page-call-deadline`, every in-page call stops itself.

**Checks.** None. Time the largest invoice `view=extended` read and the largest attachment on a live run, then record both.
