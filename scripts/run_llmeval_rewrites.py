# -*- coding: utf-8 -*-
"""跑 llmevalkit 幻觉检测 on 3 篇重写草稿"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llmevalkit_toolkit import LMEvalKit

e = LMEvalKit()
files = [
    ('content_drafts/2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md', 'midjourney vs flux'),
    ('content_drafts/2026-10-09-chatgpt-vs-claude-2026-comparison_REWRITE.md', 'chatgpt vs claude'),
    ('content_drafts/2026-10-09-claude-37-vs-gpt4o_REWRITE.md', 'claude 3.7 vs gpt-4o'),
]
for path, kw in files:
    try:
        text = open(path, encoding='utf-8').read()
        r = e.evaluate_content(text, keyword=kw)
        print('===', path)
        print('  score:', r.get('score'))
        print('  hallucination_detected:', r.get('hallucination_detected'))
        print('  ai_content_probability:', r.get('ai_content_probability'))
        warns = r.get('warnings', [])
        print('  warnings:', len(warns))
        for w in warns[:5]:
            print('   -', str(w)[:120])
        checks = r.get('checks', {})
        if isinstance(checks, dict):
            for k, v in list(checks.items())[:5]:
                print('   check', k, '=', str(v)[:100])
    except Exception as ex:
        print('===', path, 'ERROR:', str(ex)[:200])
