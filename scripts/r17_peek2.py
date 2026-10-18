import json, os, re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['heygen-review-2026','jasper-review-2026']:
    p=next(x for x in posts if x['slug']==slug)
    c=p['content']
    ob=re.findall(r'href="(https?://[^"]+)"',c)
    print(f"=== {slug} fmt={'HTML' if '<' in c[:300] else 'MD'}")
    print(' outbound:',ob)
    print(' excerpt',len(p.get('excerpt','')),'c:',p.get('excerpt','')[:200])
    print()
