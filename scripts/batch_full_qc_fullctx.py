# -*- coding: utf-8 -*-
"""用全文 context 重跑，拿真实分数（避免前1/3截取误报）"""
import os, sys, json, pickle
from pathlib import Path

ROOT = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
os.chdir(ROOT); sys.path.insert(0, '.')
from scripts.llmevalkit_toolkit import LMEvalKit

evaluator = LMEvalKit()
drafts = sorted([p for p in Path('content_drafts').glob('*.md') if not p.name.startswith('_')])

results = []
for p in drafts:
    text = p.read_text(encoding='utf-8')
    # 关键：传 context=全文，避免 toolkit 默认前1/3截取
    r = evaluator.evaluate_content(text, keyword=p.stem, context=text)
    r['file'] = p.name
    results.append(r)
    h = r.get('checks',{}).get('hallucination',{})
    print(f"{p.name}: score={r['score']} hallu={r['hallucination_detected']} ai_prob={r['ai_content_probability']:.1%} words={r['word_count']}")
    for k,v in h.items():
        if isinstance(v,dict):
            print(f"   {k}: {v.get('score')}")

results.sort(key=lambda x: x['score'])
Path('iteration_center/_batch_qc_fullctx.pkl').write_bytes(pickle.dumps(results))
print('\nSorted:')
for r in results:
    print(f"  {r['score']:3} | {r['file']}")
