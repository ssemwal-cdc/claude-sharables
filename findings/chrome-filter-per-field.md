---
id: F168
slug: chrome-filter-per-field
kind: finding
status: observed
date: 2026-10-02
---
# The output filter blanks one field, not the call

**Outcome protected.** A skill reads what the filter left intact, instead of treating the whole result as lost.

**Argument.**

The output filter was once described as blanking a whole tool result when any field held a URL query string.

Measured live 2026-10-02, that is not what it does.

It blanks only the one result field whose value holds a URL query string, as `[BLOCKED: Cookie/query string data]`. Sibling fields on the same result survive untouched.

The JavaScript source sent to the tool is never echoed back, on a success and on a thrown error alike.

A second trigger fires per field too. A dotted string, such as a version number or a hostname like `app.procore.com`, comes back `[BLOCKED: JWT token]`.

`tabs_context_mcp` and `navigate` results carry their own redaction. `X-Amz-Algorithm`, `X-Amz-Credential`, `X-Amz-Date`, `X-Amz-SignedHeaders` and `X-Amz-Signature` values come back `REDACTED`. `X-Amz-Expires=60` survives.

Inside the page, `location.href` is intact. The redaction is a property of the tool result, not of the page.

**Evidence.**

- Measured live 2026-10-02, Claude in Chrome, Claude Code auto mode.
- Supersedes the whole-result-blanked description this skill once carried.

**Checks.** none
