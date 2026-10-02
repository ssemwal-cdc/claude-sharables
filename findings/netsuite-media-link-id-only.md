---
id: F169
slug: netsuite-media-link-id-only
kind: finding
status: observed
date: 2026-10-02
---
# A real bill's media.nl link carries no c or h

**Outcome protected.** Browser mode stops claiming a route it cannot run, instead of fetching a path that 500s.

**Argument.**

Browser mode once read the attachment link off the record page as a plain `<a href="...media.nl...">`. It expected `id`, `c` and `h` as query parameters.

A real vendor bill record, measured live 2026-10-02, shows a different anchor. It is `href="javascript:NS.UI.Util.downloadFile(...)"`, holding a JS-escaped (`\/`) `media.nl` path.

That path carries an `id` parameter. It carries no `c` and no `h`.

An in-page same-origin fetch of that path returned HTTP 500, an HTML error page, not the file.

The NetSuite connector was not connected during this pass, so connector mode was not re-tested.

**Evidence.**

- Measured live 2026-10-02, Claude in Chrome, Claude Code auto mode, a real vendor bill.
- Supersedes the DOM-split recipe this skill's browser mode once carried.

**Checks.** none
