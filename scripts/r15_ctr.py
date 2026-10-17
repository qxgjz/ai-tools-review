import json, os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
s = json.load(open('iteration_center/state.json','r',encoding='utf-8'))
for t in s.get('next_iteration_focus',[]):
    if 'CTR-20261017' in t.get('id',''):
        print('===', t['id'], '===')
        print(' task:', t.get('task','')[:200])
        print(' rank:', t.get('rank'), 'impr:', t.get('impressions'), 'ctr:', t.get('ctr'))
        print()

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['adobe-firefly-review-2026','ai-tools-comparison-2026']:
    p = next((x for x in posts if x['slug']==slug), None)
    if p:
        print(f"=== {slug} ===")
        print(f"  title: {p.get('title','')} ({len(p.get('title',''))}c)")
        print(f"  excerpt: {p.get('excerpt','')} ({len(p.get('excerpt',''))}c)")
        print()
    else:
        print(f"=== {slug} NOT FOUND in posts.json ===")
