---
id: D109
slug: netsuite-history-open
kind: decision
status: settled
date: 2026-10-12
---
# A third NetSuite verdict, history open

**Rule.** NetSuite publishes three verdicts: `clear`, `history-open`, `flagged`. `history-open` applies when every check on the item itself passes. Those checks are the math, adequate support from a `text` or `spreadsheet` outcome, and the amount tying to NetSuite. It also needs the cross-item reconcile (SKILL.md Step 5, with 5c) to leave a remainder that is not zero. Only a full `text` or `spreadsheet` read may reach it. A duplicate never explains a gap. `poWarning` keeps the residual and tells the user to ask AP and the vendor before approving. A remainder of zero after named approved bills and change orders is `clear`, with the explanation in `poWarning`. A missing intermediate application is `flagged`. Any failing check on the item itself, or a missing or unreadable attachment, is `flagged`. `flagged` outranks `history-open`. A typed-reference mismatch alone never makes `history-open` (D42, a typed reference is data).

**Outcome protected.** A reviewer is not told a right bill is wrong because of a question in the PO's history. A browser-only run stays silent about the history. The next connector run re-opens the question.

**Argument.**

A live run flagged a bill whose own figures tied: the fee table and the NetSuite amount agreed. The PO's approved billing history ran ahead of the vendor's previously-billed figure, and nothing explained the gap. `flagged` told the reviewer the bill was defective. `clear` would have hidden the gap. Neither says what is true.

The new verdict names the evidence (D6, a verdict is a recommendation). It mirrors Procore (D103, contract sum ahead of G702). There, a contract sum ahead of the pay application is `clear` only when named items explain it.

Three homes change together (D63, gate verdicts against publish). They are the `VERDICTS` allow list in `publish_dashboard.py`, the verdict vocabulary in `SKILL.md`, and the template branch. `scripts/shared_blocks.py` holds a hard-coded verdict tuple for the capability table. It gains `history-open` too.

Display. Payload and verdict-sort order is flagged, `history-open`, clear. The default sort stays newest first (D40, sort newest first by default). The row class is `vhist`. The template has an explicit branch for it, never the final `else` that draws Clear. The tiles are Clear, History open, Flagged. NetSuite has no cleared-to-approve dollar total, so none is added.

The headline reads `N pending · F flagged · H history open · dashboard updated`.

Step 5 runs only in connector mode, so only a connector run can produce `history-open`.

**Owner ruling, 2026-10-12.** A browser-only run judges only what it can see. It gives `clear` or `flagged` from its own checks. It says nothing about the billing history (D69, silence on an absent connector). `history-open` is never carried forward. Every run derives the verdict again. Only a connector run can reach it. A remainder that is not zero, positive or negative, is `history-open`. Exactly zero is `clear`.

**Evidence.**

- Incident: a live NetSuite run, 2026-10-12. The bill's own figures tied. The PO's approved billing history ran ahead of the vendor's previously-billed figure with the gap unexplained. The run flagged it.
- Related: F189, NetSuite cannot fold rows. Its premise changed with this decision.

**Checks.** `scripts/test_skill_code.py`: `test_history_open_verdict`, `test_history_open_vocabulary_checks`, and the row-class map in `test_verdict_render_guard`.
