# -*- coding: utf-8 -*-
"""协调资源核查：window2/创作家待办结构 + GSC最新数据 + ux负载"""
import json, os, glob, datetime

ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
with open(os.path.join(ROOT, "iteration_center", "state.json"), encoding="utf-8") as f:
    state = json.load(f)
nf = state.get("next_iteration_focus", [])

# 1. window2/创作家 待办 assigned_to 结构
w2 = [t for t in nf if isinstance(t.get("assigned_to"), list) and "window2" in t["assigned_to"]]
cz = [t for t in nf if isinstance(t.get("assigned_to"), list) and "创作家" in t["assigned_to"]]
print("=== window2 待办数:", len(w2), "创作家 待办数:", len(cz))
if w2:
    from collections import Counter
    print("window2 优先级:", dict(Counter(t.get("priority") for t in w2)))
    print("window2 样例:", [str(t.get("task"))[:60] for t in w2[:5]])
if cz:
    print("创作家 样例:", [str(t.get("task"))[:60] for t in cz[:5]])

# 2. ux 负载
ux = [t for t in nf if isinstance(t.get("assigned_to"), list) and "ux" in t["assigned_to"]]
print("=== ux 待办数:", len(ux))

# 3. GSC 最新报告
gsc_files = sorted(glob.glob(os.path.join(ROOT, "gsc-ga4-report", "*")), key=os.path.getmtime, reverse=True)
print("=== gsc-ga4-report 最新5个文件 ===")
for f in gsc_files[:5]:
    print(os.path.basename(f), os.path.getmtime(f))

# 4. 读最新 GSC 数据文件
for f in gsc_files[:3]:
    if f.endswith(".md") or f.endswith(".json"):
        try:
            if f.endswith(".json"):
                d = json.load(open(f, encoding="utf-8"))
                print(os.path.basename(f), "keys:", list(d.keys())[:10] if isinstance(d, dict) else f"list len {len(d)}")
            else:
                with open(f, encoding="utf-8", errors="ignore") as mf:
                    head = mf.read(800)
                print(os.path.basename(f), "head:", head[:200].replace("\n", " "))
        except Exception as e:
            print(os.path.basename(f), "err", e)
