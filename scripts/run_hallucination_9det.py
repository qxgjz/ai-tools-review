# -*- coding: utf-8 -*-
"""完整版9项检测+dump完整details到JSON（含n8n）"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llmevalkit.hallucination import (
    CausalHallucination, ConfidenceCalibration, ContradictionDetector,
    EntityHallucination, FabricatedInfo, InstructionHallucination,
    NegationHallucination, NumericHallucination,
)
from llmevalkit.compliance import PIIDetector

BASE = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

files = [
    ('content_drafts/2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md', 'midjourney-v7-vs-flux-2026'),
    ('content_drafts/2026-10-09-chatgpt-vs-claude-2026-comparison_REWRITE.md', 'chatgpt-vs-claude-2026-comparison'),
    ('content_drafts/2026-10-09-claude-37-vs-gpt4o_REWRITE.md', 'claude-37-vs-gpt4o'),
    ('content_drafts/2026-10-09-n8n-review-2026_DRAFT.md', 'n8n-review-2026'),
]

DETECTORS = [
    ('entity', EntityHallucination(use_llm=False), False),
    ('numeric', NumericHallucination(use_llm=False), False),
    ('contradiction', ContradictionDetector(use_llm=False), False),
    ('fabricated', FabricatedInfo(use_llm=False), False),
    ('negation', NegationHallucination(use_llm=False), False),
    ('causal', CausalHallucination(use_llm=False), False),
    ('calibration', ConfidenceCalibration(use_llm=False), False),
    ('instruction', InstructionHallucination(use_llm=False), True),
    ('pii', PIIDetector(use_llm=False), False),
]

all_res = {}
for path, slug in files:
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        continue
    text = open(full, encoding='utf-8').read()
    # Use FULL article as context (not 1/3) for fairer internal-consistency check
    context = text
    question = f'This review article "{slug}" — is it accurate, any fabricated info?'
    all_res[slug] = {'path': path, 'scores': {}, 'details': {}}
    print(f'\n=== {slug} (chars={len(text)}) ===')
    for name, d, need_q in DETECTORS:
        try:
            if need_q:
                r = d.evaluate(answer=text, context=context, question=question)
            else:
                r = d.evaluate(answer=text, context=context)
            all_res[slug]['scores'][name] = r.score
            all_res[slug]['details'][name] = r.details
            print(f'  [{name}] score={r.score}')
        except Exception as e:
            all_res[slug]['scores'][name] = -1
            print(f'  [{name}] ERROR: {e}')

# Print P0-relevant details
print('\n' + '='*70)
print('FABRICATED statements (all flagged):')
print('='*70)
for slug, res in all_res.items():
    f = res['details'].get('fabricated', {})
    if isinstance(f, dict) and f.get('statements'):
        bad = [s for s in f['statements'] if not s.get('supported', True)]
        print(f'\n--- {slug}: {len(bad)} unsupported statements ---')
        for s in bad:
            print(f"  [{s.get('coverage',0):.2f}] {s.get('text','')[:200]}")

print('\n' + '='*70)
print('CAUSAL claims (all flagged unsupported):')
print('='*70)
for slug, res in all_res.items():
    c = res['details'].get('causal', {})
    if isinstance(c, dict) and c.get('checks'):
        bad = [x for x in c['checks'] if not x.get('supported', True)]
        print(f'\n--- {slug}: {len(bad)} unsupported causal claims ---')
        for x in bad:
            print(f"  [{x.get('coverage',0):.2f}] {x.get('claim','')[:250]}")

print('\n' + '='*70)
print('CONTRADICTIONS:')
print('='*70)
for slug, res in all_res.items():
    ct = res['details'].get('contradiction', {})
    if isinstance(ct, dict) and ct.get('contradictions'):
        print(f'\n--- {slug}: {len(ct["contradictions"])} ---')
        for c in ct['contradictions']:
            print(f"  type={c.get('type')}")
            print(f"    ctx: {c.get('context_says','')[:150]}")
            print(f"    out: {c.get('output_says','')[:150]}")

# Save
out = os.path.join(BASE, 'iteration_center', '_hallucination_9det.json')
json.dump(all_res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2, default=str)
print(f'\nSaved: {out}')
