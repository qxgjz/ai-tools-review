"""Round 9: Generate briefs for new gap keywords"""
import json, os

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round9.json","r",encoding="utf-8") as f:
    research = json.load(f)

SELECTED = {
    "chatgpt-vs-grok": {
        "keyword": "ChatGPT vs Grok", "type": "comparison", "category": "AI chatbot",
        "title": "ChatGPT vs Grok 2026: Which AI Chatbot Is Better?",
        "meta": "We tested ChatGPT and Grok 3 on coding, writing, real-time data, and personality. Head-to-head results with pricing.",
        "quick_answer": "ChatGPT wins on coding accuracy and plugin ecosystem; Grok wins on real-time X (Twitter) data and edgy personality. ChatGPT Plus is $20/mo; Grok Premium is $30/mo. Pick ChatGPT for productivity, Grok for news/social monitoring.",
        "h2s": ["Quick Verdict", "Test Methodology", "Coding Test", "Real-Time Data", "Writing Quality", "Personality & Tone", "Pricing", "Who Should Use ChatGPT?", "Who Should Use Grok?", "Final Verdict"],
        "painpoints": ["ChatGPT's real-time data lags behind", "Grok hallucinates on non-X topics", "Both tools have usage limits on free tiers"],
        "rec_tools": ["ChatGPT Plus", "Grok 3", "Claude Pro", "Perplexity Pro", "Gemini Advanced"],
        "internal_links": ["/blog/chatgpt-deep-review-2026/", "/blog/chatgpt-alternatives-2026/", "/blog/perplexity-vs-grok/"],
    },
    "synthesia-alternatives": {
        "keyword": "Synthesia alternatives", "type": "alternatives", "category": "AI video generation",
        "title": "6 Best Synthesia Alternatives in 2026 (Cheaper & More Realistic)",
        "meta": "Synthesia is pricey. We tested 6 alternatives including HeyGen, Colossyan, and Elai. Compare pricing, avatars, and languages.",
        "quick_answer": "HeyGen wins for realistic avatars; Colossyan wins for budget; Elai wins for multi-language. Synthesia starts at $22/mo. Best value: Colossyan at $30/mo with similar quality.",
        "h2s": ["Quick Answer", "Why Look Beyond Synthesia?", "#1: HeyGen — Best Avatars", "#2: Colossyan — Best Budget", "#3: Elai.io — Best Languages", "#4: D-ID — Best API", "#5: Arcads — Best Ads", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["Synthesia avatars look stiff in close-ups", "Text-to-speech accents are inconsistent", "Premium avatars cost extra credits"],
        "rec_tools": ["HeyGen", "Colossyan", "Elai.io", "D-ID", "Arcads"],
        "internal_links": ["/blog/synthesia-vs-heygen/", "/blog/heygen-alternatives/", "/blog/best-ai-video-generators/"],
    },
    "grok-3-review": {
        "keyword": "Grok 3 review", "type": "review", "category": "AI chatbot",
        "title": "Grok 3 Review 2026: Is xAI's AI Chatbot Worth It?",
        "meta": "We tested Grok 3 for 2 weeks. Honest review of xAI's AI chatbot — real-time search, coding, personality, and pricing.",
        "quick_answer": "Grok 3 is the best AI chatbot for real-time X (Twitter) data and edgy humor. It outperforms ChatGPT on coding benchmarks but lacks plugin ecosystem. Grok Premium is $30/mo (requires X Premium+). Best for news junkies; not for enterprise.",
        "h2s": ["Quick Answer", "What Is Grok 3?", "Setup", "What We Tested", "Real-Time Search", "Coding Test", "Grok vs ChatGPT", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Requires X Premium+ subscription", "No mobile app for iOS outside US", "Hallucinates on niche technical topics"],
        "rec_tools": ["Grok 3", "ChatGPT Plus", "Claude Pro", "Perplexity Pro", "Gemini Advanced"],
        "internal_links": ["/blog/perplexity-vs-grok/", "/blog/chatgpt-vs-grok/", "/blog/chatgpt-alternatives-2026/"],
    },
    "notebooklm-review": {
        "keyword": "NotebookLM review", "type": "review", "category": "AI research",
        "title": "Google NotebookLM Review 2026: Is It the Best AI Research Tool?",
        "meta": "We tested Google NotebookLM on research papers, PDFs, and long documents. Honest review — features, pricing, and limitations.",
        "quick_answer": "NotebookLM is the best free AI tool for research and document analysis. It lets you upload PDFs, notes, and links, then asks questions grounded in your sources. Completely free. Best for students and researchers; not for creative writing.",
        "h2s": ["Quick Answer", "What Is NotebookLM?", "Setup", "What We Tested", "Source Grounding", "Audio Overview Feature", "NotebookLM vs ChatGPT", "Pricing (Free)", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Only supports text sources (no images yet)", "Upload limit of 500 notes", "No API access"],
        "rec_tools": ["NotebookLM", "ChatGPT Plus", "Claude Pro", "Perplexity Pro", "Obsidian AI"],
        "internal_links": ["/blog/notion-ai-vs-obsidian-ai/", "/blog/best-ai-research-tools-2026/", "/blog/best-ai-note-taking-tools-2026/"],
    },
    "kimi-review": {
        "keyword": "Kimi AI review", "type": "review", "category": "AI chatbot",
        "title": "Kimi AI Review 2026: Is Moonshot's Chatbot Worth Using?",
        "meta": "We tested Kimi (Moonshot AI) on long document analysis and coding. Honest review of this Chinese AI chatbot — features, pricing, and limitations.",
        "quick_answer": "Kimi (Moonshot AI) offers the best free long-context analysis (up to 2M tokens) among Chinese chatbots. It excels at PDF summarization but lacks Western app integrations. Free tier available; paid starts at $5/mo. Best for long-document work; weaker for everyday chat.",
        "h2s": ["Quick Answer", "What Is Kimi?", "Setup & Access", "What We Tested", "Long Context Test", "Coding Test", "Kimi vs ChatGPT vs Claude", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["English response quality lags behind Claude/GPT", "Data privacy concerns for enterprise", "No official US mobile app"],
        "rec_tools": ["Kimi", "ChatGPT Plus", "Claude Pro", "Qwen", "DeepSeek"],
        "internal_links": ["/blog/best-free-ai-tools-2026/", "/blog/chatgpt-alternatives-2026/", "/blog/best-ai-chatbots-2026/"],
    },
}

os.makedirs("iteration_center/content_briefs", exist_ok=True)
written = []

for slug, brief in SELECTED.items():
    paa = research.get(slug, {}).get("paa", [])
    competitors = research.get(slug, {}).get("top_competitors", [])
    content = f"""# Content Brief: {brief['keyword']}

- **Slug**: {slug}
- **Target Keyword**: {brief['keyword']}
- **Type**: {brief['type']}
- **Category**: {brief['category']}
- **KD**: low
- **Title**: {brief['title']}
- **Meta**: {brief['meta']}

## Quick Answer
{brief['quick_answer']}

## Key Takeaways
1. {brief['quick_answer'].split('.')[0]}.
2. Real test results with pricing.
3. Clear recommendation by use case.

## H2 Outline
"""
    for i, h2 in enumerate(brief["h2s"], 1):
        content += f"{i}. {h2}\n"
    content += f"""
## Must Include
- Comparison table, 3+ A vs B conclusions, How We Tested
- Internal links: {', '.join(brief['internal_links'])}
- Recommended tools: {', '.join(brief['rec_tools'])}

## Pain Points
"""
    for i, p in enumerate(brief["painpoints"], 1):
        content += f"{i}. {p}\n"
    content += "\n## FAQ (from PAA)\n"
    for q in paa[:5]:
        content += f"\n### {q}\n\nAnswer: See detailed comparison above.\n"
    content += "\n## Competitor SERP\n"
    for c in competitors[:3]:
        content += f"- {c.get('title','')}: {c.get('url','')}\n"
    content += "\n## Word Count: 2500-3500\n## Language: 100% English (US)\n"
    with open(f"iteration_center/content_briefs/{slug}_input.md", "w", encoding="utf-8") as f:
        f.write(content)
    written.append(slug)
    print(f"  Written: {slug}_input.md")

with open("iteration_center/state.json","r",encoding="utf-8") as f:
    state = json.load(f)
new_tasks = []
for slug, brief in SELECTED.items():
    task_id = f"kw_r9_{slug.replace('-','_')}"
    state["next_iteration_focus"].append({
        "id": task_id, "task": f"写{brief['type']}页：{brief['keyword']}（P0）",
        "assigned_to": ["window3"], "priority": "P0", "status": "pending",
        "source": "keyword_research_round9_2026-10-02",
        "slug": slug, "keyword": brief["keyword"], "type": brief["type"],
    })
    new_tasks.append(task_id)
with open("iteration_center/state.json","w",encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"\n=== {len(written)} briefs, {len(new_tasks)} new P0 tasks ===")
for t in new_tasks:
    print(f"  + {t}")
