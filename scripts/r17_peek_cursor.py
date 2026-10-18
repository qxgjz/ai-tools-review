import json, os, re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
p=next(x for x in posts if x['slug']=='how-to-use-cursor-for-react-development')
c=p['content']
print('LEN',len(c))
print('HEAD:',c[:600])
print('\n--- H2 ---')
for h in re.findall(r'^#{2,3}\s+(.+)$',c,flags=re.M): print(' ',h[:80])
print('\nOUTBOUND:',re.findall(r'\]\((https?://[^)]+)\)',c))
print('META keys:',[k for k in p.keys()])
print('description field:',p.get('description','')[:120])
