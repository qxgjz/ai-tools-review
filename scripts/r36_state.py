# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8')); now='2026-10-26T12:16:00'
done={
'CTR-PAGE-AI-CODING-TOOLS-COMPARISON-20261026':'已56/135达标（R34），复验通过。',
'CTR-PAGE-CREATIUM-COACH-REVIEW-20261026':'creatium-coach-review-2025已56/125达标（R33）；article-api丑陋URL留window1 301。',
'CTR-QUERY-TABBYML-20261026':'tabbyml无对应posts.json文章页，留window1。',
'P0-TIMESTAMP-DISCIPLINE-REOPEN-20261026':'R36起completed_at=实际执行时刻2026-10-26T12:16，已写日志声明。',
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in done and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=done[t['id']]; closed.append(t['id'])
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
