import os, json
src='plugins/procore-open-items-review/skills/procore-open-items-review/SKILL.md'
L=open(src,encoding='utf-8').read().split('\n')
SEG={
 'F01':(58,61),'SH1':(65,149),'F02':(150,156),'SH2':(158,168),'F03':(194,196),
 'F04':(225,228),'F_CFG':(269,300),'F05':(337,339),'F06':(402,407),'F07':(415,417),'F08':(426,452),
 'F09':(474,476),'F10':(482,485),'F11':(516,518),'F12':(526,528),'F13':(544,546),
 'F14':(554,557),'F15':(578,584),'F16':(598,618),'F17':(622,639),'F18':(662,683),
 'F19':(701,706),'T_REG':(748,773),'F20':(955,989),'F21':(1009,1011),
 'SH3':(1057,1064),'SH4':(1066,1091),'F22':(1109,1111),
}
out={}
for k,(a,b) in SEG.items():
    out[k]='\n'.join(L[a-1:b])
json.dump(out,open('.seg.json','w'))
print('wrote', len(out), 'segments')
