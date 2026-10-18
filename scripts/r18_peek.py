import json,os,re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['midjourney-review-2026','kling-review-2026','leonardo-ai-review-2026']:
    p=next(x for x in posts if x['slug']==slug)
    ob=re.findall(r'href="(https?://[^"]+)"',p['content'])
    print(f"== {slug}\n  TITLE: {p['title']}\n  OB: {ob}\n  EXCERPT: {p.get('excerpt','')}\n")
