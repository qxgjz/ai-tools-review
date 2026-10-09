# -*- coding: utf-8 -*-
"""查看 ContradictionDetector 报出的具体矛盾内容，人工核验真伪"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import llmevalkit.hallucination as hall

files = [
    ('content_drafts/2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md', 'midjourney'),
    ('content_drafts/2026-10-09-chatgpt-vs-claude-2026-comparison_REWRITE.md', 'chatgpt'),
    ('content_drafts/2026-10-09-claude-37-vs-gpt4o_REWRITE.md', 'claude'),
]
for path, tag in files:
    text = open(path, encoding='utf-8').read()
    full_ctx = text
    print('=====', tag, path)
    try:
        det = hall.ContradictionDetector(use_llm=False)
        r = det.evaluate(answer=text, context=full_ctx)
        print('score:', r.score)
        print('reason:', r.reason)
        details = getattr(r, 'details', None)
        print('details:', str(details)[:800])
    except Exception as ex:
        print('ERROR:', str(ex)[:300])
    print()
