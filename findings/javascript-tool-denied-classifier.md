---
id: pending
slug: javascript-tool-denied-classifier
kind: finding
status: observed
date: 2026-08-14
---
# The classifier can deny everything

**Outcome protected.** A denial stops the run instead of being routed around.

**Argument.**

The browser JavaScript tool can be denied by the permission classifier. That is the one failure that stops both skills dead.

Everything load-bearing goes through that tool. That is the Procore gate fan-out, every attachment read and the NetSuite bulk query.

So a denial is not a degraded run. It is no run.

The agent was right to stop rather than route around it, and right to reject the sandbox as a substitute. The sandbox is a different network and a different cross-origin environment, so a result from there would not answer the question asked.

Refusing to launder a denial through a different execution context is the correct instinct. Keep it.

It is worse on a schedule than in a chat. It fires on the first such call of every run, and a stalled prompt nobody watches reads as a hang.

Do not mine the denial text. The reason string has been a fixed classifier message since v2.1.208, and the classifier scores severity internally rather than explaining.

Do not generalise from a diagnostic to the workflow. The probe that was denied fetched 5 URLs across 4 CDNs, and both skills only ever fetch one CDN.

**Evidence.**

- Hit 2026-08-14 while running the CDN probe. The call was blocked before it reached the page, with the tab already open and correct.
- The cause was environmental. See D‹auto-mode-not-skip-all›, auto mode and never skip-all.

**Checks.** none
