# -*- coding: utf-8 -*-
import io, sys
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, base)
path = base + r'\content_drafts\2026-10-12-gemini_38_flash_review_REWRITE.md'
md = io.open(path, encoding='utf-8').read()
from llmevalkit.hallucination.core_detectors import ContradictionDetector
cd = ContradictionDetector(use_llm=False)
res = cd.evaluate(answer=md, context=md)
for c in res.details['contradictions']:
    print('---')
    print('CTX:', c['context_says'][:200])
    print('OUT:', c['output_says'][:200])
    print('TYPE:', c['type'])
