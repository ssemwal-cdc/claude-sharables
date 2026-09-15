---
id: pending
slug: widget-is-only-deliverable
kind: decision
status: settled
date: 2026-08-21
---
# The widget is the deliverable

**Rule.** Never attach the working files. The rendered widget is the whole deliverable.

**Outcome protected.** A reviewer reads one dashboard instead of sorting through download cards.

**Argument.**

Runs began presenting the working files as chat file cards. The template, the publish script, the review log and the rendered page all appeared as download cards.

Nothing in either skill asks for that. Newer harness builds push agents to surface files a run wrote, and the state files pattern-match a deliverable.

Both skills now carry an absolute rule that the widget is the only deliverable.

If cards still appear with that rule shipped, the surface is auto-listing written files. No skill wording can suppress that.

**Evidence.**

- Observed 2026-08-21.
- One run later handed a 164 KB page over as the deliverable. See F‹render-read-wall-serialise›, the read side had a real wall.

**Checks.** none
