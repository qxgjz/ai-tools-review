# -*- coding: utf-8 -*-
"""用 llmevalkit 6.0 真实幻觉检测器（EntityHallucination / NumericHallucination / ContradictionDetector）检测 3 篇草稿"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llmevalkit.hallucination import EntityHallucination, NumericHallucination, ContradictionDetector

files = [
    ('content_drafts/2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md', 'midjourney-v7-vs-flux-2026'),
    ('content_drafts/2026-10-09-chatgpt-vs-claude-2026-comparison_REWRITE.md', 'chatgpt-vs-claude-2026-comparison'),
    ('content_drafts/2026-10-09-claude-37-vs-gpt4o_REWRITE.md', 'claude-37-vs-gpt4o'),
]

detectors = []
for name, cls in [('entity', EntityHallucination), ('numeric', NumericHallucination), ('contradiction', ContradictionDetector)]:
    try:
        d = cls()
        detectors.append((name, d))
        print(f'  {name} detector init OK: {type(d).__name__}')
    except Exception as e:
        print(f'  {name} detector init FAIL: {str(e)[:120]}')

for path, slug in files:
    text = open(path, encoding='utf-8').read()
    print('===', slug)
    for name, d in detectors:
        try:
            if hasattr(d, 'detect'):
                r = d.detect(text)
            elif hasattr(d, 'check'):
                r = d.check(text)
            elif hasattr(d, 'evaluate'):
                r = d.evaluate(text)
            else:
                r = 'NO_ENTRY'
            print(f'  [{name}]', str(r)[:200])
        except Exception as e:
            print(f'  [{name}] ERROR: {str(e)[:150]}')
