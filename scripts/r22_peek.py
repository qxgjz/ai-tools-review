import json,os,re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['synthesia-review-2026','tabnine-review-2026','writesonic-review-2026']:
    p=next(x for x in posts if x['slug']==slug)
    c=p['content']
    print('====',slug,'wc=',p.get('wordCount'),'len=',len(c),'title=',p['title'])
    print('BLUF?', 'Bottom line' in c or 'TL;DR' in c, '| HTMLtags=', len(re.findall(r'<h2|<p |<li',c)), '| links=',re.findall(r'href="(https?://[^"]+)"',c)[:3])
    print('HEAD300:',c[:300].replace('\n',' '))
    print()
