---
id: F26
slug: xml-scratch-tab-no-createelement
kind: finding
status: observed
date: 2026-08-14
---
# The scratch tab is XML

**Outcome protected.** A rasterised PDF page renders instead of throwing.

**Argument.**

The bucket-root scratch tab is an XML document, so the ordinary element factory does not work there.

The content type is `application/xml`, so creating a canvas yields a null-namespace element with no drawing context.

The XML content type is exactly why that tab was chosen. It is attachable where a PDF is not, so this is permanent.

Use an offscreen canvas, or create the element in the XHTML namespace.

Never move the tab to an HTML page. It must stay same-origin with the presigned link or the fetch hits the cross-origin wall.

NetSuite is unaffected, because it runs pdf.js in the record tab, which is ordinary HTML. Do not normalise the two.

Worth noting how this surfaced. It was an incidental error in a probe written to ask about something else. It was disclosed rather than smoothed over.

A run could have caught the exception quietly and reported four clean results. That would have left a broken render call in the skill. It would be found later by a scanned invoice in production.

**Evidence.**

- Observed 2026-08-14 when the canvas check in the probe threw.

**Checks.** none
