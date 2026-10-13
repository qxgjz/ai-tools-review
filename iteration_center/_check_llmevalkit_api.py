# -*- coding: utf-8 -*-
"""检查 llmevalkit 幻觉检测器是否需要 API key"""
import inspect
from llmevalkit.hallucination import EntityHallucination, NumericHallucination, ContradictionDetector

for name, cls in [('EntityHallucination', EntityHallucination), ('NumericHallucination', NumericHallucination), ('ContradictionDetector', ContradictionDetector)]:
    print(f'=== {name} ===')
    try:
        sig = inspect.signature(cls.__init__)
        print('  __init__ 参数:', list(sig.parameters.keys()))
    except Exception as e:
        print('  __init__ 签名获取失败:', e)
    # 看看类里引用了哪些环境变量
    try:
        src = inspect.getsource(cls)
        import re
        envs = set(re.findall(r'os\.environ\.get\([\'"]([^\'"]+)', src))
        envs |= set(re.findall(r'getenv\([\'"]([^\'"]+)', src))
        print('  引用环境变量:', envs if envs else '无')
        # 检查是否有 detect 方法
        methods = [m for m in dir(cls) if not m.startswith('_')]
        print('  方法:', methods)
    except Exception as e:
        print('  源码获取失败:', e)
    print()
