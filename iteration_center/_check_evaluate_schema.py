# -*- coding: utf-8 -*-
"""查看 evaluate 签名与 required_fields，确认正确输入格式"""
import inspect
from llmevalkit.hallucination import EntityHallucination, NumericHallucination, ContradictionDetector

for name, cls in [('EntityHallucination', EntityHallucination), ('NumericHallucination', NumericHallucination), ('ContradictionDetector', ContradictionDetector)]:
    print(f'=== {name} ===')
    d = cls(use_llm=False)
    try:
        sig = inspect.signature(d.evaluate)
        print('  evaluate 签名:', sig)
    except Exception as e:
        print('  evaluate 签名失败:', e)
    try:
        print('  required_fields:', d.required_fields)
    except Exception as e:
        print('  required_fields 获取失败:', e)
    # 看类源码
    try:
        src = inspect.getsource(cls.evaluate)
        print('  evaluate 源码(前800字符):')
        print(src[:800])
    except Exception as e:
        print('  源码失败:', e)
    print()
