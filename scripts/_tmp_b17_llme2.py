# -*- coding: utf-8 -*-
import io, sys
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from scripts.llmevalkit_toolkit import LMEvalKit
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
jobs = [
    ('cursor_ai_review', 'cursor ai review'),
    ('midjourney-v7-review-2026', 'midjourney v7 review'),
    ('suno-alternatives', 'suno alternatives'),
]
ev = LMEvalKit()
for slug, kw in jobs:
    md = io.open(base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md', encoding='utf-8').read()
    r = ev.evaluate_content(md, keyword=kw, context=md)
    hall = r.get('checks', {}).get('hallucination', {})
    print('===', slug, '| score:', r.get('overall_score') or r.get('score'))
    print('  hallucination:', {k: (v.get('score') if isinstance(v, dict) else v) for k, v in hall.items() if isinstance(v, dict)})
    print('  detected:', r.get('hallucination_detected'))
