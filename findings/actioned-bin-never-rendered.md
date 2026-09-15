---
id: pending
slug: actioned-bin-never-rendered
kind: finding
status: settled
date: 2026-08-24
---
# Actioned bin never rendered

**Outcome protected.** The queue count on the dashboard matches the queue.

**Argument.** A documentation sweep found this, not a run.
That is the point worth keeping, because neither plugin would ever have reported it.
Both skills' carry-forward rules kept an item for one run after it left the queue.
The stated reason was so the dashboard could show it in the actioned bin.
Neither bin could render.

**NetSuite's was collateral from the same day.** Its bin was fed by the `gone` state.
That state belonged to the dead `live` machinery, removed earlier that day as unreachable.
The instruction that fed the bin was not updated with it.
That is self-inflicted drift, caught within hours only because the sweep went looking.

**Procore's never worked, and the guard that blocks it was added deliberately.**
Its template filtered `bin` on `verdict === "gone"`.
`gone` is not in Step 6's vocabulary.
The publish script's `VERDICTS` allowlist would abort on it.
So the bin never rendered in any run.
It could not render without a fourth verdict nobody defined.

**The harm was mild and real.** A departed item lingered as an apparently pending row for one run.
That inflated the queue count.
Execute would have skipped it, because it re-verifies before every click.
So this could never have caused a wrong click, only a wrong number.
Both rules now say drop the item.
Both bins are gone.
Procore's markup, CSS and filter were removed once no run could reach them.
Finishing the bin would have meant inventing a fifth verdict nobody had asked for.

**This turned out to be automatable.** The first version of this note said it probably was not.
`check_verdict_vocabulary()` asserts every verdict a template branches on is one its script can emit.
It reproduces the Procore bin exactly.
It is mutation-tested.
The first attempt at that test passed silently, because the injecting `sed` had not applied.
So the check looked verified when nothing had been checked.
Re-run properly, it fires and names the file, the verdict and the allowlist.
A check that passes because the mutation never landed is worse than no check.
It also certifies itself.

**The honest residue is not automated.** Removing dead code leaves live prose pointing at it.
Nothing catches that.
`validate.py` checks that the docs mention every plugin.
It never checks that the docs describe behaviour the code still has.
The NetSuite instruction that survived its own bin's deletion was found by reading docs against code.
The verdict check covers one narrow machine-settleable slice of that.
The rest is still a person reading.

**Evidence.** Found 2026-08-24 by a documentation sweep.
The Procore bin had never rendered in any run since it shipped.
The queue-count inflation was one row per departed item, for one run. `unmeasured` in aggregate.

**Checks.** `check_verdict_vocabulary()` in `scripts/shared_blocks.py`, mutation-tested.
