# -*- coding: utf-8 -*-
"""扩展幻觉检测：加n8n草稿 + 打印contradiction完整details"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llmevalkit.hallucination import EntityHallucination, NumericHallucination, ContradictionDetector

BASE = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

files = [
    ('content_drafts/2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md', 'midjourney-v7-vs-flux-2026'),
    ('content_drafts/2026-10-09-chatgpt-vs-claude-2026-comparison_REWRITE.md', 'chatgpt-vs-claude-2026-comparison'),
    ('content_drafts/2026-10-09-claude-37-vs-gpt4o_REWRITE.md', 'claude-37-vs-gpt4o'),
    ('content_drafts/2026-10-09-n8n-review-2026_DRAFT.md', 'n8n-review-2026'),
]

detectors = []
for name, cls, kw in [
    ('entity', EntityHallucination, {'use_llm': False}),
    ('numeric', NumericHallucination, {'use_llm': False}),
    ('contradiction', ContradictionDetector, {'use_llm': False}),
]:
    d = cls(**kw)
    detectors.append((name, d))

all_results = {}
for path, slug in files:
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        print(f'=== {slug}: MISSING {path}')
        continue
    text = open(full, encoding='utf-8').read()
    # Use whole article as context (not just 1500 chars) for fairer entity check
    context = text
    print(f'\n{"="*70}\n=== {slug} (chars={len(text)}) ===')
    all_results[slug] = {'path': path, 'scores': {}, 'details': {}}
    for name, d in detectors:
        try:
            r = d.evaluate(answer=text, context=context)
            print(f'  [{name}] score={r.score:.3f}  reason={r.reason}')
            all_results[slug]['scores'][name] = r.score
            all_results[slug]['details'][name] = r.details
        except Exception as e:
            print(f'  [{name}] ERROR: {e}')
            all_results[slug]['scores'][name] = -1

# Print contradictions in detail
print('\n' + '='*70)
print('CONTRADICTION DETAILS (full):')
print('='*70)
for slug, res in all_results.items():
    c = res['details'].get('contradiction', {})
    if isinstance(c, dict) and c.get('contradictions'):
        print(f'\n--- {slug} ---')
        for i, ct in enumerate(c['contradictions']):
            print(f'  #{i+1} type={ct.get("type","?")}')
            print(f'     context_says: {ct.get("context_says","")[:200]}')
            print(f'     output_says : {ct.get("output_says","")[:200]}')

# Print numeric mismatches (first 10)
print('\n' + '='*70)
print('NUMERIC MISMATCHES (first 10 per article):')
print('='*70)
for slug, res in all_results.items():
    n = res['details'].get('numeric', {})
    if isinstance(n, dict) and n.get('checks'):
        bad = [c for c in n['checks'] if not c.get('match', True)]
        print(f'\n--- {slug}: {len(bad)} bad numbers ---')
        for c in bad[:10]:
            print(f"  output={c.get('output')!r}  context={c.get('context')!r}  diff={c.get('diff')}")

# Save full JSON
out = os.path.join(BASE, 'iteration_center', '_hallucination_raw.json')
json.dump(all_results, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2, default=str)
print(f'\nRaw details saved: {out}')
