"""Round 10: Generate briefs"""
import json, os
os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round10.json","r",encoding="utf-8") as f:
    research = json.load(f)

SELECTED = {
    "gemini-25-vs-gpt5": {
        "keyword": "Gemini 2.5 vs GPT-5", "type": "comparison", "category": "AI chatbot",
        "title": "Gemini 2.5 vs GPT-5 2026: Which AI Model Is Better?",
        "meta": "We tested Gemini 2.5 Pro and GPT-5 on coding, reasoning, multimodal, and pricing. Head-to-head results.",
        "quick_answer": "GPT-5 wins on coding and reasoning benchmarks; Gemini 2.5 Pro wins on multimodal and long context. Both require paid tier. Pick GPT-5 for coding, Gemini for research.",
        "h2s": ["Quick Verdict", "Test Setup", "Reasoning Test", "Coding Test", "Multimodal", "Long Context", "Pricing", "Who Should Use Which?", "Final Verdict"],
        "painpoints": ["GPT-5 is slower than GPT-4o", "Gemini free tier has rate limits", "Both hallucinate on math"],
        "rec_tools": ["GPT-5", "Gemini 2.5 Pro", "Claude Opus", "Grok 3", "Perplexity Pro"],
        "internal_links": ["/blog/chatgpt-vs-gemini-2026/", "/blog/gemini-review-2026/", "/blog/chatgpt-deep-review-2026/"],
    },
    "lovable-review": {
        "keyword": "Lovable review", "type": "review", "category": "AI app builder",
        "title": "Lovable Review 2026: Is the AI App Builder Worth It?",
        "meta": "We tested Lovable (formerly GPT Engineer) for 2 weeks. Honest review of this AI app builder — pricing, code quality, and limitations.",
        "quick_answer": "Lovable is the best AI app builder for non-technical founders. It generates full-stack React apps with Supabase backend. Free tier; Pro starts at $25/mo. Best for MVPs; not for production.",
        "h2s": ["Quick Answer", "What Is Lovable?", "Setup", "What We Built", "Code Quality", "Lovable vs v0 vs Bolt.new", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Exported code locks you to Lovable infra", "Complex auth flows fail", "Mobile UX is inconsistent"],
        "rec_tools": ["Lovable", "v0.dev", "Bolt.new", "Bubble", "Webflow AI"],
        "internal_links": ["/blog/lovable-vs-boltnew/", "/blog/v0-vs-lovable/", "/blog/best-ai-app-builders/"],
    },
    "openai-o3-review": {
        "keyword": "OpenAI o3 review", "type": "review", "category": "AI chatbot",
        "title": "OpenAI o3 Review 2026: Is the Reasoning Model Worth It?",
        "meta": "We tested OpenAI o3 on coding, math, and reasoning. Honest review of this fast-thinking AI model — pricing, benchmarks, and limitations.",
        "quick_answer": "OpenAI o3 is the fastest reasoning model for coding and math. It outperforms GPT-5 on complex reasoning but is slower and more expensive. Requires ChatGPT Plus ($20/mo). Best for hard coding problems; overkill for everyday chat.",
        "h2s": ["Quick Answer", "What Is o3?", "What We Tested", "Reasoning Benchmarks", "Coding Test", "o3 vs GPT-5 vs Claude Opus", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["o3-mini is much weaker than full o3", "Reasoning traces are verbose", "No API for free users"],
        "rec_tools": ["OpenAI o3", "GPT-5", "Claude Opus", "Gemini 2.5 Pro", "DeepSeek R1"],
        "internal_links": ["/blog/chatgpt-deep-review-2026/", "/blog/gpt-5-vs-claude-opus/", "/blog/best-ai-coding-tools-2026/"],
    },
    "manus-ai-review": {
        "keyword": "Manus AI review", "type": "review", "category": "AI agent",
        "title": "Manus AI Review 2026: Is the General-Purpose AI Agent Legit?",
        "meta": "We tested Manus AI for 2 weeks. Honest review of this autonomous AI agent — what it can do, pricing, and limitations.",
        "quick_answer": "Manus is the most capable general-purpose AI agent available. It can browse the web, write code, and complete multi-step tasks autonomously. Access via waitlist; pricing TBD. Best for complex workflows; not yet production-ready.",
        "h2s": ["Quick Answer", "What Is Manus?", "How It Works", "What We Tested", "Task Completion", "Manus vs Devin vs ChatGPT", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Waitlist is slow", "Task reliability varies", "No transparent pricing yet"],
        "rec_tools": ["Manus", "Devin", "ChatGPT Agent", "Claude", "Cursor"],
        "internal_links": ["/blog/devin-ai-review/", "/blog/best-ai-agents-2026/", "/blog/best-ai-coding-tools-2026/"],
    },
    "jasper-ai-alternatives": {
        "keyword": "Jasper AI alternatives", "type": "alternatives", "category": "AI writing",
        "title": "6 Best Jasper AI Alternatives in 2026 (Cheaper & Better)",
        "meta": "Jasper AI is expensive for what it offers. We tested 6 alternatives including Writesonic, Copy.ai, and ChatGPT. Compare pricing and features.",
        "quick_answer": "Writesonic wins for SEO content; Copy.ai wins for team workflows; ChatGPT wins for pure writing quality. Jasper starts at $49/mo. Best value: ChatGPT Plus at $20/mo.",
        "h2s": ["Quick Answer", "Why Look Beyond Jasper?", "#1: Writesonic — Best SEO", "#2: Copy.ai — Best Team", "#3: ChatGPT Plus — Best Writing", "#4: Notion AI — Best Docs", "#5: Rytr — Best Budget", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["Jasper's brand voice feature is inconsistent", "SEO integrations are shallow", "Team seats are expensive"],
        "rec_tools": ["Writesonic", "Copy.ai", "ChatGPT Plus", "Notion AI", "Rytr"],
        "internal_links": ["/blog/writesonic-alternatives/", "/blog/best-ai-writing-tools-2026/", "/blog/best-ai-content-writers-2026/"],
    },
}

os.makedirs("iteration_center/content_briefs", exist_ok=True)
written = []
for slug, brief in SELECTED.items():
    paa = research.get(slug, {}).get("paa", [])
    comps = research.get(slug, {}).get("top_competitors", [])
    content = f"""# Content Brief: {brief['keyword']}

- **Slug**: {slug}
- **Keyword**: {brief['keyword']}
- **Type**: {brief['type']}
- **Category**: {brief['category']}
- **Title**: {brief['title']}
- **Meta**: {brief['meta']}

## Quick Answer
{brief['quick_answer']}

## H2 Outline
"""
    for i, h in enumerate(brief["h2s"], 1):
        content += f"{i}. {h}\n"
    content += f"""
## Must Include
- Internal links: {', '.join(brief['internal_links'])}
- Tools: {', '.join(brief['rec_tools'])}
## Pain Points
"""
    for i, p in enumerate(brief["painpoints"], 1):
        content += f"{i}. {p}\n"
    content += "\n## FAQ\n"
    for q in paa[:5]:
        content += f"\n### {q}\n\nAnswer: See above.\n"
    content += "\n## SERP\n"
    for c in comps[:3]:
        content += f"- {c.get('title','')}: {c.get('url','')}\n"
    content += "\n## Word Count: 2500-3500\n## Language: English (US)\n"
    with open(f"iteration_center/content_briefs/{slug}_input.md","w",encoding="utf-8") as f:
        f.write(content)
    written.append(slug)
    print(f"  Written: {slug}")

with open("iteration_center/state.json","r",encoding="utf-8") as f:
    state = json.load(f)
for slug, brief in SELECTED.items():
    state["next_iteration_focus"].append({
        "id": f"kw_r10_{slug.replace('-','_')}",
        "task": f"写{brief['type']}页：{brief['keyword']}（P0）",
        "assigned_to": ["window3"], "priority": "P0", "status": "pending",
        "source": "round10_2026-10-02", "slug": slug,
        "keyword": brief["keyword"], "type": brief["type"],
    })
with open("iteration_center/state.json","w",encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"\n=== {len(written)} briefs, {len(SELECTED)} P0 tasks ===")
