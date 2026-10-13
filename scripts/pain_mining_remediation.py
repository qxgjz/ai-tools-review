#!/usr/bin/env python3
"""痛点挖掘补救: 补充Product Hunt+更多聚类, 修正优先级, 追加到已有结果"""
import requests, json, os
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
today = now.strftime("%Y-%m-%d")
now_str = now.strftime("%Y-%m-%d %H:%M:%S JST")

SERPER_KEY = "db3bbe31d1470d3d4358896851c04030d2e76a6e"
SERPER_URL = "https://google.serper.dev/search"
HEADERS = {"X-API-KEY": SERPER_KEY, "Content-Type": "application/json"}

PROJECT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"
PAIN_MD = os.path.join(PROJECT, "iteration_center", "pain_points.md")
STATE_PATH = os.path.join(PROJECT, "iteration_center", "state.json")

def serper(q, num=10):
    try:
        r = requests.post(SERPER_URL, headers=HEADERS, json={"q": q, "num": num}, timeout=20)
        return r.json().get("organic", [])
    except Exception as e:
        print(f"  [ERR] {q[:50]}: {e}")
        return []

# === 补充搜索: Product Hunt + AI编码 + AI图像 + 更多Reddit ===
extra_queries = [
    ("Product Hunt", 'site:producthunt.com/posts AI "review" OR "comment" OR "feedback"'),
    ("Product Hunt2", 'site:producthunt.com "AI" "not worth" OR "disappointing" OR "overhyped"'),
    ("Reddit AI编码", 'site:reddit.com cursor OR windsurf OR "ai coding" frustrating OR "not worth" OR buggy OR expensive'),
    ("Reddit AI图像", 'site:reddit.com "ai image" OR dalle OR "stable diffusion" consistency OR "not good enough" OR frustrating'),
    ("Reddit AI SEO", 'site:reddit.com "AI SEO" OR "ai content" google penalty OR "not ranking" OR waste'),
    ("HN AI编码", 'site:news.ycombinator.com cursor OR copilot OR "ai coding" disappointing OR "not as good" OR overhyped'),
]

extra_comments = []
for label, q in extra_queries:
    print(f"=== {label} ===")
    results = serper(q, num=8)
    for r in results:
        snippet = r.get("snippet", "")
        if snippet and len(snippet) > 30:
            src = label.replace("2","").split()[0]
            extra_comments.append({"source": label, "src_group": src, "url": r.get("link",""), "title": r.get("title",""), "quote": snippet})
    print(f"  got {len(results)} results")

print(f"\n=== Extra comments: {len(extra_comments)} ===")

# === 新增P1聚类定义 ===
new_clusters = [
    {
        "theme": "AI编码工具(Cursor/Copilot)实际效果不如宣传",
        "keywords": ["cursor", "windsurf", "copilot", "coding tool", "code generation", "ai coding"],
        "target": "AI编码工具",
        "article": "AI Coding Tools in 2026: Why Cursor and Copilot Still Can't Replace Senior Devs",
        "search_kw": "ai coding tools worth it cursor copilot 2026",
        "priority": "P1"
    },
    {
        "theme": "AI生成内容被Google惩罚/不排名",
        "keywords": ["ai seo", "ai content", "google penalty", "not ranking", "ai content penalty"],
        "target": "AI SEO/内容",
        "article": "Does AI Content Get Penalized by Google in 2026? What Actually Happens",
        "search_kw": "ai content google penalty 2026 does it rank",
        "priority": "P1"
    },
    {
        "theme": "AI图像生成一致性差/商用不可靠",
        "keywords": ["ai image", "dalle", "stable diffusion", "consistency", "image generator"],
        "target": "AI图像生成",
        "article": "AI Image Generators Still Can't Do Consistency in 2026 (And Workarounds That Work)",
        "search_kw": "ai image generator consistency problem 2026",
        "priority": "P1"
    },
]

# 分配补充评论到新聚类
for cl in new_clusters:
    cl["items"] = []
    for c in extra_comments:
        text = (c["title"] + " " + c["quote"]).lower()
        if any(kw in text for kw in cl["keywords"]):
            cl["items"].append(c)

# 搜索意图验证
for cl in new_clusters:
    if cl["items"]:
        results = serper(cl["search_kw"], num=10)
        cl["verified"] = len(results) >= 5
        cl["serp_count"] = len(results)
        domains = set()
        for r in results[:5]:
            try: domains.add(r.get("link","").split("/")[2])
            except: pass
        cl["competition"] = "High" if len(domains)<=2 else ("Medium" if len(domains)<=4 else "Low")
        cl["top_competitors"] = [r.get("link","")[:60] for r in results[:3]]
    else:
        cl["verified"] = False
        cl["competition"] = "N/A"
        cl["top_competitors"] = []
    print(f"  {cl['theme'][:40]}: items={len(cl['items'])}, verified={cl.get('verified')}, comp={cl.get('competition')}")

