---
id: D75
slug: execute-type-coverage-gate
kind: decision
status: settled
date: 2026-09-01
---
# Gate the two type lists

**Rule.** Keep the review type vocabulary, the execute route table and the type manifest naming the same types.

**Outcome protected.** A reviewed but unactionable type fails the build instead of stopping a batch.

**Argument.**

`check_execute_type_coverage()` asserts that three things name the same three types. Those are the review step type vocabulary, the execute step route table and the hardcoded manifest.

Both lists are prose, and prose gains a type on one side without the other.

Same shape and same friction as the check registry manifest, for the same reason.

**Evidence.**

- Added 2026-09-01 after F94, NetSuite could not click purchase orders.
- Mutation-tested five ways. Dropping the row, shrinking the schema, inventing a fourth type, renaming the heading and blanking a gate cell all fail.

**Checks.** `check_execute_type_coverage()` in `scripts/shared_blocks.py`.
