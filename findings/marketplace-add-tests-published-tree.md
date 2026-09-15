---
id: F78
slug: marketplace-add-tests-published-tree
kind: finding
status: observed
date: 2026-08-26
---
# marketplace add tests the release

**Outcome protected.** A pre-push check answers the question a maintainer asked it.

**Argument.**

`claude plugin marketplace add .` does not test local changes. The snippet in this repo claimed it did for months.

Two things were wrong. The bare dot is rejected outright, so the argument must be `./`.

With `./` the command succeeds while testing the wrong tree. The local path is used to read `marketplace.json` alone. Every plugin content read then comes from the `url` in its `git-subdir` source, at `main` on GitHub.

So the sequence answers whether the published release installs. It never answers whether what you are about to push is installable.

The failure is silent and inverted. The route prints `Successfully installed` either way, so a broken change reads as verified.

The pre-push check is F81, plugin-dir loads the working tree.

**Evidence.**

- Corrected by observation 2026-08-26. Local `HEAD` carried an unpushed new skill version, and the fresh install reported the previous version.
- The cache directory under `~/.claude/plugins/cache/compass-claude-plugins/` was named for the SHA that `git ls-remote origin refs/heads/main` returns.
- The rejection text is `Invalid marketplace source format. Try: owner/repo, https://..., or ./path`.

**Checks.** none
