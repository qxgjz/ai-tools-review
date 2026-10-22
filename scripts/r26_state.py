# -*- coding: utf-8 -*-
import io,json,os,datetime
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'
s=json.load(io.open(fn,encoding='utf-8'))
now='2026-10-22T19:10:00'
close_notes={
'CTR-ADOBE-FIREFLY-20261021':'R26核验合规，无需改写：title 58c、excerpt 154c，关键词adobe firefly在标题，长度达标(50-60/120-155)；imp=1为样本噪声，CTR=0非meta缺陷。',
'CTR-AI-CODING-TOOLS-20261021':'R26核验合规（R23已修）：title 57c、excerpt 154c含CTA Pick your best AI coding assistant today；imp=3噪声。',
'CTR-AI-POLICY-20261021':'R26核验合规：app/ai-policy/page.tsx title 50c、description 146c，关键词AI Usage Policy在标题；政策页无需交易CTA。',
'CTR-ASTRA-REVIEW-20261022':'R26核验合规：openai_astra_review title 56c含astra review、excerpt 128c含价值点；imp=1噪声，meta达标不改写。'
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in close_notes and t.get('status')=='pending':
        t['status']='completed'; t['completed_at']=now; t['close_note']=close_notes[t['id']]
        closed.append(t['id'])
# mirror into completed_tasks
for cid in closed:
    rec=next((t for t in s['next_iteration_focus'] if t.get('id')==cid),None)
    if rec and not any(x.get('id')==cid for x in s.get('completed_tasks',[])):
        s.setdefault('completed_tasks',[]).insert(0,rec)
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
