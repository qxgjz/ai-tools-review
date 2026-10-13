# -*- coding: utf-8 -*-
import io, os, sys
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
from llmevalkit_toolkit import LMEvalKit
ev = LMEvalKit()
hall = ev._modules['hallucination']
for slug, kw in [('gemini-vs-chatgpt-2026','gemini vs chatgpt'), ('elevenlabs-v2-review-2026','elevenlabs v2 review')]:
    p = os.path.join(base, 'content_drafts', '2026-10-11-%s_REWRITE.md' % slug)
    body = io.open(p, encoding='utf-8').read()
    d = hall.ContradictionDetector(use_llm=False)
    r = d.evaluate(answer=body, context=body)
    print('===', slug, '| score:', r.score)
    print('reason:', r.reason[:3000])
    print()
