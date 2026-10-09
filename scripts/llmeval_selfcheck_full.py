# -*- coding: utf-8 -*-
"""按用户补充规则执行 llmevalkit 自检：
口径A: evaluate_content 默认调用（context=文章前1/3）
口径B: evaluate_content 传入 context=全文（幻觉检测器的正确对照基准应为文章依据来源/全文，
       默认口径用文章自身前1/3作context，后半段实体必然"不在context"→ 误报幻觉）
输出两种口径分数，供对比。
"""
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
        full_ctx = text  # 口径B：全文作为context
        rA = e.evaluate_content(text, keyword=kw)                      # 口径A 默认
        rB = e.evaluate_content(text, keyword=kw, context=full_ctx)    # 口径B 全文context
        print('===', path)
        print('A(默认前1/3ctx) score:', rA.get('score'), '| halluc:', rA.get('hallucination_detected'),
              '| ai_prob:', round(rA.get('ai_content_probability', 0), 3))
        hallA = rA.get('checks', {}).get('hallucination', {})
        print('  A halluc细节:', {k: v for k, v in hallA.items() if isinstance(v, dict) and 'score' in v})
        print('B(全文ctx)     score:', rB.get('score'), '| halluc:', rB.get('hallucination_detected'),
              '| ai_prob:', round(rB.get('ai_content_probability', 0), 3))
        hallB = rB.get('checks', {}).get('hallucination', {})
        print('  B halluc细节:', {k: v for k, v in hallB.items() if isinstance(v, dict) and 'score' in v})
        warns = rB.get('warnings', [])
        print('  B warnings:', len(warns), [str(w)[:90] for w in warns[:4]])
    except Exception as ex:
        print('===', path, 'ERROR:', str(ex)[:200])
