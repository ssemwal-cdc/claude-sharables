import re
p='plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md'
L=open(p,encoding='utf-8').read().split('\n')
fence=0; shared=0; table=0; blank=0; head=0; bullet=0; para=0
inf=False; insh=False
for ln in L:
    if '__SHARED:' in ln: insh=True
    if insh:
        shared+=1
        if '__END_SHARED:' in ln: insh=False
        continue
    if re.match(r'^ *```', ln):
        inf = not inf; fence+=1; continue
    if inf: fence+=1; continue
    s=ln.strip()
    if not s: blank+=1
    elif s.startswith('|'): table+=1
    elif s.startswith('#'): head+=1
    elif re.match(r'^([-*]|\d+\.) ', s): bullet+=1
    else: para+=1
print('fence',fence,'shared',shared,'table',table,'blank',blank,'head',head,'bullet',bullet,'para',para)
print('total',len(L),'sum',fence+shared+table+blank+head+bullet+para)
