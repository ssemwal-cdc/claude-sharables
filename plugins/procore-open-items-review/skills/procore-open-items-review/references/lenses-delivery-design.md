# The `delivery` and `design` lenses

Read this file only when `config.focus.lenses` names `delivery`, `design`, or both. It is
Step 5's lens section, moved out of the spine because most runs never select either lens.

**Skip a lens's checks unless it is selected.** Absent both, Step 5 ends before this file.
**Read this first, because it governs every check in both lenses.** Procore records carry
scope, schedule and design origin unevenly. A narrative field may be thorough, terse, or
blank, and none of those is misconduct. So both lenses are **lenient by design**.

- **Missing or thin information is never a finding.** A blank schedule-impact field means nobody filled it in, **not** that the change has no schedule impact. Report what is there. Never infer an absence into a claim.
- **Three states, never a boolean:** `stated` means the record says it, `absent` means the field exists and is empty, `failed` means the read errored. `failed` is never `absent`.
- **These lenses add context. They do not add flags.** A lens check produces a line in `facts` or `context`, never a `flagged` verdict on its own. No exceptions.
- The financial checks in `core` decide the verdict. These tell a reader what the change *touches*.
- **`pc.del-schedule-impact`** reports the ICR's `schedule_impact` alongside its cost impact. Where it is blank, say it is unstated rather than saying there is none.
- **`pc.del-scope-affected`** names **what the change touches**, from the narrative's Scope section: which buildings, systems or trades.
- **`pc.del-ofci`** names owner-furnished equipment the change references, and says which side of the delivery hand-off it sits on.
- **`pc.dsn-change-origin`** says **what caused the change**: an RFI, a bulletin, a drawing revision, a spec section, a field condition, or unstated.
- **`pc.dsn-drawing-ref`** pulls drawing, sheet, spec and bulletin references out of the record and its support. **Report them as found. Do not verify them.**
- This skill cannot open the drawing set, and a reference it cannot resolve is not thereby wrong.
- **`pc.dsn-unknown-workflow`** lists every queue row whose `item_type` is not one of the four, with its `title` and `url`, under a plain heading. Say in that heading that these are workflows this skill does not yet know.
- **Never review such an item, never guess its verbs, and never let it reach the execute list.**

**On what these lenses cannot reach, stated plainly because it matters most to design.**
This skill reviews the workflow-response queue from `open_items/mine`. **The daily
substance of design management lives in other Procore tools and does not appear in this
queue.** That covers RFI response, submittal review and drawing issuance. So the `design`
lens covers *design-driven change* well and *design production* not at all. Say so if
asked. Use `pc.dsn-unknown-workflow` to surface anything that does turn up.