# === 追加到pain_points.md ===
with open(PAIN_MD, "r", encoding="utf-8") as f:
    existing = f.read()

# 在统计汇总前插入新P1
insert_point = existing.find("---\n\n## 统计汇总")
if insert_point == -1:
    insert_point = len(existing)

new_section = "\n## 补充P1痛点（增量搜索追加）\n\n"
valid_new = [c for c in new_clusters if c["items"]]
for i, cl in enumerate(valid_new, 1):
    src_groups = sorted(set(c["src_group"] for c in cl["items"]))
    new_section += f"### [P1] #{i} {cl['theme']}\n\n"
    new_section += f"- **目标工具/主题**: {cl['target']}\n"
    new_section += f"- **建议文章标题**: {cl['article']}\n"
    new_section += f"- **证据数**: {len(cl['items'])}条，来自{len(src_groups)}个来源（{', '.join(src_groups)}）\n"
    new_section += f"- **搜索意图验证**: {'✅ 通过' if cl['verified'] else '❌'}（SERP={cl.get('serp_count',0)}）\n"
    new_section += f"- **SERP竞争度**: {cl['competition']}\n"
    new_section += f"- **我们是否已覆盖**: ❌ 未覆盖\n\n"
    new_section += "| # | 来源 | URL | 用户原话 |\n|---|------|-----|---------|\n"
    for j, item in enumerate(cl["items"][:4], 1):
        quote = item["quote"].replace("|","\\|").replace("\n"," ")[:180]
        new_section += f"| {j} | {item['src_group']} | {item['url'][:70]} | {quote} |\n"
    new_section += "\n"

updated = existing[:insert_point] + new_section + existing[insert_point:]

# 更新统计
old_p1 = "P1 | 2"  # 之前是2个P1
updated = updated.replace("| P1 | 2 |", f"| P1 | {2+len(valid_new)} |")
updated = updated.replace(f"| 有效聚类痛点 | 4 |", f"| 有效聚类痛点 | {4+len(valid_new)} |")
updated = updated.replace(f"| 抓取评论数 | 72 |", f"| 抓取评论数 | {72+len(extra_comments)} |")
updated = updated.replace(f"| 抓取来源数 | 5 |", f"| 抓取来源数 | 6 |")

with open(PAIN_MD, "w", encoding="utf-8") as f:
    f.write(updated)
print(f"\n=== pain_points.md updated: {os.path.getsize(PAIN_MD)} bytes ===")

# === 修正: 把AI视频从P1提升为P0 (覆盖检查误判) ===
# 追加P0待办到state.json
with open(STATE_PATH, "r", encoding="utf-8") as f:
    state = json.load(f)

# AI视频生成credits - 提升为P0
video_todo = {
    "id": f"PAIN-P0-{today}-VIDEO",
    "priority": "P0",
    "task": "用户痛点【AI视频生成credits烧太快/性价比低】，建议写文章【Why AI Video Generators Burn Through Credits Fast (And Free Alternatives in 2026)】，正文必须引用用户原话做H2/FAQ，SERP竞争度=Medium",
    "assigned_to": ["window2", "创作家"],
    "source": f"pain_point_mining_{today}",
    "verified": True,
    "serp_competition": "Medium",
    "sources_count": 2,
    "evidence_count": 4,
    "search_keyword": "ai video generator credits expensive alternative 2026",
    "note": "覆盖检查修正: best-ai-video-editors不等于视频生成定价文章，实际未覆盖",
    "status": "pending",
    "created": now_str
}
state["next_iteration_focus"].append(video_todo)

# 新增P1待办
for cl in valid_new:
    todo = {
        "id": f"PAIN-P1-{today}-{abs(hash(cl['theme']))%100000}",
        "priority": "P1",
        "task": f"用户痛点【{cl['theme']}】，建议写文章【{cl['article']}】",
        "assigned_to": ["window2", "创作家"],
        "source": f"pain_point_mining_{today}",
        "verified": cl.get("verified", False),
        "serp_competition": cl.get("competition", "N/A"),
        "sources_count": len(set(c["src_group"] for c in cl["items"])),
        "status": "pending",
        "created": now_str
    }
    state["next_iteration_focus"].append(todo)

state["last_updated"] = now_str
with open(STATE_PATH, "w", encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

total_new = 1 + len(valid_new)
print(f"state.json: +1 P0 (video修正) + {len(valid_new)} P1 = {total_new} todos added")
print(f"Total P0 now: 3, Total P1 now: {2+len(valid_new)}")

print("\n" + "="*60)
print("REMEDIATION SUMMARY")
print("="*60)
print(f"Extra sources added: Product Hunt, more Reddit/HN")
print(f"Extra comments: {len(extra_comments)}")
print(f"New P1 clusters: {len(valid_new)}")
print(f"P0 corrected: AI video (was P1 due to false coverage check)")
print(f"Final: 3 P0 + {2+len(valid_new)} P1")
print(f"pain_points.md: {os.path.getsize(PAIN_MD)} bytes")
