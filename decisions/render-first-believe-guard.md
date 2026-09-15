---
id: pending
slug: render-first-believe-guard
kind: decision
status: settled
date: 2026-09-01
---
# Render first, believe the guard

**Rule.** Render the dashboard. Fall back only after an observed failure, never on a size estimate.

**Outcome protected.** A reviewer keeps one-click execute on a large queue.

**Argument.**

There is no known ceiling on the render tool. Every threshold anyone proposed for it was invented, including by the repo notes.

The template carries a guard that turns a truncated render into a red banner. That exists so the question is settled by observation.

An estimate is not an observed failure.

Four runs declined a render. The first three argued the output side and were wrong. See F‹render-read-wall-serialise›, the read side had a real wall.

One of those handed over a 120 KB dashboard as a file. That cost one-click execute entirely to avoid a risk that had not happened.

A fallback is licensed by a read that actually came back short. A byte count is not a licence.

The slim build is not a size fallback. See F‹slim-build-not-a-fallback›, the slim build saves little.

**Evidence.**

- A 99 KB Procore dashboard with 43 items rendered in a single call, 2026-08-12.
- Two runs before that refused on size grounds without attempting. One read 929 of 1849 lines and extrapolated the rest.
- The read-side ceiling is real and separate. It was measured 2026-09-01 at 174 KB over 2,834 lines.
- The tool takes content inline only. See F‹show-widget-inline-only›, show_widget takes content inline.
- The caller cannot see what rendered. See F‹render-unverifiable-ask-user›, the render is unverifiable agent-side.
- NetSuite cannot fold rows at all. See F‹slim-build-not-a-fallback›, NetSuite cannot fold rows.
- An asset shipped a threshold that fed a refusal. See F‹invented-threshold-in-comment›, an asset invented a threshold.
- The same run produced four findings this repo could not have produced. See F‹a-wrong-run-found-four-defects›, a wrong run found four defects.

**Checks.** `test_render_fits_one_read` in `scripts/test_skill_code.py`, mutation-tested.
