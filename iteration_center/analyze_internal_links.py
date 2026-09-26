"""
内链分析 + Quick Answer/Key Takeaways缺口分析
输出：
1. internal_link_gaps.md - 入链最少的工具页Top20
2. qa_takeaways_gaps.md - Quick Answer/Key Takeaways缺口清单
"""
import json
import os
import re
from collections import defaultdict

PROJECT_ROOT = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review"

# 读取数据
with open(os.path.join(PROJECT_ROOT, "data", "tools.json"), "r", encoding="utf-8") as f:
    tools = json.load(f)

with open(os.path.join(PROJECT_ROOT, "data", "posts.json"), "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"工具总数: {len(tools)}")
print(f"文章总数: {len(posts)}")

# ============================================================
# 1. 内链分析
# ============================================================
print("\n=== 开始内链分析 ===")

# 统计每个工具页的入链
inbound_count = defaultdict(int)
inbound_sources = defaultdict(list)

# 从文章中找内链
for post in posts:
    post_slug = post.get("slug", "")
    content = post.get("content", "") or post.get("body", "") or ""
    
    # 找所有指向/tools/xxx的链接
    links = re.findall(r'/tools/([a-zA-Z0-9\-_]+)', content)
    for tool_slug in links:
        inbound_count[tool_slug] += 1
        if post_slug not in inbound_sources[tool_slug]:
            inbound_sources[tool_slug].append(post_slug)

# 也从工具页之间找互链（如果有的话）
for tool in tools:
    tool_slug = tool.get("slug", "")
    # 工具详情页通常不会互相链接，这里只统计文章内链

# 构建工具slug到名称的映射
tool_slug_map = {}
for tool in tools:
    slug = tool.get("slug", "")
    name = tool.get("name", slug)
    tool_slug_map[slug] = name

# 找入链最少的Top20工具页
# 只考虑有名有姓的工具页，排除空slug
tool_slugs_with_names = [(slug, name) for slug, name in tool_slug_map.items() if slug]

# 按入链数排序（升序）
sorted_by_links = sorted(tool_slugs_with_names, key=lambda x: inbound_count.get(x[0], 0))

print(f"有入链的工具数: {len(inbound_count)}")
print(f"零入链的工具数: {sum(1 for slug in tool_slugs_with_names if inbound_count.get(slug, 0) == 0)}")

# 取Top20入链最少的
bottom20 = sorted_by_links[:20]

# 写内链分析报告
report_path = os.path.join(PROJECT_ROOT, "iteration_center", "internal_link_gaps.md")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("# 内链缺口分析报告\n\n")
    f.write(f"生成时间: 2026-09-16\n\n")
    f.write("## 总览\n\n")
    f.write(f"- 工具总数: {len(tools)}\n")
    f.write(f"- 有入链的工具数: {len(inbound_count)}\n")
    f.write(f"- 零入链的工具数: {sum(1 for slug in tool_slugs_with_names if inbound_count.get(slug, 0) == 0)}\n\n")
    
    f.write("## 入链最少的Top20工具页\n\n")
    f.write("| 排名 | 工具名称 | 工具URL | 当前入链数 | 建议加内链的位置 |\n")
    f.write("|:---:|---------|---------|:--------:|----------------|\n")
    
    for i, (slug, name) in enumerate(bottom20, 1):
        count = inbound_count.get(slug, 0)
        url = f"/tools/{slug}"
        
        # 建议加内链的位置：找同分类的文章
        # 简化建议：根据工具名的关键词，建议加到相关review文章或分类页
        suggestion = f"加到相关review文章、{name} alternatives页、分类页"
        
        f.write(f"| {i} | {name} | {url} | {count} | {suggestion} |\n")
    
    f.write("\n## 优化建议\n\n")
    f.write("### P0（本周做）\n")
    f.write("1. 给排名前50但零入链的工具页加内链\n")
    f.write("2. 从高流量文章（/compare、/blog/openai_astra_review）往重要工具页加内链\n")
    f.write("3. 在每篇文章的\"Related Tools\"板块加3-5个相关工具内链\n\n")
    
    f.write("### P1（下周做）\n")
    f.write("1. 建立工具页之间的互链（Top 10工具页互相链接）\n")
    f.write("2. 分类页底部加\"Recently Reviewed Tools\"内链模块\n")
    f.write("3. 检查锚文本是否描述性，不要全用\"click here\"\n")

print(f"内链分析报告已写入: {report_path}")

# ============================================================
# 2. Quick Answer / Key Takeaways 缺口分析
# ============================================================
print("\n=== 开始Quick Answer/Key Takeaways缺口分析 ===")

missing_qa = []
missing_kt = []
has_both = []

for post in posts:
    post_slug = post.get("slug", "")
    title = post.get("title", "")
    content = post.get("content", "") or post.get("body", "") or ""
    
    has_qa = bool(re.search(r'quick answer|quickanswer|## Quick Answer|### Quick Answer', content, re.IGNORECASE))
    has_kt = bool(re.search(r'key takeaways|keytakeaways|## Key Takeaways|### Key Takeaways|## Takeaways', content, re.IGNORECASE))
    
    if not has_qa:
        missing_qa.append({
            "slug": post_slug,
            "title": title,
            "url": f"/blog/{post_slug}"
        })
    
    if not has_kt:
        missing_kt.append({
            "slug": post_slug,
            "title": title,
            "url": f"/blog/{post_slug}"
        })
    
    if has_qa and has_kt:
        has_both.append(post_slug)

print(f"有Quick Answer: {len(posts) - len(missing_qa)}")
print(f"缺Quick Answer: {len(missing_qa)}")
print(f"有Key Takeaways: {len(posts) - len(missing_kt)}")
print(f"缺Key Takeaways: {len(missing_kt)}")
print(f"两个都有: {len(has_both)}")

# 写缺口分析报告
report_path2 = os.path.join(PROJECT_ROOT, "iteration_center", "qa_takeaways_gaps.md")
with open(report_path2, "w", encoding="utf-8") as f:
    f.write("# Quick Answer / Key Takeaways 缺口分析\n\n")
    f.write(f"生成时间: 2026-09-16\n\n")
    
    f.write("## 总览\n\n")
    f.write(f"- 文章总数: {len(posts)}\n")
    f.write(f"- 有Quick Answer: {len(posts) - len(missing_qa)} 篇\n")
    f.write(f"- 缺Quick Answer: {len(missing_qa)} 篇\n")
    f.write(f"- 有Key Takeaways: {len(posts) - len(missing_kt)} 篇\n")
    f.write(f"- 缺Key Takeaways: {len(missing_kt)} 篇\n")
    f.write(f"- 两个都有: {len(has_both)} 篇\n\n")
    
    f.write("## 优化优先级排序\n\n")
    f.write("### P0（本周必须补）- 排名前50的文章优先\n")
    f.write("（根据GSC数据，以下文章已经有排名，补Quick Answer/Key Takeaways提升最快）\n\n")
    
    # 从GSC数据知道排名好的文章
    top_ranked_posts = [
        ("stable-diffusion-review-2026", "Stable Diffusion Review 2026", 5.4),
        ("dify_ai_review", "Dify AI Review", 5.5),
        ("cursor_ai_review", "Cursor AI Review", 7.4),
        ("midjourney-v7-review", "Midjourney V7 Review", 7.5),
        ("gemini_38_flash_review", "Gemini 3.8 Flash Review", 7.6),
        ("openai_astra_review", "OpenAI Astra Review", 11.2),
        ("suno-review-2026", "Suno Review 2026", 11.5),
    ]
    
    f.write("| 优先级 | 文章标题 | 排名 | 缺Quick Answer | 缺Key Takeaways |\n")
    f.write("|:---:|---------|:---:|:---:|:---:|\n")
    
    for slug, title, rank in top_ranked_posts:
        has_qa = not any(p["slug"] == slug for p in missing_qa)
        has_kt = not any(p["slug"] == slug for p in missing_kt)
        qa_status = "❌" if not has_qa else "✅"
        kt_status = "❌" if not has_kt else "✅"
        f.write(f"| P0 | {title} | {rank} | {qa_status} | {kt_status} |\n")
    
    f.write("\n### P1（下周补）- 其他review类文章\n")
    f.write("| 文章标题 | 缺Quick Answer | 缺Key Takeaways |\n")
    f.write("|---------|:---:|:---:|\n")
    
    # 列出其他缺的文章（前20个）
    other_missing = [p for p in missing_qa if p["slug"] not in [s for s, _, _ in top_ranked_posts]]
    for post in other_missing[:20]:
        title = post["title"][:60]  # 截断长标题
        has_kt = not any(p["slug"] == post["slug"] for p in missing_kt)
        kt_status = "❌" if not has_kt else "✅"
        f.write(f"| {title} | ❌ | {kt_status} |\n")
    
    f.write(f"\n...还有 {len(other_missing) - 20} 篇\n\n")
    
    f.write("## 给窗口3的优化顺序清单\n\n")
    f.write("### 第一步：补Top 7排名好的文章（P0）\n")
    for slug, title, rank in top_ranked_posts:
        f.write(f"1. /blog/{slug} — {title}（当前排名{rank}）\n")
    
    f.write("\n### 第二步：补其他review文章（P1）\n")
    f.write("按发布时间倒序，新发布的文章优先补，因为新文章还在沙盒期，加Quick Answer有助于快速收录\n\n")
    
    f.write("### 模板参考\n")
    f.write("```markdown\n## Quick Answer\n[2-3句话直接回答核心问题]\n\n## Key Takeaways\n- [要点1]\n- [要点2]\n- [要点3]\n```\n")

print(f"缺口分析报告已写入: {report_path2}")
print("\n=== 分析完成 ===")
