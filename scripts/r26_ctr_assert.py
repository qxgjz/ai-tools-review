# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
items=posts if isinstance(posts,list) else posts.get('posts',posts)
def chk(name,t,ex,kw):
    ok_t=50<=len(t)<=60; ok_e=120<=len(ex)<=155
    print(f'{name}: title {len(t)}c {"OK" if ok_t else "FAIL"} | desc {len(ex)}c {"OK" if ok_e else "FAIL"} | kw="{kw}" in title={kw.lower() in t.lower()}')
    print('   T:',repr(t)); print('   D:',repr(ex))
for p in items:
    s=p.get('slug','')
    if s=='adobe-firefly-review-2026': chk('adobe-firefly',p['title'],p.get('excerpt',''),'adobe firefly')
    if s=='ai-coding-tools-comparison-2026': chk('ai-coding-tools',p['title'],p.get('excerpt',''),'ai coding tools')
    if s=='openai_astra_review': chk('astra',p['title'],p.get('excerpt',''),'astra')
# ai-policy static
t='AI Usage Policy & Editorial Standards | AIToolCrux'
d='Learn how AIToolCrux uses AI tools responsibly in our content creation process. Our commitment to transparency, accuracy, and editorial integrity.'
chk('ai-policy',t,d,'ai usage policy')
