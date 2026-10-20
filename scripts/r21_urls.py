import json,os
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
g=json.load(open('gsc-ga4-report/live_pull_20261013_2006.json','r',encoding='utf-8'))
for p in g.get('top_pages',[]):
    k=str(p.get('keys'))
    if 'article-api' in k or 'creatium' in k or 'elevenlabs' in k or 'firefly' in k:
        print(p.get('position'),p.get('impressions'),p.get('clicks'),p.get('ctr'),'|',p.get('keys'))
