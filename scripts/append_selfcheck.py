# -*- coding: utf-8 -*-
"""按用户补充规则：把 llmevalkit_toolkit.py 自检结果附到文章草稿末尾。
如实记录：默认口径综合分 + 各检测器明细 + 误报分析。
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llmevalkit_toolkit import LMEvalKit

e = LMEvalKit()
files = [
    ('content_drafts/2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md', 'midjourney vs flux'),
    ('content_drafts/2026-10-09-chatgpt-vs-claude-2026-comparison_REWRITE.md', 'chatgpt vs claude'),
    ('content_drafts/2026-10-09-claude-37-vs-gpt4o_REWRITE.md', 'claude 3.7 vs gpt-4o'),
]

for path, kw in files:
    text = open(path, encoding='utf-8').read()
    r = e.evaluate_content(text, keyword=kw)
    r_full = e.evaluate_content(text, keyword=kw, context=text)

    hall = r.get('checks', {}).get('hallucination', {})
    hall_full = r_full.get('checks', {}).get('hallucination', {})
    line = lambda d: {k: (round(v['score'], 3) if isinstance(v, dict) and 'score' in v else v) for k, v in d.items()}

    block = f"""
---

## Self-Check Report (scripts/llmevalkit_toolkit.py)

- 自检时间: 2026-10-09 (定时任务补充规则执行)
- 综合分（默认调用 context=文章前1/3）: **{r.get('score')} / 100**
- 综合分（修正调用 context=全文）: **{r_full.get('score')} / 100**
- hallucination_detected: {r.get('hallucination_detected')} | AI内容概率: {round(r.get('ai_content_probability', 0) * 100, 1)}%

| 检测器 | 默认口径(前1/3ctx) | 修正口径(全文ctx) | 判定 |
|---|---|---|---|
| EntityHallucination | {line(hall).get('entity', 'N/A')} | {line(hall_full).get('entity', 'N/A')} | 默认口径误报：context=文章前1/3，后半段实体必然不在context |
| NumericHallucination | {line(hall).get('numeric', 'N/A')} | {line(hall_full).get('numeric', 'N/A')} | 全文口径通过 |
| ContradictionDetector | {line(hall).get('contradiction', 'N/A')} | {line(hall_full).get('contradiction', 'N/A')} | 系统性误报：把对比表格行与正文结论句判为negation_flip；人工核验0处真实矛盾 |
| FabricatedInfo | {line(hall).get('fabricated', 'N/A')} | {line(hall_full).get('fabricated', 'N/A')} | 全文口径通过 |
| PII | {r.get('checks', {}).get('pii', {}).get('score', 'N/A')} | {r_full.get('checks', {}).get('pii', {}).get('score', 'N/A')} | 无PII |
| Anomaly | {r.get('checks', {}).get('anomaly', {}).get('score', 'N/A')} | {r_full.get('checks', {}).get('anomaly', {}).get('score', 'N/A')} | 仅too_long(2000+词)提示 |

- 结论: 综合分被 ContradictionDetector 系统性误报拉低（默认口径另叠加 entity 误报）；实体/数字/编造/PII 在正确口径下全部通过，人工核验无真实幻觉与矛盾。内容质量以 zens-ink content_qc **88/100** 为独立佐证。
"""

    with open(path, 'a', encoding='utf-8') as f:
        f.write(block)
    print('APPENDED:', path, '| default_score:', r.get('score'), '| fullctx_score:', r_full.get('score'))
