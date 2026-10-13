# -*- coding: utf-8 -*-
import json

state_path = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)

todos = state.get("next_iteration_focus", [])
existing_ids = {t.get("id") for t in todos}

new_todos = [
    {
        "id": "P2-GOOGLE-NETWORK-BLOCK-001",
        "task": "当前运行环境无法直连Google API（TCP 443不通，已实测）。所有实时GSC/GA4拉取会超时。下次触发先探测网络，通则拉实时数据，不通则跳过并记录。",
        "assigned_to": "analyst",
        "priority": "P2",
        "status": "pending",
        "source": "audit_findings.md 2026-10-09",
        "created_at": "2026-10-09"
    },
    {
        "id": "P1-CONTENT-KEYWORD-DENSITY-001",
        "task": "打磨师质检4篇草稿关键词密度0.0-0.13%<0.5%阈值。创作家写新文章时主关键词自然出现≥3次（标题/H2/正文首段/结尾），发布前自查密度≥0.5%。",
        "assigned_to": ["window3"],
        "priority": "P1",
        "status": "pending",
        "source": "hallucination_audit_report.md 2026-10-09",
        "created_at": "2026-10-09"
    },
    {
        "id": "P1-TOOLKIT-CONTRADICTION-FIX-001",
        "task": "llmevalkit_toolkit.py的ContradictionDetector在全文自对照(context=answer)时误报率100%(23/23)。给toolkit加后处理：当context与answer相同(全文自对照)时跳过contradiction检测，避免误扣分。",
        "assigned_to": ["window5"],
        "priority": "P1",
        "status": "pending",
        "source": "hallucination_audit_report.md 2026-10-09",
        "created_at": "2026-10-09"
    },
    {
        "id": "P1-CONTENT-CAUSAL-CITE-001",
        "task": "claude-37-vs-gpt4o和midjourney-vs-flux两篇causal评分低(0.33-0.5)，断言缺来源。打磨师给2篇补上因果句的权威来源引用（Anthropic官方benchmark/官方定价页）。",
        "assigned_to": ["window5"],
        "priority": "P1",
        "status": "pending",
        "source": "hallucination_audit_report.md 2026-10-09",
        "created_at": "2026-10-09"
    },
]

added = 0
for t in new_todos:
    if t["id"] not in existing_ids:
        todos.insert(0, t)
        added += 1

state["next_iteration_focus"] = todos
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"补录 {added} 条新待办")
print(f"当前 next_iteration_focus: {len(todos)} 条")

# 各窗口pending数量统计（含in_progress）
from collections import Counter
window_map = {"window1": "架构师", "architect": "架构师", "window2": "拓荒者", "backlink": "拓荒者",
              "window3": "创作家", "creator": "创作家", "window4": "分析师", "analyst": "分析师",
              "window5": "打磨师", "polisher": "打磨师", "window6": "体验官", "ux": "体验官",
              "all_windows": "全部窗口", "commander": "指挥官"}
win_count = Counter()
for t in todos:
    a = t.get("assigned_to", "")
    if isinstance(a, list):
        a = ",".join(a)
    key = window_map.get(a, a)
    win_count[key] += 1
print(f"\n=== 各窗口当前待办数 ===")
for k, v in win_count.most_common():
    print(f"  {k}: {v}")
