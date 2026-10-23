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
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
norm={p['slug'].replace('_','-'):p['slug'] for p in posts}
for url,imp in sorted(agg.items(),key=lambda x:-x[1]):
    tail=url.rstrip('/').split('/')[-1]
    n=tail.replace('_','-')
    hit=norm.get(n)
    print(f"{imp:5} {'BLOG' if hit else '    '} {url}  -> {hit}")
