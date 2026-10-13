# -*- coding: utf-8 -*-
import io
from llmevalkit.modules.hallucination import ContradictionDetector
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-11-midjourney-v7-review-2026_REWRITE.md'
md = io.open(p, encoding='utf-8').read()
d = ContradictionDetector(use_llm=False)
r = d.evaluate(answer=md, context=md)
print('score:', r.score)
print('reason:', (r.reason or '')[:2000])
