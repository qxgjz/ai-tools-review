# -*- coding: utf-8 -*-
import io,json,re,os
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
for slug in ['synthesia-review-2026','tabnine-review-2026','writesonic-review-2026']:
    p=next(x for x in posts if x['slug']==slug); c=p['content'][:30000]
    ob=re.findall(r'\]\((https?://[^)]+)\)',c)
    print('===',slug,'in[:30000] outbound=',ob)
    print('FAQ marker in[:30000]:', 'Frequently Asked' in c or 'FAQPage' in c or bool(re.search(r'^faq:',c,re.M)))
