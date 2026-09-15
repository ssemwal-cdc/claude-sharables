---
id: pending
slug: render-unverifiable-ask-user
kind: finding
status: observed
date: 2026-08-24
---
# The render is unverifiable agent-side

**Outcome protected.** A truncated dashboard is reported instead of hidden.

**Argument.**

The render tool returns the same success string whatever it rendered. The path test proved it says that while showing a line of text.

The integrity guard raises its banner to the user, not to the caller.

So an agent asked to render a large file is asked to take an unobservable risk with an approval queue. Refusing looks like the careful choice.

Four rounds of rewording did not shift that. The warning about not trusting the success message probably reinforced it.

The fix is not more reassurance. It is to close the loop by asking the user to report the banner, one sentence after the render.

Both skills now do that.

**Evidence.**

- Recorded 2026-08-24 after four refusals. The refusal count is the measurement. The effect of the ask is `unmeasured`.

**Checks.** none
