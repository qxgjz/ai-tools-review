# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8')); now='2026-10-26T18:47:00'
done={
'CTR-PAGE-AI-POLICY-20261026':'/ai-policy非posts.json文章页，留window1。',
'CTR-PAGE-HOMEPAGE-CANONICAL-20261026':'首页title/meta属模板层app/layout，留window1。',
'CTR-PAGE-MEETING-ASSISTANTS-20261026':'已54/143达标（R34），复验通过。',
'CTR-PAGE-OBSERVABILITY-20261026':'已52/140达标（R34），复验通过。',
'CTR-PAGE-PRODUCTIVITY-20261026':'已52/141达标（R34），复验通过。',
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in done and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=done[t['id']]; closed.append(t['id'])
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
