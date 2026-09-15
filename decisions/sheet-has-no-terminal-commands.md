---
id: pending
slug: sheet-has-no-terminal-commands
kind: decision
status: settled
date: 2026-08-24
---
# No terminal commands in sheet

**Rule.** Keep terminal commands out of the onboarding sheet. Keep them in the maintainer notes and in `README.md`.

**Outcome protected.** A teammate reading the sheet sees instructions for the app they are using.

**Argument.**

The terminal and app split was resolved twice, and deleting won.

The split had just been documented, and the sheet taught it. The terminal blocks were kept and labelled, with confusion-table rows for the terminal-side errors.

Labelling is the more informative fix and it is not the one asked for.

The reader of that sheet has no terminal install. The sheet walks them through the app, start to finish.

So every terminal block was reference material for a thing they do not have, in the middle of instructions they do.

Three confusion-table rows went with the commands. Those rows document errors only a terminal command produces, so with the commands gone they describe failures the reader cannot reach.

Nothing verified was lost. The screenshot-verified in-app force-update path and the which-version question are what the update section is made of, and the app-side last-updated row stayed.

The maintainer-facing command guidance stays in this repo, because the maintainer does work in a terminal.

Do not restore consistency by putting the commands back in the sheet. If a teammate ever does end up with a terminal install, the commands are in the maintainer records.

**Evidence.**

- Deleted 2026-08-24. Three rows and two command blocks came out.
- The commands live in F‹two-command-update›, update needs the marketplace qualifier.
- The two commands are different things. See F‹plugin-command-two-surfaces›, two plugin commands exist.

**Checks.** none
