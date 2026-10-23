# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'; s=json.load(io.open(fn,encoding='utf-8'))
now='2026-10-23T22:10:00'
cid='P0-GEO-TLDR-TABLE-20261023'
note=('R29复核：state被他窗口last-write还原为pending，但posts.json中20篇r28-tldr块与6篇r28-low块完整无损；'
'R28成果已推送(17c0c2e)，重新标记completed。本轮另修5篇低分双达标(zens88+Flesch>50)：'
'cursor-alternatives 56.1 / free-ai-tools-for-students 53.6 / perplexity-alternatives 58.2 / meeting-notes 54.1 / n8n-vs-zapier 59.1；'
'mental-health zens88但Flesch48.6留正文。无新增P0-CTR待办。')
for t in s['next_iteration_focus']:
    if t.get('id')==cid:
        t['status']='completed'; t['completed_at']=now; t['close_note']=note
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('ok')
