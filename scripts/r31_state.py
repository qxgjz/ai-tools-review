# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8'))
now='2026-10-24T20:30:00'
done={
'CTR-OPT-AI-CODING-COMPARE-20261024':'title 57字符含关键词；excerpt 122字符含价值点/CTA。已改posts.json。',
'CTR-OPT-BEST-COMPARE-20261024':'title 50字符；excerpt 126字符含rankings/pricing/free tiers。已改posts.json。',
'CTR-OPT-GH-COPILOT-QUERY-20261024':'github-copilot-review-2026 title 56字符含pricing/pros；excerpt 123字符含30天实测。已改。',
'P0-GEO-TLDR-TABLE-20261023':'R31复核：25+5+33=58篇含## TL;DR，内容无损，重新completed。',
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in done and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=done[t['id']]; closed.append(t['id'])
# progress note on urge task
for t in s['next_iteration_focus']:
    if t.get('id')=='P0-CMD-POLISHER-TLDR-URGE-20261024':
        t['progress_note']='R31本轮+33篇高价值review/comparison，全库TL;DR 25→58/237；缺口212→179。目标≤20需继续批量，留pending。'
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
