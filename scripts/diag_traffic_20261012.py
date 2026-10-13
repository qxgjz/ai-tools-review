# -*- coding: utf-8 -*-
"""流量趋势诊断：对比 GSC 多天拉取"""
import json, os, glob

GSC_DIR = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\gsc-ga4-report"
files = sorted(glob.glob(os.path.join(GSC_DIR, "live_pull_*.json")))

print("=== GSC 拉取趋势（按时间）===")
for f in files:
    with open(f, encoding="utf-8") as fh:
        g = json.load(fh)
    daily = g.get("daily", [])
    tot_imp = sum(d.get("impressions", 0) for d in daily)
    tot_clk = sum(d.get("clicks", 0) for d in daily)
    tp = g.get("top_pages", []) or []
    tq = g.get("top_queries", []) or []
    tp_imp = sum(p.get("impressions", 0) for p in tp)
    tp_clk = sum(p.get("clicks", 0) for p in tp)
    print(f"{os.path.basename(f)}: daily[{len(daily)}天] 曝光{tot_imp}/点击{tot_clk} | top_pages 曝光{tp_imp}/点击{tp_clk} | 窗口{g.get('query_window_start','?')}~{g.get('query_window_end','?')}")

# 最新文件详情
print("\n=== 最新文件 top_queries/top_pages ===")
with open(files[-1], encoding="utf-8") as fh:
    g = json.load(fh)
print("top_queries:")
for q in (g.get("top_queries") or [])[:10]:
    print(f"  {q.get('keys')} | clk{q.get('clicks')} impr{q.get('impressions')} ctr{q.get('ctr',0):.2%} pos{q.get('position')}")
print("top_pages:")
for p in (g.get("top_pages") or [])[:10]:
    print(f"  {p.get('keys')} | clk{p.get('clicks')} impr{p.get('impressions')} ctr{p.get('ctr',0):.2%} pos{p.get('position')}")
