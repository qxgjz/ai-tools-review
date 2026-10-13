# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-13"

# 读最新 GSC 数据
gsc_path = os.path.join(BASE, "gsc-ga4-report", "live_pull_20261013_0800.json")
gsc = json.load(open(gsc_path, "r", encoding="utf-8"))

print("=" * 60)
print("GSC 数据概览")
print("=" * 60)
print(f"数据区间: {gsc.get('query_window_start')} ~ {gsc.get('query_window_end')}")
print(f"拉取时间: {gsc.get('pulled_at')}")

# 汇总
daily = gsc.get("daily", [])
total_clicks = sum(d.get("clicks", 0) for d in daily)
total_impr = sum(d.get("impressions", 0) for d in daily)
avg_ctr = (total_clicks / total_impr * 100) if total_impr > 0 else 0

print(f"\n总点击: {total_clicks}")
print(f"总曝光: {total_impr}")
print(f"平均 CTR: {avg_ctr:.2f}%")

# 日趋势
print(f"\n{'日期':<12} {'点击':<6} {'曝光':<6} {'CTR':<8} {'排名':<8}")
print("-" * 50)
for d in daily[-7:]:
    date = d.get("keys", [""])[0]
    clk = d.get("clicks", 0)
    impr = d.get("impressions", 0)
    ctr = d.get("ctr", 0) * 100
    pos = d.get("position", 0)
    print(f"{date:<12} {clk:<6} {impr:<6} {ctr:<8.2f} {pos:<8.2f}")

# Top queries
print(f"\n{'='*60}")
print("Top Queries (Top 20)")
print(f"{'='*60}")
queries = gsc.get("top_queries", [])
for q in queries[:20]:
    kw = q.get("keys", [""])[0]
    clk = q.get("clicks", 0)
    impr = q.get("impressions", 0)
    ctr = q.get("ctr", 0) * 100
    pos = q.get("position", 0)
    print(f"{kw[:45]:<45} clk={clk} impr={impr} ctr={ctr:.1f}% pos={pos:.1f}")

# Top pages
print(f"\n{'='*60}")
print("Top Pages (Top 20)")
print(f"{'='*60}")
pages = gsc.get("top_pages", [])
for p in pages[:20]:
    url = p.get("keys", [""])[0]
    clk = p.get("clicks", 0)
    impr = p.get("impressions", 0)
    ctr = p.get("ctr", 0) * 100
    pos = p.get("position", 0)
    short = url.replace("https://www.aitoolcrux.com", "")[:50]
    print(f"{short:<50} clk={clk} impr={impr} ctr={ctr:.1f}% pos={pos:.1f}")

# CTR 优化机会：排名 5-15 但 CTR<3%
print(f"\n{'='*60}")
print("CTR 优化机会（排名 5-20 但 CTR<3%）")
print(f"{'='*60}")
ctr_opps = []
for p in pages:
    pos = p.get("position", 0)
    ctr = p.get("ctr", 0) * 100
    impr = p.get("impressions", 0)
    url = p.get("keys", [""])[0]
    if 5 <= pos <= 20 and ctr < 3 and impr >= 5:
        ctr_opps.append({"url": url, "pos": pos, "ctr": ctr, "impr": impr})
        print(f"  {url[:60]:<60} pos={pos:.1f} ctr={ctr:.1f}% impr={impr}")

print(f"\nCTR 优化机会总数: {len(ctr_opps)}")

# 保存分析结果供后续使用
analysis = {
    "total_clicks": total_clicks,
    "total_impr": total_impr,
    "avg_ctr": avg_ctr,
    "ctr_opps": ctr_opps,
    "top_queries_count": len(queries),
    "top_pages_count": len(pages),
}
print(f"\n分析完成。")
