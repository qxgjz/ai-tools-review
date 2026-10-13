# -*- coding: utf-8 -*-
"""验证 llmevalkit 安装与幻觉检测 API"""
import sys
sys.path.insert(0, r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\scripts')
import llmevalkit
print('llmevalkit 版本:', getattr(llmevalkit, '__version__', 'unknown'))

# 检查 hallucination 模块里有哪些类
try:
    from llmevalkit.hallucination import EntityHallucination, NumericHallucination, ContradictionDetector
    print('hallucination 模块导入 OK: EntityHallucination/NumericHallucination/ContradictionDetector 全部存在')
except Exception as e:
    print('hallucination 模块导入失败:', str(e)[:200])
    # 列出模块内容
    try:
        import llmevalkit.hallucination as h
        print('模块内容:', [x for x in dir(h) if not x.startswith('_')])
    except Exception as e2:
        print('hallucination 模块本身不存在:', str(e2)[:200])

# 列出一级模块
print('llmevalkit 顶层模块:', [x for x in dir(llmevalkit) if not x.startswith('_')][:40])
