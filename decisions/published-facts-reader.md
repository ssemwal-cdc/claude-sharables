---
id: pending
slug: published-facts-reader
kind: decision
status: settled
date: 2026-09-18
---
# Published facts reader

**Rule.** Ruling 3 of `D‹markdown-compliance-fix-plan›`, the markdown
compliance fix plan, gets a full, independent accounting. No fact from the
four files is dropped silently.

**Outcome protected.** A published number or path in `CLAUDE.md` or a README
has a reader. Either a script would catch it drifting, or it is honest,
cited prose.

**Argument.**

The 2026-09-16 audit found 37 published numbers and paths with no reader.
That audit's own item list was not handed to this lane. This record
re-enumerates `CLAUDE.md`, `README.md` and both plugin `README.md` files
from scratch. Its count will not match 37 item for item. It is a full
accounting on its own terms, not a reproduction of the audit's list.

**Already had a reader, before this lane.** `validate.py` already checked
several things. A plugin or skill name named in the docs must resolve to a
real plugin or skill. `${CLAUDE_PLUGIN_ROOT}` asset paths must exist. Each
README Version cell must match its `SKILL.md` version line. The four
version sites must agree. `marketplace.json` and every `plugin.json` must
exist, or the build fails outright.

**Given a reader this lane.** These checks are new, all in
`scripts/validate.py` unless noted:

- Every `scripts/` or `.github/workflows/` path named in `CLAUDE.md` or a
  README must exist on disk. This covers a backtick span and a fenced
  example alike.
- A marketplace name named by any of its three forms must match
  `marketplace.json`.
- A GitHub repo URL named in prose must be this repo.
- `docs/onboarding.html` must exist, or the build fails.
  `scripts/shared_blocks.py`'s `check_onboarding_page()` silently returned
  `[]` on a missing file before this lane. See
  `F‹onboarding-check-silent-on-missing-file›`, the check passed on a
  missing file.
- `docs/index.html` must exist. `README.md` links the GitHub Pages root,
  which redirects through it.
- The NetSuite README's and `SKILL.md`'s published "3 hours" staleness
  warning must match `dashboard_template.html`'s `isStale()` threshold.
- `check_visual_read_mentions()`, in `scripts/check_records.py`. See
  `F79`, NetSuite visual read prose thin.

**Left as honest prose, on purpose.** Each of these is a claim a script
cannot observe from this checkout. Each stays prose, cited or marked
`unmeasured`, rather than given a fake reader:

- The default branch is `main`. That is a GitHub repository setting, not
  content in this checkout. Nothing here can read it without a network call.
- Every desktop-app UI path, such as `Settings → Plugins → Add → Add
  marketplace`. These name buttons in software this repo does not ship.
- `.claude/settings.json`'s `enabledPlugins` key, in the cloud-session
  paragraph. That file lives in a different repository, not this one.
- GitHub Pages' own serving behaviour and auto-update's background timing.
  These are platform behaviour, already marked `unmeasured` where they carry
  a measurement claim.
- Two dated observations in `README.md` had no citation before this lane.
  Cowork install verification now cites `F2`, Cowork runs installed plugins.
  The commit-SHA-as-version observation now cites `D9`, no version field.
- The Procore README's "60-second presigned S3 link" restated Procore's own
  link lifetime as this repo's fact. This lane dropped the figure, the same
  move ruling 10 made for the "75 down to 32" figures. It now points at
  `D24`, do not overrun the window, and carries `unmeasured`.

**Evidence.** This is an independent re-enumeration performed 2026-09-18. It
is not a transcript of the 2026-09-16 audit's own item list. The exact count
against that audit is `unmeasured`.

**Checks.** The bullets above name each one. Run `python3 scripts/validate.py`
and `python3 scripts/check_records.py`.
