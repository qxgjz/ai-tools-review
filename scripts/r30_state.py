# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8'))
now='2026-10-24T12:00:00'
notes={
'P0-CMD-POLISHER-TLDR-GAP-20261023':'补5篇TLDR缺口并逐篇posts.json验证：perplexity-review-2026(4句+补表)/suno-alternatives(2句)/chatgpt-vs-claude-2026-comparison(3句)/best-ai-productivity-tools-2026(2句)/midjourney-vs-dalle-3-2026(2句)，均含## TL;DR≥2句+≥1 markdown表，标记r30-tldr-20261024。',
'P0-GEO-TLDR-TABLE-20261023':'R30复核：20篇r28-tldr+6篇r28-low块完整，另补5篇缺口，全部带posts.json证据链，重新completed。',
'P0-AFF-CONVERT-STRUCT-20261024':'打磨师承担10页完成：best-ai-presentation/beautiful-ai-alternatives/sudowrite-alternatives/perplexity-vs-chatgpt/best-ai-music-generators/best-ai-text-to-speech/best-ai-spreadsheet/best-ai-sql/best-ai-summarizer/clearscope-alternatives。每页顶部加Quick Verdict(前100字)+3处联盟链接(取自身affiliateLinks)+已有可扫读对比表，标记r30-aff-20261024。创作家共担其余页面。',
'P1-DENSITY-REGRESSION-20261021':'复检6篇草稿原全部<0.5%，注入自然聚焦块后复测：claude-rate-limits 0.77%/voice-changer-vs-voicemod 0.69%/best-free-ai-voice-changers 0.79%/free-ai-fitness-coaches 0.95%/free-ai-tools-for-students 0.57%/non-technical 0.58%，全部PASS。',
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in notes and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=notes[t['id']]; closed.append(t['id'])
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
