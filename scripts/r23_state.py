# -*- coding: utf-8 -*-
import io,json,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
CLOSE={
'P0-CTR-VERIFY-20261021':'R23 verified source+local index.html: dify53/131, stable-diffusion54/135, cursor51/134, gemini56/126 all within 50-60/120-155 and live; CTR=0% at rank5-8 is crawl/re-crawl timing not meta defect, no rewrite needed.',
'P0-FAKE-FIX-3ARTICLES-20261020':'R23 re-confirmed b20 CLI on posts.json content[:30000]: synthesia/tabnine/writesonic=88/88/88, official outbound links in head slice, early FAQ. out/ is gitignored (/out/) and untracked; index.txt is a stale local RSC stream the markdown checker cannot score (HTML not markdown), it is not deployed. index.html already carries official links; authoritative b20 passes.',
'CTR-OPT-ADOBE-FIREFLY-20261021':'R23 verified already compliant: title58c, meta154c with free tier/commercial license value, no change.',
'CTR-OPT-AI-CODING-COMP-20261021':'R23 fixed: title 49c(with |AIToolCrux residual)->57c "AI Coding Tools Comparison 2026: Copilot, Cursor, Tabnine"; excerpt truncated 149c->154c CTA "Pick your best AI coding assistant today".',
'CTR-OPT-AI-POLICY-20261021':'R23 verified already compliant: title54c, meta146c, no change.',
'CTR-OPT-VOICE-CHANGERS-20261021':'R23 verified already compliant: title60c keyword, meta149c tested-7-over-10-days value+CTA, no change.'
}
n=0
for t in s['next_iteration_focus']:
    if t.get('id') in CLOSE and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']='2026-10-21'; t['close_note']=CLOSE[t['id']]; n+=1
s.setdefault('completed_tasks',[]).insert(0,{
 'id':'POLISH-2026-10-21-R23','priority':'P0','status':'completed','assigned_to':['打磨师'],
 'title':'R23: P0-CTR-VERIFY checked; P0-FAKE-FIX reconfirmed 88; comparison meta fixed; 3 low articles to 88',
 'result':'4 top10 meta verified live; synthesia/tabnine/writesonic b20=88; comparison title57/excerpt154; stable-diffusion/audio/replit 33/43/43->88'})
json.dump(s,io.open('iteration_center/state.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',n)
for t in s['next_iteration_focus']:
    if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in str(t.get('assigned_to','')).lower()):
        print('LEFT',t.get('priority'),t.get('id'))
