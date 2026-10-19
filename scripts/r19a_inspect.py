import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s=json.load(open('iteration_center/state.json','r',encoding='utf-8'))
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
ids=['CTR-20261018-03','CTR-20261018-04','CTR-20261018-05','CTR-20261018-06','CTR-20261019-01','CTR-20261019-02','CTR-20261019-03','CTR-20261019-04','P1-ARTICLE-REFRESH-20261019']
for t in s['next_iteration_focus']:
    if t.get('id') in ids:
        print('###',t.get('id'),'|',t.get('priority'),'|',t.get('status'))
        print('  task:',t.get('task'))
        print('  url:',t.get('url') or t.get('page') or t.get('path'))
for slug in ['best-ai-voice-changers-2026','adobe-firefly-review-2026','ai-tools-comparison-2026']:
    p=next((x for x in posts if x['slug']==slug),None)
    if p:
        print(f"\n== {slug} T{len(p['title'])}c E{len(p.get('excerpt',''))}c")
        print(' T:',p['title']); print(' E:',p.get('excerpt',''))
