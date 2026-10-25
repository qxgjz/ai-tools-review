# -*- coding: utf-8 -*-
import io,json,os,sys
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
sys.path.insert(0,'scripts')
from llmevalkit_toolkit import LMEvalKit
posts=json.load(io.open('data/posts.json',encoding='utf-8')); by={p['slug']:p for p in posts}
s='veed-vs-capcut-2026'
p=by[s]
r=LMEvalKit().evaluate_content(p['content'], keyword=p.get('title','').split()[0], context=None)
print('SCORE',r.get('score') if isinstance(r,dict) else r)
print(r if isinstance(r,dict) else '')
