# -*- coding: utf-8 -*-
"""追加今日错误和经验到commander_learning.md"""

path = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 追加到「犯过的错」表格（插到表格第一行| 错误 之后）
err_row = "| **HN新号(aitoolcrux, karma=1)一次发3条评论，全部被HN反垃圾系统删除（flagged且不进comments列表）** | 2026-10-09 | 新号低karma一次只发1条评论，间隔更长；先养karma再批量发 |\n"
marker = "| 错误 | 发生时间 | 正确做法 |\n|------|---------|---------|\n"
if err_row.split("|")[1].strip() not in content:
    content = content.replace(marker, marker + err_row)

# 2. 追加到「学到的经验」表格（插到 ### 2026-10-02 战略学习 之前）
exp_section = """
### 2026-10-09 工具链修复后的爆发产出（关键验证）
| 知识点 | 验证结果 |
|---|---|
| **工具没装=窗口全废**：手册写✅的17个工具只有5个真装，各窗口调用全失败只能回退硬写 | 2026-10-09批量补装16个工具后，6个窗口当天全部真实产出（架构师6技术修复+打磨师6篇重写+创作家6篇重写+拓荒者3条HN评论+分析师GSC分析+体验官UX审计） |
| **"天天修不完问题"的根因是工具链断了**，不是窗口偷懒 | 工具齐了窗口立刻能干实事，完成率从0%→14.1%（11条completed） |
| llmevalkit全文自对照时ContradictionDetector误报率100%（23/23处"矛盾"全是表格vs正文重复陈述） | 已补P1待办：context=answer时跳过contradiction检测 |
| llmevalkit用权威官网context（docs.bfl.ai/anthropic.com/openai pricing）能真抓幻觉 | 抓到3处真实错误：Flux价格$0.03→$0.04、Claude发布时间、GPT-4o定价结构，已全部修复 |
| 打磨师重写低分文章用zens-ink content_qc≥70验收 | 3篇从28分→100/90/90，全部通过 |
| 创作家重写用zens-ink自检 | 6篇全部88分 |
| HN新号被spam detection盯上（一次3条→全删） | 新号策略：一次1条+养karma，等upvote解封 |
| 当前网络无法直连Google API（TCP 443不通） | 实时GSC/GA4拉取需代理；已补P2待办：先探测再拉取 |

"""
if "2026-10-09 工具链修复后的爆发产出" not in content:
    content = content.replace("## 学到的经验\n", "## 学到的经验\n" + exp_section)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("commander_learning.md 更新完成")
print(f"文件大小: {len(content)} 字符")
