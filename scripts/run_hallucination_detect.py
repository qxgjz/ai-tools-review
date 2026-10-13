# -*- coding: utf-8 -*-
"""用 llmevalkit 6.0 完整幻觉检测：8个幻觉检测器 + PII隐私检测
修复记录（2026-10-09 指挥官）：
  1. pip install llmevalkit 6.0.2（之前从未安装，脚本静默降级）
  2. 正确 API = evaluate(answer=..., context=...)，旧脚本调 detect() 是错的
  3. 扩展：Entity/Numeric/Contradiction → 全部8个幻觉检测器 + PIIDetector
用法：从项目根目录运行  python scripts\run_hallucination_detect.py
"""
import sys
import os
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
]

# 全部检测器（纯规则模式，不依赖 LLM API key）
# (名称, 实例, 是否需要 question)
DETECTORS = [
    ('entity_实体幻觉', EntityHallucination(use_llm=False), False),
    ('numeric_数字幻觉', NumericHallucination(use_llm=False), False),
    ('contradiction_前后矛盾', ContradictionDetector(use_llm=False), False),
    ('fabricated_编造信息', FabricatedInfo(use_llm=False), False),
    ('negation_否定句幻觉', NegationHallucination(use_llm=False), False),
    ('causal_因果幻觉', CausalHallucination(use_llm=False), False),
    ('calibration_置信度校准', ConfidenceCalibration(use_llm=False), False),
    ('instruction_指令遵循', InstructionHallucination(use_llm=False), True),
    ('pii_隐私泄漏', PIIDetector(use_llm=False), False),
]

print('=== 检测器初始化 ===')
detectors = []
for name, d, need_q in DETECTORS:
    try:
        # 确认 evaluate 可用
        assert hasattr(d, 'evaluate'), f'{name} 无 evaluate'
        detectors.append((name, d, need_q))
        print(f'  OK: {name}')
    except Exception as e:
        print(f'  FAIL: {name} - {str(e)[:100]}')
print(f'共 {len(detectors)} 个检测器就绪\n')

for path, slug in files:
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        print(f'=== {slug}: 文件不存在 {path}')
        continue
    text = open(full, encoding='utf-8').read()
    # context：文章前 1/3 作为基准事实（对比文章内部一致性）
    context = text[:max(1500, len(text) // 3)]
    question = f'这篇评测文章 "{slug}" 的内容是否准确、有无虚构信息？'
    print(f'=== {slug} (字数{len(text)}, context{len(context)}) ===')
    for name, d, need_q in detectors:
        try:
            if need_q:
                r = d.evaluate(answer=text, context=context, question=question)
            else:
                r = d.evaluate(answer=text, context=context)
            # 分数含义：1.0=完全一致/无幻觉，越低风险越高
            details = str(r.details)[:160] if getattr(r, 'details', None) else ''
            print(f'  [{name}] score={r.score} | {r.reason} | {details}')
        except Exception as e:
            print(f'  [{name}] ERROR: {str(e)[:140]}')
    print()
