# -*- coding: utf-8 -*-
"""batch31 llmevalkit: evaluate 3 drafts WITHOUT context (per batch29/30 SOP)"""
import io, os, sys

sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from scripts.llmevalkit_toolkit import LMEvalKit

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
jobs = [
    ('content_drafts/2026-10-17-ai-tools-hallucinate-least-2026_NEW.md', 'ai hallucination'),
    ('content_drafts/2026-10-17-ai-writing-tools-match-your-voice-2026_NEW.md', 'ai writing voice'),
    ('content_drafts/2026-10-17-ai-tools-generous-rate-limits-2026_NEW.md', 'ai rate limits'),
]
lme = LMEvalKit()
for fn, kw in jobs:
    p = os.path.join(base, fn)
    content = io.open(p, encoding='utf-8').read()
    try:
        r = lme.evaluate_content(content=content, keyword=kw)
        score = r.get('score') if isinstance(r, dict) else getattr(r, 'score', None)
        hal = r.get('hallucination_detected') if isinstance(r, dict) else getattr(r, 'hallucination_detected', None)
        print(fn.split('/')[-1], '| score:', score, '| hallucination_detected:', hal)
    except Exception as e:
        print(fn.split('/')[-1], '| ERR:', type(e).__name__, str(e)[:200])
