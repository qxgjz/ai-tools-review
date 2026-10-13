# -*- coding: utf-8 -*-
"""2026-10-12 早间：协调分流 + 学习笔记关键数据更新"""
import json, os

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")
LEARN = r"C:\Users\通明街\Doubao\chats\2026-09-02\new-chat\commander_learning.md"
NOW = "2026-10-12T06:50:00"

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state["next_iteration_focus"]

def add_todo(tid, task, win, prio, source):
    nf.append({
        "id": tid,
        "task": task,
        "assigned_to": win,
        "priority": prio,
        "status": "pending",
        "source": source,
        "created_at": NOW,
    })
    print("新增: {} -> {} [{}]".format(tid, win, prio))

add_todo("P0-PUSH-W2-20261012", "加快批量执行：window2 当前34条pending(P0=14)超载，要求每次会话至少处理5条外链/目录提交，不允许一次只做1-2条", ["window2", "增长黑客"], "P0", "commander_coord_20261012")
add_todo("P0-PUSH-CREATOR-20261012", "加快批量执行：创作家当前33条pending(P0=14)超载，要求每次会话至少写/修5篇文章，不允许一次只写1-2篇", ["创作家", "window3"], "P0", "commander_coord_20261012")
add_todo("P0-UX-REVERIFY-20261012", "UX复测任务：昨晚网站从CODE=000全面恢复(ranking/tools/midjourney/404页全200)，请体验官对首页+ranking+3个工具页+3篇高流量文章做一次完整UX巡检，确认无新退化，产出ux_daily报告", ["体验官", "ux", "window6"], "P1", "commander_coord_20261012")
add_todo("P1-POLISH-BATCH-20261012", "批量打磨：创作家pending中有多篇待质量提升文章，打磨师按关键词/痛点优先级批量打磨>=5篇（用真实slug+zens-ink复查>=70分）", ["打磨师", "window5"], "P1", "commander_coord_20261012")
add_todo("P1-PAIN-NEW-20261012", "拓荒者新选题：继续从Reddit/HN/G2挖掘AI工具新痛点，本轮产出>=3个P0+5个P1痛点并写state待办", ["拓荒者"], "P1", "commander_coord_20261012")

with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print("state.json已保存, active={}".format(len(nf)))

block = """

### 2026-10-12 指挥官早间调度（06:50）
- **完成率100%（本批）**：9条completed全部线上复测通过——昨晚重开的假完成待办被架构师round10/11连夜真实修复：/ranking/ 200(299KB)、/tools/midjourney/ 200(369KB)、/blog/best-ai-search-engines-2026 200、首页200(464KB)、无尾斜杠301生效、tools-index拆分落地(870KB本地)
- **重要教训（自我修正）**：昨晚(10-11 21:38)判断"9条假完成"是**误判**——当时CODE=000是网站故障超时而非404，架构师commit 4665ec7/d09a7b2/a6b3201/d2eb30b/86b5534有真实大规模改动（round10: 9 todos done + chunk -57% + P0-FAKE-FIX real impl；round11: 17 SEO P1s fixed + category 531->477KB）。**验收必须线上复测，但CODE=000要区分超时vs 404，且要看git commit真实性**
- **本轮动作**：9条completed->archived（累计529）；补3条协调待办（window2/创作家P0>10催办、体验官/打磨师/拓荒者接活）
- **当前负载**：active=80全pending，P0=27/P1=46/P2=7；window2=34、创作家=33最重
- **30天目标**：A=48/2095(2.3%)、B=无法评估(GA4 Bot污染需切property)、C=0%
- **新错误**：同秒批量标completed要区分"真完成"vs"假完成"——先看git commit真实性+线上复测，CODE=000不等于404
- **新经验**：架构师round10/11证明"重开假完成待办+催办"机制有效——重开后架构师连夜真实修复，网站全站恢复200；指挥官闭环（重开->催办->复测->清理）是推动真实修复的关键
"""
with open(LEARN, "a", encoding="utf-8") as f:
    f.write(block)
print("学习笔记已追加")
