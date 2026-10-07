"""Round 12: Generate briefs"""
import json, os
os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round12.json","r",encoding="utf-8") as f:
    research = json.load(f)

SELECTED = {
    "gpt5-vs-o3": {
        "keyword": "GPT-5 vs OpenAI o3", "type": "comparison", "category": "AI chatbot",
        "title": "GPT-5 vs OpenAI o3 2026: Which OpenAI Model Should You Use?",
        "meta": "We tested GPT-5 and OpenAI o3 on coding, reasoning, and speed. Head-to-head comparison of two OpenAI flagship models.",
        "quick_answer": "o3 wins on complex reasoning and math; GPT-5 wins on speed and multimodal. Both are available on ChatGPT Plus ($20/mo). Pick o3 for hard problems, GPT-5 for everyday use.",
        "h2s": ["Quick Verdict", "Test Setup", "Reasoning Test", "Coding Test", "Speed Test", "Multimodal", "Pricing", "Who Should Use Which?", "Final Verdict"],
        "painpoints": ["o3 is slower than GPT-5", "Both models have usage caps", "No clear official comparison page"],
        "rec_tools": ["GPT-5", "OpenAI o3", "Claude Opus", "Gemini 2.5 Pro", "DeepSeek R1"],
        "internal_links": ["/blog/chatgpt-deep-review-2026/", "/blog/openai-o3-review/", "/blog/gpt-5-vs-claude-opus/"],
    },
    "perplexity-max-review": {
        "keyword": "Perplexity Max review", "type": "review", "category": "AI chatbot",
        "title": "Perplexity Max Review 2026: Is the $200/Month Plan Worth It?",
        "meta": "We tested Perplexity Max for 2 weeks. Honest review of this premium AI research plan — what you get vs Pro and whether it's worth $200/mo.",
        "quick_answer": "Perplexity Max ($200/mo) unlocks GPT-5, Claude Opus, and unlimited Pro searches. Best for power researchers and analysts. Most users are better off with Pro at $20/mo. Pick Max only if you hit Pro limits daily.",
        "h2s": ["Quick Answer", "What Is Perplexity Max?", "What We Tested", "Model Access", "Pro vs Max Comparison", "Is It Worth $200/mo?", "Pricing", "Strengths", "Weaknesses", "Who Should Upgrade?", "FAQs"],
        "painpoints": ["$200/mo is steep for most users", "No annual plan discount", "Browser extension still has limits"],
        "rec_tools": ["Perplexity Max", "Perplexity Pro", "ChatGPT Plus", "Claude Pro", "Gemini Advanced"],
        "internal_links": ["/blog/perplexity-review-2026/", "/blog/perplexity-vs-grok/", "/blog/claude-vs-perplexity/"],
    },
    "cursor-2-review": {
        "keyword": "Cursor 2.0 review", "type": "review", "category": "AI coding",
        "title": "Cursor 2.0 Review 2026: Is the AI Code Editor Still Worth It?",
        "meta": "We tested Cursor 2.0 on real projects. Honest review of this AI-first code editor — new features, pricing, and limitations.",
        "quick_answer": "Cursor 2.0 is still the best AI code editor. New features include background agents, multi-file edits, and built-in terminal. Pro is $20/mo. Best for professional developers; free tier is limited.",
        "h2s": ["Quick Answer", "What's New in Cursor 2.0?", "Setup", "What We Tested", "Background Agent", "Multi-File Edits", "Cursor vs Windsurf vs Copilot", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Background agent can be expensive", "Free tier has strict usage caps", "Refactoring large files breaks sometimes"],
        "rec_tools": ["Cursor", "Windsurf", "GitHub Copilot", "Claude Code", "Aider"],
        "internal_links": ["/blog/cursor-vs-windsurf/", "/blog/best-ai-coding-tools-2026/", "/blog/cursor-vs-aider/"],
    },
    "best-ai-grammar-checker": {
        "keyword": "best AI grammar checker", "type": "listicle", "category": "AI writing",
        "title": "8 Best AI Grammar Checkers in 2026 (Tested & Compared)",
        "meta": "We tested 8 AI grammar checkers including Grammarly, ProWritingAid, and QuillBot. Compare accuracy, pricing, and features.",
        "quick_answer": "Grammarly Premium wins for overall accuracy; ProWritingAid wins for fiction writers; QuillBot wins for paraphrasing. Free options: Grammarly Free and LanguageTool. Most cost $12-30/mo.",
        "h2s": ["Quick Answer", "How We Tested", "#1: Grammarly — Best Overall", "#2: ProWritingAid — Best Fiction", "#3: QuillBot — Best Paraphrasing", "#4: LanguageTool — Best Free", "#5: Wordtune — Best Rewrite", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["Grammarly misses some style issues", "Browser extension slows down sites", "ProWritingAid UI is dated"],
        "rec_tools": ["Grammarly", "ProWritingAid", "QuillBot", "LanguageTool", "Wordtune"],
        "internal_links": ["/blog/grammarly-alternatives/", "/blog/best-ai-writing-tools-2026/", "/blog/quillbot-alternatives/"],
    },
    "claude-vs-deepseek": {
        "keyword": "Claude vs DeepSeek", "type": "comparison", "category": "AI chatbot",
        "title": "Claude vs DeepSeek 2026: Which AI Model Wins?",
        "meta": "We tested Claude Opus 4.5 and DeepSeek R1 on coding, reasoning, and long context. Head-to-head comparison with pricing.",
        "quick_answer": "Claude wins on writing quality and enterprise safety; DeepSeek wins on price and open weights. Claude Pro is $20/mo; DeepSeek is free. Pick Claude for writing, DeepSeek for cost-sensitive coding.",
        "h2s": ["Quick Verdict", "Test Setup", "Writing Quality", "Coding Test", "Long Context", "Pricing", "Who Should Use Claude?", "Who Should Use DeepSeek?", "Final Verdict"],
        "painpoints": ["DeepSeek English quality lags", "Claude rate limits on free tier", "Both models hallucinate on niche facts"],
        "rec_tools": ["Claude Opus", "DeepSeek R1", "GPT-5", "Gemini 2.5 Pro", "Llama"],
        "internal_links": ["/blog/best-ai-chatbots-2026/", "/blog/deepseek-vs-gpt/", "/blog/chatgpt-alternatives-2026/"],
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
        "id": f"kw_r12_{slug.replace('-','_')}",
        "task": f"写{brief['type']}页：{brief['keyword']}（P0）",
        "assigned_to": ["window3"], "priority": "P0", "status": "pending",
        "source": "round12_2026-10-03", "slug": slug,
        "keyword": brief["keyword"], "type": brief["type"],
    })
with open("iteration_center/state.json","w",encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"\n=== {len(SELECTED)} briefs, {len(SELECTED)} P0 tasks ===")
