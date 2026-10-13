# -*- coding: utf-8 -*-
"""2026-10-12 周走查：GSC最新 + state本周归档统计"""
import json, os, glob

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
IC = os.path.join(ROOT, "iteration_center")

# GSC最新
gsc_dir = os.path.join(ROOT, "gsc-ga4-report")
files = sorted([f for f in os.listdir(gsc_dir) if f.startswith("live_pull")])
print("GSC文件数:", len(files))
if files:
    latest = files[-1]
    print("最新:", latest)
    with open(os.path.join(gsc_dir, latest), encoding="utf-8") as f:
        gsc = json.load(f)
    print("daily_start:", gsc.get("daily_start"), "daily_end:", gsc.get("daily_end"))
    print("query_window:", gsc.get("query_window_start"), "->", gsc.get("query_window_end"))
    print("top_queries:", gsc.get("top_queries"))
    print("top_pages:", gsc.get("top_pages"))
    d = gsc.get("daily", {})
    if isinstance(d, dict) and d:
        print("daily示例:", list(d.items())[:5])

# state本周归档（10-06之后archived）
with open(os.path.join(IC, "state.json"), encoding="utf-8") as f:
    state = json.load(f)
arch = state.get("archived_todos", [])
week_arch = [t for t in arch if str(t.get("archived_at", t.get("completed_at", ""))).startswith("2026-10-0[6-9]") or str(t.get("archived_at", t.get("completed_at", ""))).startswith("2026-10-1")]
print("\narchived累计:", len(arch), "本周(10/6后)归档:", len(week_arch))
for t in week_arch[-15:]:
    print(f"  - {t.get('id')} | {t.get('priority')} | archived={t.get('archived_at', '?')[:10]} | {str(t.get('task'))[:70]}")

nf = state.get("next_iteration_focus", [])
print("\nactive:", len(nf))
from collections import Counter
print("状态:", dict(Counter(t.get("status") for t in nf)))
print("优先级:", dict(Counter(t.get("priority") for t in nf)))
