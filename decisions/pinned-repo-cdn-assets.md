---
id: pending
slug: pinned-repo-cdn-assets
kind: decision
status: settled
date: 2026-10-21
---
# Dashboards may load fixed assets from a pinned repo copy

**Rule.** A dashboard may load its fixed CSS and JS from this repo through jsdelivr `/gh/`. The URL names a full commit sha. The tag carries an SRI `sha384` hash. Both are required. Built. Not yet pinned.

The repo stays public on the `ssemwal-cdc` account under its current name. Merges keep the pinned commit: merge method `merge`, never squash or rebase.

**Outcome protected.** A dashboard stays small enough to render in one read. The code it runs is the code reviewed in this repo.

**Argument.**

D95, a skill never shapes its way past a filter, bars a run from hiding what it does. A pinned load is not that. This repo holds the reviewed code. The pin names one commit. The 2026-11-11 probe showed that a wrong hash blocks the load. Without the pin and the hash it would be unreviewed code. So both are the whole condition.

The pin only resolves while the repo is public and keeps its name and account. See D13, keep this repo public. A squash or rebase merge rewrites the commit, and the pinned sha would stop resolving.

Owner ruling, 2026-10-21. The probe in F‹widget-readystate-complete›, the widget runs scripts late, showed a pinned `<script src>` loads in the widget.

**Status.** Built. Not yet pinned.

- The check is `check_asset_pins` in `scripts/shared_blocks.py`. `validate.py` runs it in the call list that `--check` shares. Its tests are in `scripts/test_asset_pins.py`.
- `python3 scripts/shared_blocks.py --pin <sha>` writes the sha, the `sha384` and `crossorigin="anonymous"` into every pinned or placeholder tag in every shell. The placeholders are `__PIN_SHA__`, `__PIN_CSS_SRI__` and `__PIN_JS_SRI__`.
- Each dashboard shell is a template plus `dashboard.css` and `dashboard.js`. Publish inlines any asset whose tag still holds `__PIN_`. A pinned tag stays a CDN tag. Inline fallback lasts one run: D‹inline-fallback-per-run›, a flag that is never stored.

**What the check refuses.** Each refusal is a check failure.

- In a shell, a `<script src>` or `<link href>` must be the pinned form or the placeholder form. Its file must sit in that shell's own `assets/` folder.
- In a shell, a CDN URL in an inline script or style must be the pinned form.
- In a shell, no CSS `@import`. See D‹no-css-import-in-shell›, the ruling on CSS imports.
- In an assets `.js` or `.css` file, no URL on `cdn.jsdelivr.net`, `unpkg.com`, `cdnjs.cloudflare.com` or `esm.sh`.
- In an assets `.css` file, no `@import`.
- A URL inside an HTML comment passes. Publish strips comments first.

**Pin form.** A pin is a full 40-hex sha. The check reads three states: pass, fail and unknown. The sha must exist, be an ancestor of HEAD, and hold the same file as HEAD. The tag's `integrity` must be the `sha384` of that file at the pin. A short sha or a ref fails. A clone with no git, or a shallow clone that lacks the pinned sha, gives unknown, never a pass. One pin per plugin: D‹one-pin-per-plugin›, the rule that `--pin` carries out.

**Merges.** The merge tool appends a claim commit on top of the PR head. It does not rewrite branch commits, so the pinned commit survives. Read in the merge tool's source, 2026-11-11.

**Evidence.**

- Probe, 2026-10-21: a `<script src>` from `cdn.jsdelivr.net/gh/ssemwal-cdc/claude-sharables@<full sha>` loaded in the widget.
- Owner probe, 2026-11-11: a script and a stylesheet with the correct sha384 loaded. The same files with a wrong value were blocked. See F‹widget-readystate-complete›, the widget runs scripts late.

**Known limits (notes, not debts).** Found in review round 3 of the pin check, 2026-11-11. None is a debt.

- The check does not read `.htm`, `.mjs`, nested asset folders, iframes or SVG `href`. These are attacker-only forms.
- `@import url("data:...")` passes in a shell's inline `<style>`. It is refused in an assets `.css` file.
- An `@import` inside a CSS comment in an assets `.css` file raises a false alarm.
- The CDN host check is a four-host denylist: the four hosts named in the refusals above.

**Checks.** `scripts/test_asset_pins.py`, with `check_asset_pins`.

Kind: process
Home: scripts/shared_blocks.py
