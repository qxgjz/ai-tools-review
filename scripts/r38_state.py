# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8')); now='2026-10-27T12:20:00'
done={
'CTR-OPT-AI-POLICY-20261024':'/ai-policy非posts.json文章页，留window1。',
'CTR-PAGE-COMPARISON-TOOLS-SLASH-20261026':'best-ai-comparison-tools-2026已50/126达标（R35），复验通过。',
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in done and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=done[t['id']]; closed.append(t['id'])
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
