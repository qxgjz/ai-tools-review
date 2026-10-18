import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
vc=next(x for x in posts if x['slug']=='best-ai-voice-changers-2026')
print('CTR-02 voice-changers:',len(vc['title']),'c /',len(vc['excerpt']),'c')
print(' T:',vc['title']); print(' E:',vc['excerpt'])

s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
notes={
 'CTR-20261018-01':f"R18 optimized midjourney-review-2026: clean title 55c 'Midjourney Review 2026: Best AI Image Generator, Tested' (removed truncated '| AIToolCrux'), excerpt 149c; article raised 60->100",
 'CTR-20261018-02':f"R18 verified best-ai-voice-changers-2026 already compliant: title 59c, excerpt 155c with CTA; 1 impression sample noise, no change needed",
}
n=0
for t in s['next_iteration_focus']:
    if t.get('id') in notes and t.get('status')!='completed':
        t['status']='completed'; t['completed_at']='2026-10-18'; t['close_note']=notes[t['id']]; n+=1
s.setdefault('completed_tasks',[]).insert(0,{
 'id':'POLISH-2026-10-18-R18','priority':'P1','status':'completed','assigned_to':['window5','打磨师'],
 'title':'R18: close CTR-01(midjourney title) + CTR-02(verified); fix midjourney/kling/leonardo to 100',
 'result':'midjourney-review 60->100 (clean title55c, BLUF, DALL-E link); kling 75->100 (BLUF, klingai.com); leonardo 75->100 (BLUF, leonardo.ai, excerpt132c)'
})
json.dump(s,open('iteration_center/state.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('closed',n)
