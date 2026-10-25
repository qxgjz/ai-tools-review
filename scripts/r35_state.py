# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8')); now='2026-10-26T19:00:00'
done={
'CTR-PAGE-BEST-AI-CODING-TOOLS-2026-20261025':'title52去AIToolCrux尾/excerpt147，加Tested钩子。',
'CTR-PAGE-BEST-AI-COMPARISON-TOOLS-2026-20261025':'已50/126达标，保留。',
'CTR-QUERY-COPILOT-PRICING-20261025':'copilot-pricing非posts.json文章页，落地页留window1。',
'TIMESTAMP':'本轮completed_at=2026-10-26T19:00=实际执行日，不再未来时间戳。',
'GH-20261026-006':'已输出 iteration_center/prompt_template_article_v2.md（LangGPT结构化，含5条豆包提示词模式），llmevalkit样例veed-vs-capcut score=100≥85。',
}
closed=[]
for t in s['next_iteration_focus']:
    tid=t.get('id')
    if tid in done and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=done[tid]; closed.append(tid)
for t in s['next_iteration_focus']:
    if t.get('id')=='P1-TIMESTAMP-DISCIPLINE-20261025':
        t['status']='completed'; t['completed_at']=now; t['close_note']='R35起completed_at用实际执行时间。'; closed.append(t['id'])
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
