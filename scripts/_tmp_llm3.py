# -*- coding: utf-8 -*-
import io, sys, os, json
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts'
files = [('2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md', 'best ai tools for beginners 2026'),
         ('2026-10-10-agenta-ai-review-2026_DRAFT.md', 'agenta ai review open source agent builder'),
         ('2026-10-10-cursor-vs-windsurf-2026_REWRITE.md', 'cursor vs windsurf ai code editor')]
from scripts.llmevalkit_toolkit import LMEvalKit
ev = LMEvalKit()
for fn, kw in files:
    body = io.open(base + '\\' + fn, encoding='utf-8').read()
    res = ev.evaluate_content(body, keyword=kw, context=body)
    print('===', fn)
    print('  score:', res.get('score'), '| hallucination_detected:', res.get('hallucination_detected'))
    det = res.get('hallucination_details') or res.get('details') or {}
    if isinstance(det, dict):
        for k, v in list(det.items())[:8]:
            print('   ', k, ':', str(v)[:120])
