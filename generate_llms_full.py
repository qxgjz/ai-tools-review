import json
import os

# 读取数据文件
with open('data/tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

with open('data/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

with open('data/alternatives.json', 'r', encoding='utf-8') as f:
    alternatives = json.load(f)

# 生成llms-full.txt
output = []

# 头部
output.append("# llms-full.txt - AIToolCrux")
output.append("# Full content index for AI crawlers and LLM systems")
output.append("# https://www.aitoolcrux.com")
output.append(f"# Generated: 2026-09-11")
output.append(f"# Total pages: {len(tools) + len(posts) + len(alternatives) + 17 + 10}")
output.append("")

# 首页内容
output.append("=" * 80)
output.append("## PAGE: Homepage")
output.append("URL: https://www.aitoolcrux.com/")
output.append("Title: Best AI Tools 2026: Expert Reviews & Comparisons | AIToolCrux")
output.append("")
output.append("AIToolCrux is the leading platform for expert AI tool reviews, comparisons, and recommendations.")
output.append("We test 533+ AI tools across 17 categories with hands-on experience and honest ratings.")
output.append("")
output.append("Top Categories: AI Chat, Image Generation, Video, Writing, Audio, Coding, Productivity, Design, AI Agents")
output.append("Top Tools: ChatGPT, Claude, Gemini, Midjourney, GitHub Copilot, Cursor, Jasper, Perplexity")
output.append("")

# 方法论页面
output.append("=" * 80)
output.append("## PAGE: Methodology")
output.append("URL: https://www.aitoolcrux.com/methodology")
output.append("Title: Our Review Methodology | AIToolCrux")
output.append("")
output.append("We use a six-dimension scoring system for every AI tool:")
output.append("1. Features (25%): Breadth and depth of functionality")
output.append("2. Ease of Use (20%): Learning curve and user experience")
output.append("3. Performance (20%): Speed, accuracy, and reliability")
output.append("4. Value for Money (15%): Pricing relative to capabilities")
output.append("5. Support (10%): Customer service and documentation quality")
output.append("6. Innovation (10%): Unique features and advancement")
output.append("")
output.append("All tools are tested hands-on by our editorial team. Ratings are updated regularly.")
output.append("Affiliate relationships do not influence ratings or rankings.")
output.append("")

# 分类页面
categories = {}
for tool in tools:
    cat = tool.get('category', 'other')
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(tool)

output.append("=" * 80)
output.append("## CATEGORY PAGES")
output.append("")

for cat, cat_tools in sorted(categories.items()):
    output.append("-" * 60)
    output.append(f"### Category: {cat.title()}")
    output.append(f"URL: https://www.aitoolcrux.com/category/{cat}")
    output.append(f"Tools in category: {len(cat_tools)}")
    output.append("")
    output.append(f"Top rated {cat} AI tools:")
    for t in sorted(cat_tools, key=lambda x: x.get('rating', 0), reverse=True)[:10]:
        output.append(f"- {t['name']}: {t.get('rating', 'N/A')}/10 - {t.get('description', '')[:100]}")
    output.append("")

# 工具详情页（Top 50详细，其余简要）
output.append("=" * 80)
output.append("## TOOL DETAIL PAGES")
output.append("")

sorted_tools = sorted(tools, key=lambda x: x.get('rating', 0), reverse=True)

for i, tool in enumerate(sorted_tools):
    output.append("-" * 60)
    output.append(f"### Tool: {tool['name']}")
    output.append(f"URL: https://www.aitoolcrux.com/tools/{tool['slug']}")
    output.append(f"Rating: {tool.get('rating', 'N/A')}/10")
    output.append(f"Category: {tool.get('category', 'N/A')}")
    output.append(f"Pricing: {tool.get('pricing', 'N/A')}")
    output.append("")
    output.append(f"Description: {tool.get('description', '')}")
    output.append("")
    
    # 只对Top 50显示详细信息
    if i < 50:
        if tool.get('keyFeatures'):
            output.append("Key Features:")
            for feat in tool.get('keyFeatures', [])[:8]:
                output.append(f"- {feat}")
            output.append("")
        
        if tool.get('pros'):
            output.append("Pros:")
            for pro in tool.get('pros', [])[:5]:
                output.append(f"- {pro}")
            output.append("")
        
        if tool.get('cons'):
            output.append("Cons:")
            for con in tool.get('cons', [])[:5]:
                output.append(f"- {con}")
            output.append("")
        
        if tool.get('useCases'):
            output.append("Use Cases:")
            for uc in tool.get('useCases', [])[:5]:
                output.append(f"- {uc}")
            output.append("")
    else:
        output.append("[Brief entry - full details available on page]")
        output.append("")

# 文章页面
output.append("=" * 80)
output.append("## ARTICLE / BLOG PAGES")
output.append("")

for post in posts:
    output.append("-" * 60)
    output.append(f"### Article: {post.get('title', 'Untitled')}")
    output.append(f"URL: https://www.aitoolcrux.com/blog/{post.get('slug', '')}")
    output.append(f"Date: {post.get('date', 'N/A')}")
    output.append(f"Author: {post.get('author', 'AIToolCrux Editorial Team')}")
    output.append("")
    output.append(f"Excerpt: {post.get('excerpt', post.get('description', ''))[:200]}")
    output.append("")
    
    # 显示文章内容的前500字符
    content = post.get('content', '')
    if content:
        # 移除HTML标签
        import re
        clean_content = re.sub(r'<[^>]+>', '', content)
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        output.append(f"Content preview: {clean_content[:500]}...")
        output.append("")
    
    if post.get('faqs'):
        output.append("FAQ:")
        for faq in post.get('faqs', [])[:3]:
            output.append(f"Q: {faq.get('question', '')}")
            output.append(f"A: {faq.get('answer', '')[:100]}")
        output.append("")

# 替代方案页面
output.append("=" * 80)
output.append("## ALTERNATIVE GUIDE PAGES")
output.append("")

for alt in alternatives:
    output.append("-" * 60)
    output.append(f"### Alternative Guide: {alt.get('title', '')}")
    output.append(f"URL: https://www.aitoolcrux.com/alternatives/{alt.get('slug', '')}")
    output.append(f"Target tool: {alt.get('targetTool', '')}")
    output.append("")
    output.append(f"Description: {alt.get('description', '')}")
    output.append("")
    output.append("Top alternatives:")
    for a in alt.get('alternatives', [])[:10]:
        output.append(f"- {a.get('name', '')}: {a.get('rating', 'N/A')}/10 - Best for: {a.get('reason', '')[:80]}")
    output.append("")
    
    if alt.get('faq'):
        output.append("FAQ:")
        for faq in alt.get('faq', [])[:3]:
            output.append(f"Q: {faq.get('question', '')}")
            output.append(f"A: {faq.get('answer', '')[:100]}")
        output.append("")

# 底部
output.append("=" * 80)
output.append("## END OF CONTENT INDEX")
output.append("")
output.append("For full content of any page, visit the corresponding URL.")
output.append("This file is generated automatically and updated regularly.")
output.append("Last generated: 2026-09-11")

# 写入文件
content = '\n'.join(output)
with open('public/llms-full.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"llms-full.txt generated successfully!")
print(f"File size: {len(content)} bytes ({len(content)/1024:.1f} KB)")
print(f"Total lines: {len(output)}")
print(f"Tools included: {len(tools)}")
print(f"Articles included: {len(posts)}")
print(f"Alternatives included: {len(alternatives)}")
print(f"Categories: {len(categories)}")
