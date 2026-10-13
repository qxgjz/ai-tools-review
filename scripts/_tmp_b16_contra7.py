# -*- coding: utf-8 -*-
import io, os, sys, json
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, os.path.join(base, 'scripts'))
from llmevalkit_toolkit import LMEvalKit
ev = LMEvalKit()
hall = ev._modules['hallucination']
for slug in ['gemini-vs-chatgpt-2026', 'elevenlabs-v2-review-2026']:
    p = os.path.join(base, 'content_drafts', '2026-10-11-%s_REWRITE.md' % slug)
    body = io.open(p, encoding='utf-8').read()
    d = hall.ContradictionDetector(use_llm=False)
    r = d.evaluate(answer=body, context=body)
    det = getattr(r, 'details', None)
    print('===', slug, '| score:', r.score)
    if det:
        for c in det.get('contradictions', []):
            print('  TYPE:', c.get('type'))
            print('  CTX :', c.get('context_says'))
            print('  OUT :', c.get('output_says'))
            if 'words' in c:
                print('  WORDS:', c.get('words'))
            print()
    else:
        print('  reason:', r.reason)
