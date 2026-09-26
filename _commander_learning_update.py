import json, os
from datetime import datetime

base = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
learning_path = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"

# === 1. Append learning to commander_learning.md ===
learning_entry = """| 【2026 SEO/GEO/AI搜索前沿15知识点】1.Princeton GEO研究实证：Statistics Addition（注入具体数字/百分比/金额/日期）是排名第一的GEO战术，引用位置提升41%；2.三大高ROI战术：Statistics Addition(+40%可见性)、Quotation Addition（权威第三方直接引语，AI模型训练识别归因）、Cite Sources（内联引用自己的声明来源）；3.ChatGPT每答案引用2-4源，Wikipedia占top10约48%，偏好页面前30%的确定性答案；4.Perplexity每答案引用4-8源，强时效性加权(≤90天内容)，Reddit占top10约47%，偏好具体事实/数字/日期的自包含段落；5.4亿条引用分析(Evertune 2026.5)：63%指向listicle列表文章，列表格式是AI引用磁石；6.Ahrefs配对研究：Schema markup对AI引用无显著提升，不要迷信结构化数据；7.llms.txt是新兴标准(Anthropic/Perplexity/OpenAI已采纳)，但截至2026中无确证引用权重，约10%域名已部署，低投入高潜在收益建议做；8.GEO不是SEO替代，是建立在SEO基础(可爬取/索引/权威/内链)之上的AI答案可见层；9.低搜索量长尾词在AI引擎中仍被高频提问，不要因传统搜索量低而忽视；10.E-E-A-T信号喂AI引擎：作者署名+资质、发布/更新日期、organization schema、透明方法论章节；11.答案优先结构：每段先给直接答案再给上下文，段落控制2-3句，问题式标题匹配AI提问方式；12.第三方信号主导AI引用：Reddit 47%(Perplexity)+Wikipedia 48%(ChatGPT)，实体清晰度和外部验证比站内优化更重要；13.GEO漏斗诊断：Indexed→Retrieved→Cited→Visited，逐段诊断断点在哪；14.内容刷新周期≤90天(Perplexity时效性加权)，重要内容至少每3个月更新数据和案例；15.GEO可落地优先级：先做llms.txt+答案优先改写top10页面+注入统计数据+Reddit第三方建设，schema不是优先项 | 2026-09-26 指挥官每日学习（方向⑤SEO/GEO前沿） |"""

with open(learning_path, "r", encoding="utf-8") as f:
    content = f.read()

# Insert after the last experience row (before the "---" separator after experience table)
# Find the marker "## 用户明确要求" and insert before it
marker = "## 用户明确要求"
if marker in content:
    content = content.replace(marker, learning_entry + "\n\n---\n\n" + marker, 1)
    with open(learning_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("学习笔记已更新: GEO 15知识点已写入")

# === 2. Update key data section ===
# Find and replace the website key data
old_data_marker = "## 网站关键数据"
new_data = """## 网站关键数据（2026-09-26 第103轮更新）

- 文章：107篇（最新2026-09-26: Canva AI vs Adobe Firefly）
- 工具：533个
- 截图：115个（66 webp + 49 svg）
- 迭代轮次：103轮
- Quick Answer覆盖率：100%
- GSC（最新到9/21）：9点击 / 1832曝光 / CTR 0.49% / 平均排名24.82
- GA4（9/18-9/24）：1151用户但96%新加坡爬虫(1100)，真实Google organic 7会话，美国真实用户27
- state.json待办：197条（61活跃 + 134完成），P0=8, P1=25
- 变现：已上线联盟2个（ElevenLabs 22%×12月、Mangools 25-35%终身）
- 今日重大修复：ISR超限(300万/100万→force-static全静态)、not-found 7MB→87KB、文章正文消失恢复、CI lint+unit tests修复、prettier全量格式化

---"""

if old_data_marker in content:
    # Find the old data section and replace it
    import re
    pattern = r"## 网站关键数据.*?(?=\n---\n|\n## )"
    content = re.sub(pattern, new_data, content, count=1, flags=re.DOTALL)
    with open(learning_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("关键数据已更新到第103轮")

# === 3. Add GEO actionable todos to state.json ===
state_path = os.path.join(base, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

nif = state.get("next_iteration_focus", [])
existing_titles = set(str(t.get("title", "")) for t in nif)

new_todos = [
    {
        "id": "P1-GEO-LLMSTXT-001",
        "title": "窗口1：部署/llms.txt文件（AI爬虫内容地图，低投入高潜在收益）",
        "priority": "P1",
        "status": "pending",
        "assigned_to": "窗口1",
        "source": "learning: GEO前沿 2026-09-26",
        "description": "按llmstxt.org规范创建根目录llms.txt，包含品牌简介+top20最有引用价值的页面链接+简短描述。Anthropic/Perplexity/OpenAI已采纳，约10%域名已部署，无确证权重但低投入。"
    },
    {
        "id": "P1-GEO-STATS-001",
        "title": "窗口3：GEO内容改造——top10高曝光页面注入具体统计数据+答案优先结构",
        "priority": "P1",
        "status": "pending",
        "assigned_to": "窗口3",
        "source": "learning: GEO前沿 2026-09-26",
        "description": "Princeton研究：Statistics Addition提升AI引用位置41%。对GSC top10页面（stable-diffusion/dify/cursor/midjourney/gemini等）每300字至少1个具体数字，段落首句直接给答案，段落2-3句。"
    },
    {
        "id": "P0-GEO-REDDIT-001",
        "title": "窗口2：Reddit第三方权威建设——Perplexity 47%引用来自Reddit，必须建存在感",
        "priority": "P0",
        "status": "pending",
        "assigned_to": "窗口2",
        "source": "learning: GEO前沿 2026-09-26",
        "description": "Perplexity每答案引用4-8源，Reddit占top10约47%，强时效性≤90天。在r/ChatGPT/r/ArtificialInteligence/r/midjourney等AI subreddit提供有价值的回答，自然提及aitoolcrux的对比数据。9:1法则（9次贡献1次推广）。"
    },
    {
        "id": "P1-GEO-REFRESH-001",
        "title": "窗口3：建立90天内容刷新机制——Perplexity强时效性加权，过期内容不被引用",
        "priority": "P1",
        "status": "pending",
        "assigned_to": "窗口3",
        "source": "learning: GEO前沿 2026-09-26",
        "description": "Perplexity对≤90天内容有强时效性加权。建立内容刷新SOP：每季度更新top50页面的数据/案例/定价，更新日期字段，确保AI引擎认为内容新鲜。"
    },
    {
        "id": "P2-GEO-MONITOR-001",
        "title": "窗口4：建立AI引用监测——手动测试ChatGPT/Perplexity对目标query是否引用我们",
        "priority": "P2",
        "status": "pending",
        "assigned_to": "窗口4",
        "source": "learning: GEO前沿 2026-09-26",
        "description": "每周用10个核心query在ChatGPT Search和Perplexity测试，记录是否被引用、引用位置、引用页面。GEO漏斗：Indexed→Retrieved→Cited→Visited，诊断断点。可用Otterly/Profound工具辅助。"
    }
]

added = 0
for todo in new_todos:
    if todo["title"] not in existing_titles:
        nif.append(todo)
        added += 1

state["next_iteration_focus"] = nif
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"state.json已更新: 新增{added}条GEO待办 (P0=1, P1=3, P2=1)")
print(f"当前总待办: {len(nif)}条")
