import json, re, sys
dst='plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md'
seg=json.load(open('.seg.json'))
old=open(dst,encoding='utf-8').read()
# the frontmatter description, verbatim apart from the version prefix
m=re.search(r'^description: (.*)$', old, re.M)
desc=m.group(1)
assert desc.startswith('v27 — '), desc[:20]
seg['DESC']='v28 — '+desc[len('v27 — '):]
tpl=open('.skill_new.tpl',encoding='utf-8').read()
missing=[k for k in re.findall(r'@@([A-Z0-9_]+)@@', tpl) if k not in seg]
if missing:
    sys.exit('no such segment: '+', '.join(sorted(set(missing))))
unused=[k for k in seg if '@@%s@@'%k not in tpl]
out=re.sub(r'@@([A-Z0-9_]+)@@', lambda mm: seg[mm.group(1)], tpl)

# Drop blank lines that CommonMark does not need, so the shipped prompt stays short.
# Shared-block regions are copied through untouched, markers included.
L=out.split('\n')
keep=[None]*len(L)
insh=False
for i,ln in enumerate(L):
    if '__SHARED:' in ln: insh=True
    keep[i]=insh
    if '__END_SHARED:' in ln: insh=False
def kind(s):
    s=s.strip()
    if not s: return 'blank'
    if s.startswith('|'): return 'table'
    if s.startswith('>'): return 'quote'
    if s.startswith('#'): return 'head'
    if s.startswith('```') or s.startswith('   ```'): return 'fence'
    if re.match(r'^([-*]|\d+\.)\s', s): return 'list'
    return 'para'
res=[]; infence=False
for i,ln in enumerate(L):
    if re.match(r'^ *```', ln): infence = not infence
    if keep[i] or infence or ln.strip():
        res.append(ln); continue
    # this is a blank line outside fences and shared regions
    prv=next((L[j] for j in range(i-1,-1,-1) if L[j].strip()), '')
    nxt=next((L[j] for j in range(i+1,len(L)) if L[j].strip()), '')
    if '__SHARED' in prv or '__SHARED' in nxt:
        res.append(ln); continue
    kp, kn = kind(prv), kind(nxt)
    if kn in ('table','quote'):          res.append(ln); continue
    if kp == 'quote':                    res.append(ln); continue
    if kp in ('list','table') and kn == 'para': res.append(ln); continue
    if kp == 'para' and kn == 'para':    res.append(ln); continue
    # otherwise the following block starts on its own; the blank is not needed
out='\n'.join(res)
open(dst,'w',encoding='utf-8').write(out)
print('wrote', dst, len(out.split('\n')), 'lines; unused segments:', sorted(unused) or 'none')
