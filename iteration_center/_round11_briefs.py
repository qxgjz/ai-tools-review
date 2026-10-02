"""Round 11: Generate briefs"""
import json, os
os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round11.json","r",encoding="utf-8") as f:
    research = json.load(f)

SELECTED = {
    "grok-vs-gemini": {
        "keyword": "Grok vs Gemini", "type": "comparison", "category": "AI chatbot",
        "title": "Grok vs Gemini 2026: Which AI Assistant Is Better?",
        "meta": "We tested Grok 3 and Gemini 2.5 Pro on real-time search, coding, and multimodal. Head-to-head results with pricing.",
        "quick_answer": "Gemini wins on multimodal and long context; Grok wins on real-time X (Twitter) data. Gemini Advanced is $19.99/mo; Grok Premium is $30/mo. Pick Gemini for research, Grok for news.",
        "h2s": ["Quick Verdict", "Test Setup", "Real-Time Search", "Multimodal", "Coding", "Pricing", "Who Should Use Which?", "Final Verdict"],
        "painpoints": ["Grok has no desktop app", "Gemini free tier has daily limits", "Both struggle with enterprise privacy"],
        "rec_tools": ["Grok 3", "Gemini 2.5 Pro", "ChatGPT Plus", "Claude", "Perplexity"],
        "internal_links": ["/blog/gemini-review-2026/", "/blog/perplexity-vs-grok/", "/blog/chatgpt-vs-grok/"],
    },
    "qwen-ai-review": {
        "keyword": "Qwen AI review", "type": "review", "category": "AI chatbot",
        "title": "Qwen AI Review 2026: Is Alibaba's Model Worth Using?",
        "meta": "We tested Qwen 3 (Alibaba) on coding, long context, and multilingual tasks. Honest review of this open-source AI model.",
        "quick_answer": "Qwen 3 is the best open-source multilingual model for non-English languages. It's free via Hugging Face and Alibaba Cloud. Weak English coding compared to Claude/GPT. Best for Chinese/Spanish speakers; not for US devs.",
        "h2s": ["Quick Answer", "What Is Qwen?", "Setup", "What We Tested", "Multilingual Test", "Coding Test", "Qwen vs Llama", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["English quality lags behind GPT/Claude", "Self-hosting needs GPU", "Documentation is Chinese-first"],
        "rec_tools": ["Qwen 3", "DeepSeek", "Llama", "Kimi", "ChatGPT"],
        "internal_links": ["/blog/kimi-review/", "/blog/best-free-ai-tools-2026/", "/blog/best-open-source-ai-models/"],
    },
    "best-ai-headshot-generator": {
        "keyword": "best AI headshot generator", "type": "listicle", "category": "AI image generation",
        "title": "7 Best AI Headshot Generators in 2026 (Tested & Compared)",
        "meta": "We tested 7 AI headshot generators including Photoroom, HeadshotPro, and Aragon. Compare pricing, realism, and turnaround time.",
        "quick_answer": "Aragon wins for professional quality; HeadshotPro wins for team bulk; Photoroom wins for free. Most cost $20-50 for 40 headshots. Best value: Aragon at $29.",
        "h2s": ["Quick Answer", "How We Tested", "#1: Aragon — Best Overall", "#2: HeadshotPro — Best Team", "#3: Photoroom — Best Free", "#4: Artibot — Best Budget", "#5: ProPhotos — Best Realism", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["Some generators look too plastic", "Background removal is inconsistent", "Refunds are hard to get"],
        "rec_tools": ["Aragon", "HeadshotPro", "Photoroom", "Artibot", "ProPhotos"],
        "internal_links": ["/blog/best-ai-image-generators-2026/", "/blog/midjourney-v7-review-2026/", "/blog/best-ai-portrait-generators/"],
    },
    "best-ai-slack-bots": {
        "keyword": "best AI Slack bots", "type": "listicle", "category": "AI productivity",
        "title": "8 Best AI Slack Bots in 2026 (Tested for Productivity)",
        "meta": "We tested 8 AI Slack bots including ChatGPT, Notion AI, and Slack AI. Compare which bot actually saves your team time.",
        "quick_answer": "Slack AI wins for built-in summaries; ChatGPT wins for custom workflows; Notion AI wins for doc linking. Most are free or $7-10/user. Best overall: Slack AI included in Pro.",
        "h2s": ["Quick Answer", "How We Tested", "#1: Slack AI — Built-in", "#2: ChatGPT Bot — Most Flexible", "#3: Notion AI — Docs", "#4: Fireflies.ai — Meetings", "#5: DALL-E Bot — Images", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["Bot notifications can get noisy", "Context window limits per channel", "Permissions setup is confusing"],
        "rec_tools": ["Slack AI", "ChatGPT", "Notion AI", "Fireflies.ai", "Zapier AI"],
        "internal_links": ["/blog/best-ai-productivity-tools-2026/", "/blog/fireflies-ai-alternatives/", "/blog/best-ai-automation-tools/"],
    },
    "deepseek-vs-gpt": {
        "keyword": "DeepSeek vs GPT", "type": "comparison", "category": "AI chatbot",
        "title": "DeepSeek vs GPT 2026: Which AI Model Should You Use?",
        "meta": "We tested DeepSeek R1 and GPT-5 on coding, reasoning, and pricing. Head-to-head comparison of open-source vs closed AI.",
        "quick_answer": "DeepSeek R1 wins on price (free tier + open weights) and coding benchmarks; GPT-5 wins on reliability and app ecosystem. DeepSeek is free; GPT-5 is $20/mo. Pick DeepSeek for cost-sensitive devs, GPT for enterprise.",
        "h2s": ["Quick Verdict", "Test Setup", "Reasoning Benchmarks", "Coding Test", "Pricing", "API Costs", "Who Should Use DeepSeek?", "Who Should Use GPT?", "Final Verdict"],
        "painpoints": ["DeepSeek hallucinations on math", "No official US mobile app", "DeepSeek API has rate limits"],
        "rec_tools": ["DeepSeek R1", "GPT-5", "Claude Opus", "Llama", "Qwen"],
        "internal_links": ["/blog/chatgpt-deep-review-2026/", "/blog/best-free-ai-tools-2026/", "/blog/best-open-source-ai-models/"],
    },
}

os.makedirs("iteration_center/content_briefs", exist_ok=True)
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
    print(f"  Written: {slug}")

with open("iteration_center/state.json","r",encoding="utf-8") as f:
    state = json.load(f)
for slug, brief in SELECTED.items():
    state["next_iteration_focus"].append({
        "id": f"kw_r11_{slug.replace('-','_')}",
        "task": f"写{brief['type']}页：{brief['keyword']}（P0）",
        "assigned_to": ["window3"], "priority": "P0", "status": "pending",
        "source": "round11_2026-10-02", "slug": slug,
        "keyword": brief["keyword"], "type": brief["type"],
    })
with open("iteration_center/state.json","w",encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"\n=== {len(SELECTED)} briefs, {len(SELECTED)} P0 tasks ===")
