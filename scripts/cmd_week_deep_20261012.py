# -*- coding: utf-8 -*-
"""2026-10-12 周走查：本周(10-05~10-12)数据深挖"""
import json, os, glob

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
IC = os.path.join(ROOT, "iteration_center")

# 1. iteration_log 全量看结构
with open(os.path.join(IC, "iteration_log.json"), encoding="utf-8") as f:
    log = json.load(f)
print("iteration_log 类型:", type(log).__name__)
if isinstance(log, dict):
    print("keys:", list(log.keys())[:20])
    # 尝试找本周条目
    for k in list(log.keys())[:5]:
        v = log[k]
        print(f"  {k}: {str(v)[:120]}")
elif isinstance(log, list):
    # 统计本周条目
    week_items = [i for i in log if isinstance(i, dict) and str(i.get("date", i.get("ts", ""))).startswith("2026-10")]
    print(f"总条目59，本周(10月)条目: {len(week_items)}")
    for i in week_items[:20]:
        print(f"  - {i.get('date', i.get('ts', '?'))} | {i.get('window', i.get('agent', i.get('title','?')))} | {str(i.get('summary', i.get('details', i.get('desc', i.get('task','')))))[:100]}")

print("\n=== window_logs 本周文件 ===")
for f in sorted(glob.glob(os.path.join(ROOT, "window_logs", "*.md")), key=os.path.getmtime, reverse=True):
    mt = os.path.getmtime(f)
    import datetime
    d = datetime.datetime.fromtimestamp(mt)
    if d >= datetime.datetime(2026, 10, 5):
        print(f"  {os.path.basename(f)} ({d.strftime('%m-%d %H:%M')})")
