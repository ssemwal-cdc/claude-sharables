Cut from `scripts/test_skill_code.py` by review-only-mode. Verbatim; do not edit.

===== scripts/test_skill_code.py lines 186-227 =====
# --------------------------------------------------------------- 3. gate states
def test_gate_states():
    body = js_block(os.path.join(PC, "SKILL.md"), "__gate")
    harness = r"""
var window = {};
""" + body + r"""
const EQ = String.fromCharCode(61), AMP = String.fromCharCode(38);
global.fetch = async function(u){
  const id = u.split('object_id]'+EQ)[1].split(AMP)[0];
  if (id === '2') return {ok:false, status:429};          // rate limited
  if (id === '3') return {ok:true, json: async()=>[]};    // genuinely no instance
  if (id === '4') throw new Error('network down');
  return {ok:true, json: async()=>[{
    user_permissions:{can_respond: id === '1'},
    current_step_occurrence:{name:'FA Review', due_at:'2026-08-20',
                             available_responses:['Approve']}}]};
};
(async () => {
  const rows = [1,2,3,4,5].map(n => ({key:'k'+n, pid:'999', id:String(n), type:'GenericToolItem'}));
  const out = await window.__gate(rows, 3);
  const by = k => out.find(r => r.key === k);
  console.log(JSON.stringify({
    total: out.length,
    rateLimitIsFailed: by('k2') && by('k2').state === 'failed',
    throwIsFailed:     by('k4') && by('k4').state === 'failed',
    emptyIsEmpty:      by('k3') && by('k3').state === 'empty',
    canRespondHonoured: by('k1').can === true && by('k5').can === false,
  }));
})();
"""
    rc, out, err = run_node(harness)
    if rc != 0:
        check("gate fan-out runs", False, err.splitlines()[0] if err else "non-zero exit")
        return
    r = json.loads(out)
    check("gate: every item accounted for", r["total"] == 5, "got %s" % r["total"])
    check("gate: a 429 is `failed`, never `empty`", r["rateLimitIsFailed"])
    check("gate: a thrown request is `failed`", r["throwIsFailed"])
    check("gate: a genuine no-instance is `empty`", r["emptyIsEmpty"])
    check("gate: can_respond is read correctly", r["canRespondHonoured"])



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

