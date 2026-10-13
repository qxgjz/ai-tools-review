# -*- coding: utf-8 -*-
import io, os, sys, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
from llmevalkit_toolkit import LMEvalKit

files = [
    ('claude-vs-gemini-2026-comparison', 'claude vs gemini'),
    ('gemini-vs-chatgpt-2026', 'gemini vs chatgpt'),
    ('elevenlabs-v2-review-2026', 'elevenlabs v2 review'),
]
ev = LMEvalKit()
for slug, kw in files:
    p = os.path.join(base, 'content_drafts', '2026-10-11-%s_REWRITE.md' % slug)
    body = io.open(p, encoding='utf-8').read()
    r = ev.evaluate_content(body, keyword=kw, context=body)
    if isinstance(r, dict):
        print('===', slug, '| score:', r.get('score') or r.get('overall_score') or r.get('total'), '| flags:', r.get('flags') or r.get('issues'))
    else:
        print('===', slug, '| RAW:', str(r)[:500])
