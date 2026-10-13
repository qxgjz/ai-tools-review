# -*- coding: utf-8 -*-
"""2026-10-12 早间：GSC最新读数 + audit_findings新增问题检查"""
import json, os, datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# 1. GSC最新
gsc_dir = os.path.join(ROOT, "gsc-ga4-report")
gsc_files = [f for f in os.listdir(gsc_dir) if f.startswith("live_pull")]
gsc_files.sort()
latest = gsc_files[-1]
print(f"最新GSC: {latest}")
with open(os.path.join(gsc_dir, latest), encoding="utf-8") as f:
    gsc = json.load(f)
print(f"GSC key: {list(gsc.keys())[:10]}")
if "rows" in gsc:
    total_imp = sum(r.get("impressions", 0) for r in gsc["rows"])
    total_clk = sum(r.get("clicks", 0) for r in gsc["rows"])
    print(f"GSC: impressions={total_imp} clicks={total_clk} rows={len(gsc['rows'])}")
elif isinstance(gsc, dict):
    for k in ["impressions", "clicks", "total_impressions", "total_clicks"]:
        if k in gsc:
            print(f"GSC {k}={gsc[k]}")

# 2. audit_findings 检查最近新增的P0/P1（取文件末尾80行找新内容）
af = os.path.join(ROOT, "iteration_center", "audit_findings.md")
with open(af, encoding="utf-8") as f:
    lines = f.readlines()
print(f"\naudit_findings总行数: {len(lines)}")
# 找文件头部的更新时间或日志
head = "".join(lines[:40])
if "2026-10-12" in head:
    print("头部含10-12标记")
# 打印末尾40行看是否有新待办线索
tail = "".join(lines[-40:])
print("\n=== 末尾40行 ===")
print(tail)
