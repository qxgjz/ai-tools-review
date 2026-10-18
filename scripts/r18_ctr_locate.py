import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
for kw in ['midjourney','voice']:
    print(f'===== keyword: {kw} =====')
    for p in posts:
        blob=(p['slug']+' '+p.get('title','')+' '+p.get('excerpt','')+' '+' '.join(p.get('tags',[]))).lower()
        if kw in blob:
            t=p.get('title','');e=p.get('excerpt','')
            print(f"[{p['slug']}] T{len(t)}c E{len(e)}c")
            print('   T:',t)
            print('   E:',e)
