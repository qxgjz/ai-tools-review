import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
want=['adobe-firefly-review-2026','ai-tools-comparison-2026','creatium-coach-review-2025','elevenlabs-review-2026']
for slug in want:
    p=next((x for x in posts if x['slug']==slug),None)
    if not p: print('MISSING',slug); continue
    print(f"\n## {slug} T{len(p['title'])}c E{len(p.get('excerpt',''))}c")
    print('T:',p['title']); print('E:',p.get('excerpt',''))
