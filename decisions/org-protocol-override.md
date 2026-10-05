---
id: D79
slug: org-protocol-override
kind: decision
status: settled
date: 2026-10-05
---
# Repo workflow beats org protocol

**Rule.** Edit `plugins/<name>/` in place and push. When the user asks for a plugin file, package it from `main`.

**Outcome protected.** The repo stays the one source of a plugin, and a push to `main` is the release.

**Argument.**

Some sessions arrive with an organisation instruction to copy a plugin out, repackage it, and deliver an archive. That instruction is written for a plugin that lives somewhere else. This repo is the source of truth.

Three reasons, in the order they bite. The git working tree is the plugin that ships, so a working copy has no upstream to sync back to. A push to `main` is the release. An uploaded archive installs as a local upload with no marketplace source behind it. The tooling the instruction names is absent, because this repo has no `skill-creator` and no `package_skill` script.

Name the divergence in the reply. A maintainer must see which instruction was set aside and why.

Amended 2026-10-05 by the maintainer. The ban on handing a plugin over as a file is deleted. A file is built from `main` only, on the user's request. An uploaded copy does not update on a push, so say so when you hand one over.

**Evidence.**

- Recorded 2026-09-10 after a session followed the repo workflow and flagged the conflict. The flag was confirmed correct.
- The local-upload copy never syncs. That follows from the install shape. Nobody tested it, so it is `unmeasured`.
- The checks that exist are `scripts/validate.py`, `scripts/test_skill_code.py` and `claude --plugin-dir`.

**Checks.** `scripts/validate.py` runs on every build. No check can see a packaged hand-off.
