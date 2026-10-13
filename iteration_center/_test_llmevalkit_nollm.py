# -*- coding: utf-8 -*-
"""测试 use_llm=False 纯规则模式是否可用"""
from llmevalkit.hallucination import EntityHallucination, NumericHallucination, ContradictionDetector

text = open(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-09-midjourney-v7-vs-flux-2026_REWRITE.md', encoding='utf-8').read()
print('文章字数:', len(text))

for name, cls, kwargs in [
    ('entity(noLLM)', EntityHallucination, {'use_llm': False}),
    ('numeric(noLLM)', NumericHallucination, {'use_llm': False}),
    ('contradiction(noLLM)', ContradictionDetector, {'use_llm': False}),
]:
    try:
        d = cls(**kwargs)
        r = d.evaluate(text)
        print(f'[{name}] type={type(r).__name__} result={str(r)[:300]}')
    except Exception as e:
        print(f'[{name}] ERROR: {str(e)[:200]}')

# 再看看不传 use_llm 默认是什么
for name, cls in [('entity(default)', EntityHallucination), ('numeric(default)', NumericHallucination), ('contradiction(default)', ContradictionDetector)]:
    try:
        d = cls()
        r = d.evaluate(text)
        print(f'[{name}] result={str(r)[:200]}')
    except Exception as e:
        print(f'[{name}] ERROR: {str(e)[:200]}')
