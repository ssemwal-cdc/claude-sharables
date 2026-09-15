---
id: F12
slug: show-widget-inline-only
kind: finding
status: observed
date: 2026-08-12
---
# show_widget takes content inline

**Outcome protected.** A reviewer sees a dashboard instead of a line of text.

**Argument.**

The tool schema has three properties. The loading messages array is the only required one. The other two are the title and the widget code.

There is no path property, no file property and no src property.

Passing a file path where the content goes does not error. It returns the standard success string and renders the path string itself.

So the obvious optimisation looks like it worked and quietly shows the user one line of text.

Do not trust the success message on this tool as evidence that the right thing rendered.

**Evidence.**

- Schema read live 2026-08-12. The path test was run the same day.
- Nothing in the description mentions a byte, character, line or token limit, so any ceiling is `unmeasured`.

**Checks.** none
