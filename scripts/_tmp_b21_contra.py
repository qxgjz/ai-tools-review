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
    pairs = res.get('contradictions', [])
    if isinstance(pairs, dict):
        pairs = pairs.get('pairs', []) or []
    print('=====', slug, '| contradictions:', len(pairs))
    for i, pr in enumerate(pairs[:12]):
        if isinstance(pr, dict):
            print('---', i, '| sim:', pr.get('similarity'), '| a:', (pr.get('sentence_a') or pr.get('claim') or '')[:200])
            print('    b:', (pr.get('sentence_b') or pr.get('evidence') or '')[:200])
        else:
            print('---', i, repr(pr)[:300])
