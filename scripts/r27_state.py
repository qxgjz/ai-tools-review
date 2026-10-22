# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='iteration_center/state.json'
s=json.load(io.open(fn,encoding='utf-8'))
now='2026-10-22T21:30:00'
cid='CMD-POLISHER-BATCH-20261022'
note=('R27补修9篇（指挥官原生check_draft完整文件口径，非b20裸content）：8篇zens-ink 88且Flesch>50达标——'
'best-free-ai-tools-for-students 88/69.7, how-to-get-chatgpt-free 88/64.8, jasper-vs-copy-ai 88/62.1, '
'best-ai-chatbots 88/55.1, best-ai-crm 88/51.5, best-ai-note-taking 88/57.5, best-ai-legal 88/51.6, '
'best-ai-seo 88/51.6；cursor-vs-copilot zens88但Flesch45.4留待正文可读性批改。'
'手段：顶部注入BLUF(quickAnswer)+官方外链+内部链+问句H2+结构化faq转markdown FAQ；仅用post自身字段与文章点名工具官网首页，无编造数据。满足本轮≥7篇要求。')
done=False
for t in s['next_iteration_focus']:
    if t.get('id')==cid and t.get('status')=='pending':
        t['status']='completed'; t['completed_at']=now; t['close_note']=note; done=True
        if not any(x.get('id')==cid for x in s.get('completed_tasks',[])):
            s.setdefault('completed_tasks',[]).insert(0,dict(t))
json.dump(s,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',done)
