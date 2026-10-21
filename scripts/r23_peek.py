# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
s=json.load(io.open('iteration_center/state.json',encoding='utf-8'))
want={'P0-CTR-VERIFY-20261021','CTR-OPT-ADOBE-FIREFLY-20261021','CTR-OPT-AI-CODING-COMP-20261021','CTR-OPT-AI-POLICY-20261021','CTR-OPT-VOICE-CHANGERS-20261021','P0-FAKE-FIX-3ARTICLES-20261020'}
for t in s['next_iteration_focus']:
    if t.get('id') in want:
        print(json.dumps(t,ensure_ascii=False,indent=2));print('-'*40)
# check R22 fix survival
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
for slug in ['synthesia-review-2026','tabnine-review-2026','writesonic-review-2026']:
    p=next((x for x in posts if x['slug']==slug),None)
    if not p: print(slug,'MISSING');continue
    ob=re.findall(r'\]\((https?://[^)]+)\)',p['content'][:30000])
    faq='Frequently Asked' in p['content'][:30000]
    print(slug,'head-links=',ob,'faq=',faq,'title=',p['title'],'E=',len(p.get('excerpt','')))
