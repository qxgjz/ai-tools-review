# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
CLOSE={
'P0-FAKE-FIX-3ARTICLES-20261020':
 'R22 reproduced QA CLI on raw content[:30000]: synthesia/tabnine/writesonic 78/78/68 -> 88/88/88 by moving official outbound link into first 30k slice and adding early FAQ to writesonic; remaining Title/Desc/Date fails are frontmatter-only (raw content slice has none; built HTML supplies them), score>=70 met.',
'P1-CTR-REMAIN-20261020':
 'R22 verified: /about(57c/150c) and /ai-policy(52c/149c) already compliant; cleaned ai-tools-for-beginners-2026 title 58c->55c(removed |AIToolCrux tail) and excerpt 156c-truncated->150c CTA. No action needed on already-compliant pages.'
}
n=0
for t in s['next_iteration_focus']:
    if t.get('id') in CLOSE and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']='2026-10-20'; t['close_note']=CLOSE[t['id']]; n+=1
s.setdefault('completed_tasks',[]).insert(0,{
 'id':'POLISH-2026-10-20-R22','priority':'P0','status':'completed','assigned_to':['打磨师'],
 'title':'R22: P0 fake-fix 3 articles to 88; CTR-REMAIN verified+beginners cleaned',
 'result':'synthesia/tabnine/writesonic 88 via early outbound+FAQ; beginners title55/excerpt150; about/ai-policy compliant'})
json.dump(s,io.open('iteration_center/state.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',n)
for t in s['next_iteration_focus']:
    if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in str(t.get('assigned_to','')).lower()):
        print('LEFT',t.get('priority'),t.get('id'))
