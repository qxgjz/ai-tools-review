# -*- coding: utf-8 -*-
import io,json,os,glob,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
agg={}
for fp in glob.glob('gsc-ga4-report/live_pull_*.json'):
    try: d=json.load(io.open(fp,encoding='utf-8'))
    except: continue
    for r in d.get('top_pages',[]):
        url=r['keys'][0]
        agg[url]=agg.get(url,0)+int(r.get('impressions',0))
rank=sorted(agg.items(),key=lambda x:-x[1])
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
slugset={p['slug'] for p in posts}
blog=[]
for url,imp in rank:
    m=re.search(r'/blog/([^/?#]+)',url)
    if m and m.group(1) in slugset: blog.append((m.group(1),imp))
print('total pages',len(rank),'blog matched',len(blog))
for s,i in blog[:30]: print(i,s)
