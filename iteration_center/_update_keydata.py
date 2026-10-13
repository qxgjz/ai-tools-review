# -*- coding: utf-8 -*-
import json, os, glob, datetime

proj = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# 文章数
try:
    with open(os.path.join(proj, "data", "posts.json"), "r", encoding="utf-8") as f:
        posts = json.load(f)
    post_count = len(posts) if isinstance(posts, list) else len(posts.get("posts", []))
except Exception as e:
    post_count = f"ERR {e}"

# 工具数
try:
    with open(os.path.join(proj, "data", "tools.json"), "r", encoding="utf-8") as f:
        tools = json.load(f)
    tool_count = len(tools) if isinstance(tools, list) else len(tools.get("tools", []))
except Exception as e:
    tool_count = f"ERR {e}"

# 截图数
shots = glob.glob(os.path.join(proj, "public", "screenshots", "**", "*"), recursive=True)
shot_count = len([s for s in shots if os.path.isfile(s)])

# 迭代轮次
state_path = os.path.join(proj, "iteration_center", "state.json")
with open(state_path, "r", encoding="utf-8") as f:
    state = json.load(f)
iteration = state.get("iteration_count", state.get("current_iteration", "?"))
todos = state.get("next_iteration_focus", [])
from collections import Counter
sc = Counter(t.get("status","?") for t in todos)
pc = Counter(t.get("priority","?") for t in todos)

print(f"文章数: {post_count}")
print(f"工具数: {tool_count}")
print(f"截图数: {shot_count}")
print(f"迭代轮次: {iteration}")
print(f"待办: {dict(sc)}")
print(f"优先级: {dict(pc)}")
print(f"GSC字段: impressions={state.get('gsc_latest_impressions')}, clicks={state.get('gsc_latest_clicks')}")
