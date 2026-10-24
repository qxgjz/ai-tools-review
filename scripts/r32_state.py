# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8')); now='2026-10-25T12:10:00'
done={
'CTR-OPT-OBSERVABILITY-TOOLS-20261024':'best-ai-observability-tools-2026 title 50字符去AIToolCrux尾；excerpt 150字符含rankings/free tiers。已改posts.json。',
'CTR-OPT-GEMINI-CLI-REVIEW-20261024':'无gemini-cli专页；抛光最相关落地页gemini-pricing-2026 title/excerpt含Gemini pricing关键词。留创作家后续建专页。',
'CTR-OPT-COPILOT-PRICING-QUERY-20261024':'github-copilot-review-2026 R31已优化title/pricing；本轮保持。',
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in done and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=done[t['id']]; closed.append(t['id'])
for t in s['next_iteration_focus']:
    if t.get('id')=='P0-CMD-POLISHER-TLDR-URGE-20261024':
        t['progress_note']='R32再+32篇TL;DR，覆盖58→90/238；缺口180→148。继续后续轮批量，留pending。'
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
