import re, sys
p='plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md'
L=open(p,encoding='utf-8').read().split('\n')
cur='(front)'; counts={}; order=[]
infence=False
for ln in L:
    if re.match(r'^ *```', ln): infence = not infence
    if not infence and re.match(r'^#{1,3} ', ln):
        cur=ln.strip()[:48]
    if cur not in counts: counts[cur]=0; order.append(cur)
    counts[cur]+=1
for k in order: print('%5d  %s' % (counts[k], k))
print('TOTAL', len(L))
