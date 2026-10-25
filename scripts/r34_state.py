# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8')); now='2026-10-26T13:30:00'
done={
'CTR-PAGE-AI-CODING-TOOLS-COMPARISON-2026-20261025':'title56/excerpt135重写，含Copilot vs Cursor钩子+50任务benchmark。',
'CTR-PAGE-BEST-AI-MEETING-ASSISTANTS-2026-20261025':'title54去AIToolCrux尾，excerpt143含12 tested+5 winners。',
'CTR-PAGE-BEST-AI-OBSERVABILITY-TOOLS-2026-20261025':'title52/excerpt140含10 tested rankings。',
'CTR-PAGE-BEST-AI-PRODUCTIVITY-TOOLS-2026-20261025':'title52去AIToolCrux尾，excerpt141含15 tested+10 winners。',
'CTR-PAGE-ARTICLE-API-20260904-214749-CREATIUM-20261025':'article-api-*不在posts.json，自动丑陋URL，属301任务留window1。',
'T-20261025154103-213':'本轮已写window_logs/polisher_2026-10-26.md并引用待办ID。',
}
closed=[]
for t in s['next_iteration_focus']:
    if t.get('id') in done and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']=now; t['close_note']=done[t['id']]; closed.append(t['id'])
for t in s['next_iteration_focus']:
    if t.get('id')=='P0-CMD-POLISHER-TLDR-URGE-20261024':
        t['progress_note']='R34聚焦4 CTR页+5低分；TLDR覆盖~90/247，缺口继续后续轮批量。'
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',closed)
