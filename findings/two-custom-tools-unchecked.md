---
id: pending
slug: two-custom-tools-unchecked
kind: finding
status: observed
date: 2026-09-01
---
# Second custom tool unchecked

**Outcome protected.** Every custom tool in the queue is read against its own fields.

**Argument.**

One run held 62 items across two custom tools. The second tool was unknown to the config and was reviewed against the fields of the first.

Three defects sat behind it. The tool id in the config was singular, and every record link was built from it.

A wrong tool id does not return a 404. It resolves to a real page in the wrong tool, indistinguishable from the right one.

The cost field mapping was one flat mapping for all custom tools. The two field sets are different, not renamed, so three checks read fields that do not exist there.

The by-label rule earned its keep from the other direction. One field id on the second tool is a duration in weeks. Carried across as a cost, a 52 becomes 52 dollars and the check ties on fiction.

The config field that names which tool it describes was written by setup and read by nothing. It is exactly what would have caught this.

A declared field that no step reads is worse than no field. It reads as coverage.

The config is now keyed by the queue item subtype, carrying that tool id and its own cost fields. Step 1 reconciles the queue subtypes against the config keys on every run.

The run where a new tool first appears is the run that has to notice.

Ask what field already carries the distinction when a queue turns out wider than the config. It is usually already in the payload.

**Evidence.**

- Reported 2026-09-01. The second tool was 37 of the 62 items.
- The old singular tool id survives as the link floor for rows logged before subtypes existed. The back-fill restructures an old config in place.
- This is the seventh instance of the shape these records keep recording, and the second where a wrong but valid identifier is the whole danger.

**Checks.** `test_custom_tool_subtype` in `scripts/test_skill_code.py`.
