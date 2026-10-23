# -*- coding: utf-8 -*-
import io,json,os,sys
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
sys.path.insert(0,'scripts')
from llmevalkit_toolkit import LMEvalKit
picks=['openai_astra_review','best-ai-note-taking-tools-2026','chatgpt-vs-gemini-2026-comparison']
posts=json.load(io.open('data/posts.json',encoding='utf-8'))
by={p['slug']:p for p in posts}
ev=LMEvalKit()
for s in picks:
    c=by[s]['content']
    r=ev.evaluate_content(c,keyword=by[s].get('title','')[:40])
    has_tldr='## TL;DR' in c
    print('====',s)
    print(' TL;DR present:',has_tldr,'| score:',r['score'],'| hallucination:',r['hallucination_detected'],'| AIprob:',r['ai_content_probability'])
    print(' warnings:',r['warnings'][:3])
