---
id: F4
slug: git-url-needs-dot-git
kind: finding
status: observed
date: 2026-08-11
---
# A git URL needs .git

**Outcome protected.** A marketplace URL clones the repo instead of reading one file.

**Argument.**

A full git URL needs the `.git` suffix.

Without the suffix, Claude Code treats the URL as a direct link to a hosted `marketplace.json`. It does not treat the URL as a repo to clone.

The `owner/repo` shorthand also works, and that is what `README.md` tells teammates to use.

**Evidence.**

- Verified 2026-08-11. `https://github.com/ssemwal-cdc/claude-sharables.git` works.

**Checks.** none
