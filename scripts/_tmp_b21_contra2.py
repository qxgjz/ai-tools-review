# -*- coding: utf-8 -*-
import io, sys
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
sys.path.insert(0, base)
from llmevalkit.hallucination.core_detectors import ContradictionDetector
files = {
    'devin-ai-review': base + r'\content_drafts\2026-10-12-devin-ai-review_REWRITE.md',
    'perplexity-vs-chatgpt-2026': base + r'\content_drafts\2026-10-12-perplexity-vs-chatgpt-2026_REWRITE.md',
}
d = ContradictionDetector(use_llm=False)
for slug, path in files.items():
    md = io.open(path, encoding='utf-8').read()
    res = d.evaluate(answer=md, context=md)
    print('=====', slug, '| type:', type(res).__name__)
    print('model_dump keys:', list(res.model_dump().keys()) if hasattr(res, 'model_dump') else 'n/a')
    raw = res.model_dump()
    for k, v in raw.items():
        print('key:', k, '->', repr(v)[:400])
