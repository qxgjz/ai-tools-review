# -*- coding: utf-8 -*-
"""核查completed待办真实性：完整记录 + 架构师日志位置 + 时间戳"""
import json, os, glob, datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])

print("=== completed 待办完整记录 ===")
for t in nf:
    if t.get("status") == "completed":
        print(json.dumps({k: t.get(k) for k in ("id","status","priority","assigned_to","task","source","created_at","updated_at","archived_at","completed_at","note","remark") if k in t}, ensure_ascii=False, indent=1))

# 查找架构师相关日志（window1/架构师/architect）
print("\n=== 全项目搜索架构师日志 ===")
for pat in ("window_logs/*arch*", "window_logs/*window1*", "window_logs/*架构*", "iteration_center/*arch*"):
    hits = glob.glob(os.path.join(ROOT, pat))
    for h in hits:
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(h)).strftime("%m-%d %H:%M")
        print(mt, h)

print("\n=== window_logs 完整文件列表 ===")
for f in sorted(glob.glob(os.path.join(ROOT, "window_logs", "*"))):
    mt = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%m-%d %H:%M")
    print(mt, os.path.basename(f))
