# -*- coding: utf-8 -*-
import json, os
from datetime import datetime

BASE = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
TODAY = "2026-10-12"
NOW = datetime.now().isoformat(timespec="seconds")

gsc = json.load(open(os.path.join(BASE, "gsc-ga4-report", "live_pull_20261012_2007.json"), "r", encoding="utf-8"))
queries = gsc.get("top_queries", [])
pages = gsc.get("top_pages", [])

# 筛选排名 15-50 且有曝光的查询
opportunities = []
for q in queries:
    pos, impr, clk = q["position"], q["impressions"], q["clicks"]
    kw = q["keys"][0]
    if 15 <= pos <= 50 and impr >= 5:
        ctr = clk / max(impr, 1) * 100
        opportunities.append({
            "keyword": kw,
            "impr": impr,
            "clicks": clk,
            "ctr": round(ctr, 2),
            "pos": round(pos, 1),
        })

# 按曝光排序
opportunities.sort(key=lambda x: x["impr"], reverse=True)
top20 = opportunities[:20]

print(f"Total queries: {len(queries)}")
print(f"Opportunities (pos 15-50, impr>=5): {len(opportunities)}")
print(f"Top 20:")
for i, o in enumerate(top20, 1):
    print(f"  {i}. {o['keyword']}: impr={o['impr']}, pos={o['pos']}, CTR={o['ctr']}%")

# 页面维度的机会（排名 15-50）
page_opps = []
for p in pages:
    pos, impr, clk = p["position"], p["impressions"], p["clicks"]
    url = p["keys"][0].replace("https://www.aitoolcrux.com", "")
    if 15 <= pos <= 50 and impr >= 10:
        ctr = clk / max(impr, 1) * 100
        page_opps.append({"url": url, "impr": impr, "pos": round(pos,1), "ctr": round(ctr,2)})
page_opps.sort(key=lambda x: x["impr"], reverse=True)

print(f"\nPage opportunities (pos 15-50, impr>=10): {len(page_opps)}")
for p in page_opps[:10]:
    print(f"  {p['url']}: impr={p['impr']}, pos={p['pos']}")

# 输出 keyword_opportunities.md
md = f"""# GSC 关键词机会清单（每周一筛选）

**生成时间**: {NOW}
**数据来源**: live_pull_20261012_2007.json
**筛选条件**: 排名 15-50 位，曝光 >= 5

## Total keywords analyzed: {len(queries)}

## Top {len(top20)} 机会关键词（按曝光排序）

| # | 关键词 | 曝光 | 排名 | 点击 | CTR | 优先级 |
|---|--------|------|------|------|-----|--------|
"""

for i, o in enumerate(top20, 1):
    if o["impr"] >= 20:
        pri = "P0"
    elif o["impr"] >= 10:
        pri = "P1"
    else:
        pri = "P2"
    md += f"| {i} | {o['keyword']} | {o['impr']} | {o['pos']} | {o['clicks']} | {o['ctr']}% | {pri} |\n"

md += f"""
## 页面机会（排名 15-50，曝光 >= 10）

| 页面 | 曝光 | 排名 | CTR |
|------|------|------|-----|
"""
for p in page_opps:
    md += f"| {p['url']} | {p['impr']} | {p['pos']} | {p['ctr']}% |\n"

md += """
## 建议行动

- **P0 关键词**（曝光 >= 20）：优先优化现有内容或新建文章，争取排名进入前 10
- **P1 关键词**（曝光 10-19）：在现有相关文章中内链锚文本指向
- **P2 关键词**（曝光 5-9）：监控，观察是否有上升趋势
"""

with open(os.path.join(BASE, "iteration_center", "keyword_opportunities.md"), "w", encoding="utf-8") as f:
    f.write(md)
print(f"\n[OK] keyword_opportunities.md written")

# 更新 state.json：P0 关键词写待办
state_path = os.path.join(BASE, "iteration_center", "state.json")
state = json.load(open(state_path, "r", encoding="utf-8"))

p0_keywords = [o for o in top20 if o["impr"] >= 20]
added = 0
for o in p0_keywords:
    task = f"关键词 '{o['keyword']}' GSC 排名 {o['pos']}, 曝光 {o['impr']}，优化现有内容或新建文章争取前10"
    existing = [t for t in state["next_iteration_focus"] if o["keyword"] in t.get("task", "")]
    if existing:
        print(f"  [SKIP] {o['keyword']}")
        continue
    state["next_iteration_focus"].append({
        "id": f"KW-{TODAY.replace('-','')}-mon{added:02d}",
        "task": task,
        "assigned_to": ["window2", "创作家"],
        "priority": "P0",
        "status": "pending",
        "source": f"gsc_weekly_opportunity_{TODAY}",
        "keyword": o["keyword"],
        "gsc_pos": o["pos"],
        "gsc_impr": o["impr"],
        "created_at": NOW,
    })
    added += 1

json.dump(state, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"[OK] state.json: {added} new keyword todos")

# 写日志
log_path = os.path.join(BASE, "window_logs", f"analyst_{TODAY}.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"\n\n---\n\n## 每周一 GSC 关键词筛选 - {NOW}\n\n")
    f.write(f"Total queries analyzed: {len(queries)}\n")
    f.write(f"Opportunities (pos 15-50, impr>=5): {len(opportunities)}\n")
    f.write(f"Top 20 written, P0 todos added: {added}\n")

print("DONE")
