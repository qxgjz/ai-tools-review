import json,os,re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in ['microsoft-365-copilot-review-2026','notion-ai-review-2026','otter-ai-review-2026','adobe-firefly-review-2026','best-ai-voice-changers-2026']:
    p=next(x for x in posts if x['slug']==slug)
    ob=re.findall(r'href="(https?://[^"]+)"',p['content'])
    print(f"== {slug} T{len(p['title'])}c E{len(p.get('excerpt',''))}c")
    print(' T:',p['title']); print(' E:',p.get('excerpt','')); print(' OB:',ob,'\n')
