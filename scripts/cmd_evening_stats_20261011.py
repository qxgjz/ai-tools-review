# -*- coding: utf-8 -*-
"""指挥官 2026-10-11 21:38 晚间调度：统计待办状态 + 窗口日志检查"""
import json, os, glob, collections, datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
STATE = os.path.join(ROOT, "iteration_center", "state.json")

with open(STATE, encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])
arch = state.get("archived_todos", [])

pending = sum(1 for t in nf if t.get("status") == "pending")
inprog = sum(1 for t in nf if t.get("status") == "in_progress")
comp = sum(1 for t in nf if t.get("status") == "completed")
by_prio = collections.Counter(t.get("priority") for t in nf)

# 按窗口统计（assigned_to 可能是 list 或 str）
def win_key(t):
    a = t.get("assigned_to")
    if isinstance(a, list):
        return a[0] if a else "?"
    return str(a)

by_win = collections.Counter(win_key(t) for t in nf if t.get("status") != "completed")
by_win_comp = collections.Counter(win_key(t) for t in nf if t.get("status") == "completed")

total = len(nf)
rate = (comp / (pending + comp) * 100) if (pending + comp) > 0 else 0

print("=== state.json 当前 ===")
print("active:", total, "| pending:", pending, "| in_progress:", inprog, "| completed:", comp)
print("完成率:", round(rate, 1), "%")
print("优先级分布:", dict(by_prio))
print("pending按窗口:", dict(by_win))
print("completed按窗口:", dict(by_win_comp))
print("archived累计:", len(arch))
print("iteration:", state.get("iteration", 0))

# completed 待办明细（供清理用）
comp_todos = [t for t in nf if t.get("status") == "completed"]
print("\n=== completed 待办明细 ===")
for t in comp_todos:
    print(t.get("id"), "|", t.get("priority"), "|", str(t.get("task"))[:80], "|", t.get("assigned_to"))

# 窗口日志最近修改时间
print("\n=== window_logs 最近10个文件 ===")
logs = sorted(glob.glob(os.path.join(ROOT, "window_logs", "*")), key=os.path.getmtime, reverse=True)
for f in logs[:10]:
    mt = datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%m-%d %H:%M")
    print(mt, os.path.basename(f))
