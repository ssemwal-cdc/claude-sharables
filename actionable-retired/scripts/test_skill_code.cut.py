Cut from `scripts/test_skill_code.py` by review-only-mode. Verbatim; do not edit.

===== scripts/test_skill_code.py lines 579-607 =====
        # position:sticky resolves against the PARENT box. On .bar the parent is exactly as
        # tall as the bar, so it never travels - measured in a real browser, not assumed.
        # Asserts the mechanism, not the styling: pinning .bar's full declaration string
        # here made a pure restyle read as a sticky regression (2026-08-21).
        m_bar = re.search(r"\.bar\{[^}]*\}", tpl)
        check("%s: sticky sits on #bar, not .bar" % label,
              "#bar{position:sticky" in tpl and bool(m_bar) and "sticky" not in m_bar.group(0))
        check("%s: the sticky bar has a container to travel in" % label,
              'class="worksec"' in tpl and ".worksec{position:relative}" in tpl)

        # CLAUDE.md has asserted since 2026-08-19 that a test covers this. Until now it did
        # not. A marked item hidden behind a filter still has to execute, so narrowing the
        # bar to the filtered rows would silently discard decisions already made.
        bar = re.search(r"function renderBar\(\)\{(.*?)\n\}", tpl, re.S)
        check("%s: renderBar is present" % label, bool(bar))
        if bar:
            body = bar.group(1)
            check("%s: renderBar counts REVIEW.items, never the filtered rows" % label,
                  "REVIEW.items" in body and "applyView" not in body)

        # The execute affordance has to exist before anything is marked, or step 2 is
        # invisible until the reader has already worked out step 1 unaided.
        if bar:
            check("%s: the bar renders unconditionally, zero marks included" % label,
                  'getElementById("bar").innerHTML=\'<div class="bar">\'' in bar.group(1) and
                  'getElementById("bar").innerHTML=\'<p class="note"' not in bar.group(1))
        check("%s: the header mirror is wired" % label,
              'id="topexec"' in tpl and 'getElementById("topexec")' in tpl)

