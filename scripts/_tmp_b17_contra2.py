# -*- coding: utf-8 -*-
import io, sys
sys.path.insert(0, r'C:\Users\通明街\AppData\Local\DoubaoWork\User Data\sandbox_runtime\bases\d0ace100fdff5b2d247847aca1e3d83b\python\Lib\site-packages')
from llmevalkit.hallucination.core_detectors import ContradictionDetector
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-midjourney-v7-review-2026_REWRITE.md'
md = io.open(p, encoding='utf-8').read()
d = ContradictionDetector(use_llm=False)
r = d.evaluate(answer=md, context=md)
print('score:', r.score)
for c in r.details.get('contradictions', []):
    print('--- type:', c.get('type'))
    print('  ctx :', c.get('context_says'))
    print('  out :', c.get('output_says'))
