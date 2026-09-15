---
id: pending
slug: dashboard-widget-host-unseen
kind: gap
status: unobserved
date: 2026-08-27
---
# Dashboard unseen in widget host

**Outcome protected.** The reader can reach an execute control wherever they are in the queue.

**Argument.** Most of the 2026-08-20 dashboard change was observed, but not where it runs.
That change was the newest-first default, the sticky execute bar, numbered steps and the header mirror.
Both dashboards were published from fixtures and driven in headless Chromium.
Treat the 2026-08-20 numbers as reported rather than reproducible.
Re-measure if any of them matters again.
Every number a command regenerates has verified correct on demand.
Almost every number a human typed into prose has since moved.

**`position:sticky` does nothing on this host.** The 2026-08-20 measurement was taken at `file://`.
The document itself scrolls there.
The widget frame auto-sizes while the conversation scrolls.
The pinned bar has never been seen working.
So sticky degrades silently to an ordinary block, with no error and no console output.
That is why the header mirror exists and must not be deleted as redundant.
The header mirror is the half that works on either host.
`docs/onboarding.html` is worded to be true either way.
It says a button sits at the bottom and a second appears in the header.
It deliberately does not promise the bottom button follows you down the page.
An earlier draft promised that and was removed unshipped.

**A floating header replaced the sticky one, and its standing differs from the rest.**
The mechanism reads the visible band with `IntersectionObserver` across the frame boundary.
`scripts/measure_float.js` publishes both dashboards from fixtures and measures the bar.
It serves the widget cross-origin into a scrolling host.
Every positional claim comes from a command a future session can re-run.
Three host arrangements were measured, and all three place the bar correctly.
Two of the three are guesses about the real arrangement.
So the feature does not rest on the 2026-08-26 report being right about the host.

**Not observed in the real widget host, by anyone.** The frame arrangement is a reproduction.
It was built from a report, not from `*.claudemcpcontent.com`.
`show_widget` returns "Content rendered" whatever it rendered.
So an agent cannot see where the bar landed.

To clear it: on the next real run, scroll into the middle of the queue.
Say whether a thin bar carrying the item count, `Filters` and `Execute` sits at the top of the screen.
If it does not, the reproduction and the host disagree, and that is the fact to record.
The row buttons work either way, because nothing was taken away to add this.

**Also unseen at real scale.** The fixtures were 6 NetSuite bills and 8 Procore items.
A real Procore queue has run to 43 or 73 items.
A sticky bar overlays the rows beneath it.
153px of overlay against a six-row fixture is not the same as against seventy rows.
Nobody has watched that.
The step headings and the restyled marked rows are cosmetic and likewise unseen.

**Evidence.** The 2026-08-20 fixtures were never committed, so nobody can re-run or audit them.
The widget-host position is guessed, not proven.
Nobody has watched the bar in the real host.
Do not cite it as established.
`scripts/measure_float.js` is reproducible and needs a browser, so it is not in CI.
Measured: 0.0px band error at every offset, and a distinct position for 26 steps of an 8px scroll.
One full-height sentinel gave 4 callbacks for a whole page and a stale band at 3 of 6 offsets.
The bar measures 153px on both dashboards.
The full header is about 380px against a 700px viewport.
Reported 2026-08-26: the maintainer has never seen the sticky bar work.

**Checks.** `test_dashboard_view` pins the mechanism. `scripts/measure_float.js` measures position by hand.
