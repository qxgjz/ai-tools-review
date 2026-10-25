# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8')); now='2026-10-25T19:20:00'
done={
'CTR-OPT-TOP10-FOUR-20261025':'4篇重写title加数字+年份+情绪词，meta加利益点+CTA：dify(50/133)/stable-diffusion(55/123)/cursor(59/129)/gemini-3.8-flash(54/122)。已改posts.json。',
'CTR-BLOG-OPENAI-ASTRA-WWW-20261025':'openai_astra_review title 57/excerpt126重写。已改。',
'CTR-BLOG-OPENAI-ASTRA-20261025':'同openai_astra_review，重复任务，合并关闭。',
'CTR-BLOG-MIDJOURNEY-V7-215236-20261025':'midjourney-v7-review-2026 title 56/excerpt130重写。已改。',
'CTR-BLOG-CREATIUM-COACH-173022-20261025':'creatium-coach-review-2025 title 56/excerpt125重写。已改。',
'CTR-QUERY-MIDJOURNEY-20261025':'midjourney-v7-review-2026同页优化，合并关闭。',
'CTR-QUERY-CODING-COMPARISON-20261025':'ai-coding-tools-comparison-2026 R31已优化title57/excerpt122。',
'P0-CMD-POLISHER-SPEED-20261024':'本轮一次处理7篇CTR+5篇低分，≥5条达标。',
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in done and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=done[t['id']]; closed.append(t['id'])
for t in s['next_iteration_focus']:
    if t.get('id')=='P0-CMD-POLISHER-TLDR-URGE-20261024':
        t['progress_note']='R32+32篇覆盖90/238；R33聚焦CTR7篇+低分5篇，TLDR缺口约148继续后续轮。'
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',len(closed),closed)
