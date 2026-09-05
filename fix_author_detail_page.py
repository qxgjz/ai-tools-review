#!/usr/bin/env python3
"""修改作者详情页面，只保留AIToolCrux Editorial Team集体作者"""

import os
import re

filepath = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\app\authors\[slug]\page.tsx"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 新的AUTHORS对象
new_authors = '''const AUTHORS: Record<string, any> = {
  "aitoolcrux-editorial-team": {
    name: "AIToolCrux Editorial Team",
    role: "Independent AI Tool Review Team",
    bio: "The AIToolCrux Editorial Team is a collective of independent AI tool reviewers with decades of combined experience in tech, development, design, and content strategy. Our team follows a transparent six-dimensional evaluation methodology, tests every tool for 14+ days, and does not accept payment for higher ratings. We believe good tool selection should be based on data, not marketing hype.",
    expertise: ["AI Chatbots", "Image Generation", "Code Assistants", "Productivity Tools", "Video Generation", "Enterprise AI"],
    avatar: "AT",
    color: "from-blue-500 to-indigo-600",
  },
};'''

# 使用正则表达式替换AUTHORS对象
# 匹配从 "const AUTHORS: Record<string, any> = {" 到对应的 "};"
pattern = r'const AUTHORS: Record<string, any> = \{.*?\n\};'
match = re.search(pattern, content, re.DOTALL)

if match:
    content = content[:match.start()] + new_authors + content[match.end():]
    print("✅ 已替换AUTHORS对象")
else:
    print("❌ 未找到AUTHORS对象")

# 写回文件
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 文件已更新")
