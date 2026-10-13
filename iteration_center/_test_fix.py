# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")
from scripts.llmevalkit_toolkit import LMEvalKit

ev = LMEvalKit()

article = """ChatGPT is an AI chatbot developed by OpenAI. It was released in November 2022. The tool uses large language models to generate text.

In 2023, OpenAI launched GPT-4 which scored 40 out of 57 on the bar exam. The model has 1 trillion parameters and can process 25000 words at once. Users report 89 percent satisfaction rate. The API costs 0.002 per 1000 tokens.

FAQ:
Q: Is ChatGPT free?
A: Yes, there is a free tier.
Q: Can it write code?
A: Yes, it supports multiple programming languages.

![screenshot](chatgpt-ui.png)
"""

print("=== 测试1: 正常长文（自比模式，期望无误报）===")
r = ev.evaluate_content(article, keyword="ChatGPT")
print(f"  分数: {r['score']}")
print(f"  幻觉: {r['hallucination_detected']}")
print(f"  AI概率: {r['ai_content_probability']:.1%}")
print(f"  幻觉检测: {r['checks'].get('hallucination', {})}")
print(f"  警告: {r['warnings']}")
print()

print("=== 测试2: 有外部参考且数据不符（期望检出幻觉）===")
ref = "GPT-4 was released in 2023 and scored 298 out of 400 on the bar exam. It has 1.76 trillion parameters."
r2 = ev.evaluate_content(article, keyword="ChatGPT", context=ref)
print(f"  分数: {r2['score']}")
print(f"  幻觉: {r2['hallucination_detected']}")
print(f"  幻觉检测: {r2['checks'].get('hallucination', {})}")
print(f"  警告: {r2['warnings']}")
