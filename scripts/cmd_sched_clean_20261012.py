# -*- coding: utf-8 -*-
"""2026-10-12 每日调度：清理completed + 报告校验 + 关键数据"""
import json, os, glob, re

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
IC = os.path.join(ROOT, "iteration_center")
STATE = os.path.join(IC, "state.json")

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])
archived = state.get("archived_todos", [])

# ===== Step 4: 清理 completed =====
completed = [t for t in nf if t.get("status") == "completed"]
kept = [t for t in nf if t.get("status") != "completed"]
for t in completed:
    t["archived_at"] = "2026-10-12T13:40:00+08:00"
archived.extend(completed)
state["next_iteration_focus"] = kept
state["archived_todos"] = archived
with open(STATE, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"[Step4] 清理 completed: {len(completed)} 条移到 archived（累计 {len(archived)}）")
print(f"  active 剩余: {len(kept)}（全 pending）")

# ===== Step 5: 报告文件列表 =====
print(f"\n[Step5] iteration_center 报告文件:")
report_files = sorted(glob.glob(os.path.join(IC, "*.md")))
for rf in report_files:
    print(f"  {os.path.basename(rf)} ({os.path.getsize(rf)}B)")

# ===== Step 8: 关键数据 =====
print(f"\n[Step8] 关键数据:")
# 文章数
posts_path = os.path.join(ROOT, "data", "posts.json")
if os.path.exists(posts_path):
    with open(posts_path, encoding="utf-8") as f:
        posts = json.load(f)
    print(f"  文章数: {len(posts)}")
else:
    print("  文章数: data/posts.json 不存在")
# 工具数
tools_path = os.path.join(ROOT, "data", "tools.json")
if os.path.exists(tools_path):
    with open(tools_path, encoding="utf-8") as f:
        tools = json.load(f)
    print(f"  工具数: {len(tools)}")
else:
    print("  工具数: data/tools.json 不存在")
# 截图数
shots = glob.glob(os.path.join(ROOT, "public", "screenshots", "**", "*"), recursive=True)
img = [s for s in shots if os.path.isfile(s) and re.search(r'\.(png|jpg|jpeg|webp)$', s, re.I)]
print(f"  截图数: {len(img)}")
# 迭代轮次
print(f"  迭代轮次: {state.get('iteration_count', state.get('iteration', '?'))}")
# 存档数
print(f"  archived累计: {len(archived)}")
