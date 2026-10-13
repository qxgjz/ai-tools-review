# -*- coding: utf-8 -*-
"""实测 llmevalkit 6.0.2 全部模块可用性与当前覆盖情况"""
import importlib, inspect

# 1. 尝试导入全部 13 个文档声明的模块
modules = [
    "hallucination", "ai_content_detection", "compliance",
    "document_parsing", "governance", "security",
    "observability", "ground_truth", "conversation",
    "red_team", "anomaly_detection", "quality", "toxicity"
]
print('=== 模块可用性 ===')
ok, fail = [], []
for m in modules:
    try:
        mod = importlib.import_module(f'llmevalkit.{m}')
        ok.append(m)
        # 列出每个模块的关键类
        classes = [x for x in dir(mod) if not x.startswith('_') and isinstance(getattr(mod, x), type)]
        print(f'  ✅ {m}: {len(classes)}个类 {classes[:8]}')
    except Exception as e:
        fail.append(m)
        print(f'  ❌ {m}: {str(e)[:80]}')

print(f'\n可用: {len(ok)}个 | 失败: {len(fail)}个 {fail}')

# 2. 看当前脚本实际检测了什么
print('\n=== 当前 run_hallucination_detect.py 实际覆盖 ===')
print('仅覆盖 hallucination 模块 3 个检测器: entity/numeric/contradiction')
print('未覆盖: ai_content_detection(是否AI生成), quality(内容质量78指标),')
print('        compliance(合规), governance(治理), security(安全), conversation(对话)等')
