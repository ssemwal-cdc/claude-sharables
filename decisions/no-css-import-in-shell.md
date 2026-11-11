---
id: D119
slug: no-css-import-in-shell
kind: decision
status: settled
date: 2026-11-11
---
# No CSS import in a shell or an assets stylesheet

**Rule.** A dashboard shell takes no CSS `@import`, pinned or not. An assets `.css` file takes no `@import` either. Load CSS with a pinned `<link>`.

**Outcome protected.** A dashboard loads no code that its pin does not name. An `@import` would pull in a file that no `integrity` hash covers.

**Argument.**

A pinned `<link>` names one commit and one `sha384`. The browser checks the file against that hash. An `@import` inside a stylesheet fetches another file that no hash checks. So the rule refuses it, even when the stylesheet itself is pinned.

**Evidence.**

- Ruling, 2026-11-11, by the orchestrating session under the owner's 2026-10-21 grant.
- Check `check_asset_pins`: a shell's inline `<style>` refuses an `@import`, except one whose URL starts `data:`. An assets `.css` file refuses any `@import`.

**Checks.** `check_asset_pins` in `scripts/shared_blocks.py`. Tests in `scripts/test_asset_pins.py`.

Kind: process
Home: scripts/shared_blocks.py
