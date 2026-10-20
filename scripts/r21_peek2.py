import json,os,re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['synthesia-review-2026','tabnine-review-2026','writesonic-review-2026']:
    p=next(x for x in posts if x['slug']==slug)
    ob=re.findall(r'href="(https?://[^"]+)"',p['content'])
    print(slug,'T',len(p['title']),'E',len(p.get('excerpt','')),ob)
