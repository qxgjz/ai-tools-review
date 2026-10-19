import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
notes={
 'CTR-20261018-03':'R19 real rewrite (68 impr, rank16.5): title 60c "Best AI Voice Changers 2026: Free & Real-Time Tools Compared", excerpt 149c with free-options + CTA',
 'CTR-20261018-04':'R19 real rewrite (26 impr, rank5.2): title 58c "Adobe Firefly Review 2026: Free AI Image Generator, Tested", excerpt 154c, added official firefly.adobe.com link; page 100',
 'CTR-20261018-05':'R19 verified ai-tools-comparison-2026 compliant title58c/excerpt148c; 1-impression noise',
 'CTR-20261018-06':'R19 verified 301 live in public/_redirects -> /blog/creatium-coach-review-2025/ (20 impr on orphan URL, redirect is the fix)',
 'CTR-20261019-01':'R19 dup of R18-01: midjourney-review already optimized title55c in R18; 1-impression noise, no further change',
 'CTR-20261019-02':'R19 dup of R18-02: best-ai-voice-changers verified; 1-impression noise',
 'CTR-20261019-03':'R19 verified 301 live -> /blog/creatium-coach-review-2025/',
 'CTR-20261019-04':'R19 verified 301 live -> /blog/elevenlabs-review-2026/',
}
n=0
for t in s['next_iteration_focus']:
    if t.get('id') in notes and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']='2026-10-19'; t['close_note']=notes[t['id']]; n+=1
s.setdefault('completed_tasks',[]).insert(0,{
 'id':'POLISH-2026-10-19-R19','priority':'P1','status':'completed','assigned_to':['window5','打磨师'],
 'title':'R19: real CTR rewrite voice-changers/firefly; verify 301s+dups; fix copilot/notion/otter to 100',
 'result':'CTR-03 title60c/excerpt149c; CTR-04 title58c/excerpt154c+official link; 3x301 verified; copilot/notion/otter 100 (BLUF/outbound/clean titles)'
})
json.dump(s,open('iteration_center/state.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',n)
left=[(t.get('priority'),t.get('id')) for t in s['next_iteration_focus'] if t.get('status')=='pending' and ('打磨' in str(t.get('assigned_to','')) or 'window5' in str(t.get('assigned_to','')).lower())]
for x in left: print(' LEFT',x)
