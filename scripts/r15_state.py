import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))

# Close 5 CTR tasks
close_map = {
 'CTR-20261017-01': 'title/meta already optimized (R10: 53c/137c); 26 impressions, CTR=0% needs accumulation',
 'CTR-20261017-02': 'optimized: title 58c "AI Tools Comparison 2026: Best Tools Compared Side by Side", excerpt 148c',
 'CTR-20261017-03': 'article-api old URL already 301 in public/_redirects -> /blog/creatium-coach-review-2025/',
 'CTR-20261017-04': 'article-api old URL already 301 in public/_redirects -> /blog/creatium-coach-review-2025/',
 'CTR-20261017-05': 'article-api old URL already 301 in public/_redirects -> /blog/elevenlabs-review-2026/',
}
for t in s.get('next_iteration_focus',[]):
    if t.get('id') in close_map and t.get('status')=='pending':
        t['status'] = 'completed'
        t['completed_at'] = '2026-10-17'
        t['close_note'] = close_map[t['id']]

s.setdefault('completed_tasks',[]).insert(0,{
    'id':'POLISH-2026-10-17-R15','priority':'P1',
    'title':'R15: close 5 CTR + fix 3 articles to 100',
    'status':'completed','assigned_to':['polisher'],
    'result':'5 CTR closed (02 optimized title58c/excerpt148c; 01 already optimized; 03/04/05 already 301); cursor-vs-copilot 60->100, dall-e-3 75->100, figma-ai 75->100'
})
json.dump(s, open('iteration_center/state.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

# verify closed
left = [t['id'] for t in s['next_iteration_focus'] if t.get('id','').startswith('CTR-20261017') and t.get('status')=='pending']
print("remaining pending CTR-20261017:", left)
print("state updated")
