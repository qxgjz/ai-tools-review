# -*- coding: utf-8 -*-
"""2026-10-12 每日调度：资源协调催办 + 更新关键数据到学习笔记"""
import json, os

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")
LEARN = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])
existing_ids = {t.get("id") for t in nf}
today = "2026-10-12"

# Step 6: 协调——window2(P0=16)/创作家(P0=15)超载催办；拓荒者可承接
new_todos = [
    {
        "id": "P0-URGE-W2-20261012",
        "task": "催办：window2当前37条pending(P0=16)严重超载，完成率<50%；本周优先消化P0-COMMUNITY-REDDIT(Reddit暖号)、P0-BACKLINK-15(外链5-15域名)、新目录提交3条；目录批量提交类任务可移交拓荒者分担，window2聚焦社区渠道+编辑链接",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window2", "增长黑客"],
        "source": "commander_coord_20261012",
        "created_at": today,
    },
    {
        "id": "P0-URGE-CREATOR-20261012",
        "task": "催办：创作家当前36条pending(P0=15)严重超载，完成率<50%；本周按GSC/关键词优先级批量出文>=5篇（优先ai agent词簇：best-ai-agents-2026/ai-agent-vs-chatbot/how-to-build-an-ai-agent），每篇2000字+FAQ+引用真实用户评论，写完必须交打磨师审计",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["创作家", "window3"],
        "source": "commander_coord_20261012",
        "created_at": today,
    },
]
added = 0
for t in new_todos:
    if t["id"] in existing_ids:
        continue
    nf.append(t)
    added += 1
state["next_iteration_focus"] = nf
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"协调催办新增: {added} 条，active总数: {len(nf)}")

# Step 8: 更新关键数据到学习笔记
block = f"""
## 2026-10-12 每日调度（14:4x）网站关键数据更新

| 指标 | 数值 | 变化 |
|------|------|------|
| 文章数 | 154篇 | — |
| 工具数 | 533个 | — |
| 截图数 | 144个 | — |
| archived累计 | 539条 | +10（今晨架构师round12 6条+打磨师R8/batch20 4条真完成） |
| active待办 | 93条（全pending） | 清理10条completed后+补录4条报告待办+2条协调催办 |
| GSC曝光（09-12~10-09窗口） | ~41-48 | 最佳页best-ai-voice-changers-2026 68曝光/2点击/CTR 2.9% |
| GSC点击 | 0-2 | openai_astra 68曝光/1点击/CTR 1.5% |
| GA4 | 1969 sess/8.1% eng | 仍受Bot污染（旧property） |
| 30天目标 | A≈2.3%、B=无法评估、C=0% | 未变化 |

**今日窗口真实产出（git commit+线上复测实证）**：架构师round12（62070b2 12:33 LCP/CLS/pSEO dedup 533 unique/cache bfcache + ae70a42 12:50 17 P1s verified）+打磨师R8（a1211f1 12:01 CTR 3页+HTML->MD 3篇50->100）+batch20（d8809aa 13:16 3篇 zens-ink 73/llmevalkit 100，0c7cb7a 13:26 deploy 200）+增长（hyzenpro提交成功✅+外链第七轮30条线索）+分析师（GSC 41/0、CTR 3 opps 4 todos）。
**新经验**：①completed_at未来时间戳初判存疑→git commit+线上复测证明真完成，验收必须双通道而非只看状态 ②GSC daily窗口与top_pages窗口口径不同（daily=最近7天41/0，top_pages=整窗口68/2），读报告要区分 ③window2/创作家P0超载已加催办，拓荒者可承接目录提交分担。
"""
with open(LEARN, "a", encoding="utf-8") as f:
    f.write(block)
print("关键数据已更新到 commander_learning.md")
