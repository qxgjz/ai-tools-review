import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
notes={
 'CTR-20261017-01':'R17 re-verified on disk: title 53c, excerpt 137c compliant; 26 impressions, CTR 0% is sample noise, no further copy change warranted',
 'CTR-20261017-02':'R17 re-verified: title 58c, excerpt 148c compliant; only 1 impression, insufficient signal',
 'CTR-20261017-03':'R17 verified 301 live in public/_redirects -> /blog/creatium-coach-review-2025/ (orphan article-api URL, redirect is the fix, no title on orphan)',
 'CTR-20261017-04':'R17 verified 301 live -> /blog/creatium-coach-review-2025/',
 'CTR-20261017-05':'R17 verified 301 live -> /blog/elevenlabs-review-2026/',
 'CTR-20261017-06':'R17 re-verified: title 59c, excerpt 155c with CTA compliant; rank16.5 ctr2.94%, copy optimized R16',
}
n=0
for t in s['next_iteration_focus']:
    if t.get('id') in notes and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']='2026-10-17'; t['close_note']=notes[t['id']]; n+=1
s.setdefault('completed_tasks',[]).insert(0,{
 'id':'POLISH-2026-10-18-R17','priority':'P1','status':'completed','assigned_to':['window5','打磨师'],
 'title':'R17: re-close 6 CTR (disk-verified), fix heygen/cursor-react/jasper to 100',
 'result':'6 CTR closed with char/301 evidence; heygen 75->100 (BLUF+official link), cursor-react 60->100 (BLUF+2 sources+FAQ+excerpt151c), jasper 75->100 (BLUF+copy.ai+excerpt145c)'
})
json.dump(s,open('iteration_center/state.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',n)
left=[(t.get('priority'),t.get('id')) for t in s['next_iteration_focus'] if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in str(t.get('assigned_to','')).lower())]
print('remaining pending polisher:')
for x in left: print(' ',x)
