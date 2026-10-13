# -*- coding: utf-8 -*-
"""2026-10-12 周走查：读本周数据概览"""
import json, os, glob

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
IC = os.path.join(ROOT, "iteration_center")

# 1. iteration_log.json
for p in [os.path.join(IC, "iteration_log.json"), os.path.join(ROOT, "iteration_log.json")]:
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            log = json.load(f)
        print(f"iteration_log.json: {p}")
        if isinstance(log, list):
            print(f"  条目数: {len(log)}")
            for item in log[-8:]:
                if isinstance(item, dict):
                    print(f"  - {item.get('date', item.get('ts', '?'))} | {str(item.get('window', item.get('agent', '?')))} | {str(item.get('summary', item.get('task', item.get('desc', ''))))[:90]}")
        elif isinstance(log, dict):
            print(f"  keys: {list(log.keys())[:15]}")
        break

# 2. 检查health_report / weekly_roi / 其他周报
for name in ["health_report.md", "weekly_roi.md", "commander_weekly_review.md"]:
    p = os.path.join(IC, name)
    print(f"\n=== {name}: {'存在' if os.path.exists(p) else '不存在'} ===")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            content = f.read()
        print(content[:1500])
