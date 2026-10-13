# -*- coding: utf-8 -*-
"""批量全量质检：遍历 content_drafts/*.md，用 LMEvalKit.evaluate_content 跑全部。"""
import os, sys, json, re
from pathlib import Path

ROOT = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(ROOT)
sys.path.insert(0, '.')

from scripts.llmevalkit_toolkit import LMEvalKit

# 草稿文件（排除 _ 开头的报告）
drafts = sorted([p for p in Path('content_drafts').glob('*.md') if not p.name.startswith('_')])

# 每篇主关键词（从slug推断）
KEYWORDS = {
    'midjourney-v7-vs-flux': 'Midjourney v7 vs Flux',
    'chatgpt-vs-claude': 'ChatGPT vs Claude',
    'claude-37-vs-gpt4o': 'Claude 3.7 Sonnet vs GPT-4o',
    'n8n-review': 'n8n workflow automation',
}

def guess_keyword(name: str) -> str:
    for k, v in KEYWORDS.items():
        if k in name.lower():
            return v
    return name

evaluator = LMEvalKit()
print('=== Toolkit status ===')
print(json.dumps(evaluator.status(), indent=2, ensure_ascii=False))

results = []
for p in drafts:
    text = p.read_text(encoding='utf-8')
    kw = guess_keyword(p.stem)
    print(f'\n=== {p.name} ({len(text)} chars, kw="{kw}") ===')
    try:
        r = evaluator.evaluate_content(text, keyword=kw)
    except Exception as e:
        r = {'score': -1, 'error': str(e), 'warnings': [f'eval error: {e}']}
    r['file'] = p.name
    r['keyword_used'] = kw
    results.append(r)
    print(f"  score={r.get('score')}  hallucination={r.get('hallucination_detected')}  ai_prob={r.get('ai_content_probability',0):.1%}  words={r.get('word_count')}")
    for w in r.get('warnings', []):
        print(f"    WARN: {w}")

# 按分数排序
results.sort(key=lambda x: x.get('score', 0))

# 判定
def grade(r):
    s = r.get('score', 0)
    if s < 70 or r.get('hallucination_detected'):
        return 'P0-重写'
    if r.get('ai_content_probability', 0) > 0.8:
        return 'P0-加真人体验'
    if s < 85:
        return 'P1-修改'
    return '通过-可发布'

print('\n' + '='*70)
print('SUMMARY (sorted by score low->high):')
print('='*70)
for r in results:
    print(f"  {r.get('score',0):>3} | {grade(r):14} | {r['file']}")

# 保存原始结果
out = Path('iteration_center') / '_batch_qc_raw.json'
out.write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(f'\nRaw JSON: {out}')

# 存到模块级供下一步写报告
import pickle
Path('iteration_center/_batch_qc_results.pkl').write_bytes(pickle.dumps(results))
