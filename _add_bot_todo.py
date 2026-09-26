import json, os

base = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
state_path = os.path.join(base, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

nif = state.get("next_iteration_focus", [])
existing_titles = set(str(t.get("title", "")) for t in nif)

bot_todo = {
    "id": "P0-GA4-BOT-FILTER-001",
    "title": "窗口4：GA4 Bot过滤——96%新加坡数据中心爬虫污染数据，必须过滤",
    "priority": "P0",
    "status": "pending",
    "assigned_to": "窗口4",
    "source": "audit_findings.md P0-1 2026-09-26",
    "description": "GA4近7天1151用户中1100(96%)来自新加坡数据中心IP，互动率仅5.8%，严重污染所有指标。必须：1)在GA4中创建Bot过滤audience（排除新加坡数据中心IP+互动率<10%+单页会话）；2)GA4管理后台启用自动Bot过滤；3)对比过滤前后数据，建立干净数据视图。"
}

if bot_todo["title"] not in existing_titles:
    nif.append(bot_todo)
    state["next_iteration_focus"] = nif
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("已补充P0待办: GA4 Bot过滤")
else:
    print("GA4 Bot过滤待办已存在")

print(f"总待办: {len(nif)}")
