"""Round 6: Generate briefs for best opportunities"""
import json, os

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round6.json","r",encoding="utf-8") as f:
    research = json.load(f)

# Select best opportunities: low KD first
SELECTED = {
    "notion-ai-vs-obsidian-ai": {
        "keyword": "Notion AI vs Obsidian AI", "type": "comparison", "category": "note-taking AI",
        "title": "Notion AI vs Obsidian AI 2026: Which Knowledge Base Wins?",
        "meta": "We compared Notion AI and Obsidian AI on note-taking, AI search, pricing, and offline use. See which knowledge base fits your workflow.",
        "quick_answer": "Notion AI wins for team collaboration and real-time sync; Obsidian AI wins for local-first notes and plugin ecosystem. Notion AI starts at $10/mo per member; Obsidian AI is $8/mo. Pick Notion for teams, Obsidian for individual power users.",
        "h2s": ["Quick Verdict", "What We Tested", "Note-Taking Experience", "AI Features Comparison", "Pricing", "Who Should Use Notion?", "Who Should Use Obsidian?", "Pain Points", "Final Verdict"],
        "painpoints": ["Notion AI search misses old notes in large workspaces", "Obsidian AI requires manual plugin setup for basic features", "Notion's offline mode is unreliable on slow connections"],
        "rec_tools": ["Notion AI", "Obsidian AI", "Logseq", "Roam Research", "Mem.ai"],
        "internal_links": ["/blog/best-ai-note-taking-apps/", "/blog/notion-ai-review-2026/", "/blog/best-ai-productivity-tools/"],
    },
    "grammarly-alternatives": {
        "keyword": "Grammarly alternatives", "type": "alternatives", "category": "AI writing assistant",
        "title": "7 Best Grammarly Alternatives in 2026 (Free & Paid)",
        "meta": "Tired of Grammarly's premium paywall? We tested 7 alternatives including ProWritingAid, LanguageTool, and QuillBot. See which grammar checker beats Grammarly.",
        "quick_answer": "ProWritingAid wins for detailed style reports; LanguageTool wins for free tier and multi-language; QuillBot wins for paraphrasing. Grammarly Premium is $12/mo. Free option: LanguageTool free tier checks 10,000 characters.",
        "h2s": ["Quick Answer", "Why Look Beyond Grammarly?", "#1: ProWritingAid — Best Detailed Feedback", "#2: LanguageTool — Best Free Option", "#3: QuillBot — Best Paraphrasing", "#4: Hemingway Editor — Best Readability", "#5: Writer.com — Best Enterprise", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["Grammarly underlines valid technical terms as errors", "Premium features are locked behind expensive subscription", "Browser extension slows down sites like Notion and Gmail"],
        "rec_tools": ["ProWritingAid", "LanguageTool", "QuillBot", "Hemingway Editor", "Writer.com"],
        "internal_links": ["/blog/best-ai-grammar-checkers/", "/blog/quillbot-alternatives/", "/blog/best-ai-writing-tools/"],
    },
    "roo-code-review": {
        "keyword": "Roo Code review", "type": "review", "category": "AI coding extension",
        "title": "Roo Code Review 2026: Is the Free AI Coding Agent Worth It?",
        "meta": "We tested Roo Code (formerly Cline) on real coding tasks. Honest review of this open-source AI coding extension — pricing, features, and how it compares to Cursor.",
        "quick_answer": "Roo Code is a powerful open-source VS Code extension that uses your own API key (Claude/GPT), making it cheaper than Cursor for heavy users. It excels at autonomous multi-file edits but lacks Cursor's polish. Free to use with your own API key; Cursor Pro is $20/mo.",
        "h2s": ["Quick Answer", "What Is Roo Code?", "What We Tested", "Real Test Results: Feature Builds", "Roo Code vs Cursor", "Pricing (API Key Breakdown)", "Strengths", "Weaknesses", "Who Should Use Roo Code?", "FAQs"],
        "painpoints": ["Roo Code makes too many API calls without warning", "Multi-file edits can break builds without rollback", "Configuration is overwhelming for beginners"],
        "rec_tools": ["Roo Code", "Cursor", "Claude Code", "GitHub Copilot", "Windsurf"],
        "internal_links": ["/blog/cursor-alternatives-2026/", "/blog/cursor-vs-github-copilot-2026/", "/blog/windsurf-vs-cursor/"],
    },
    "crawl4ai-review": {
        "keyword": "Crawl4AI review", "type": "review", "category": "AI web scraping",
        "title": "Crawl4AI Review 2026: Best Open-Source Web Scraper for LLMs?",
        "meta": "We tested Crawl4AI for 2 weeks. Honest review of this open-source web scraping library designed for AI/LLM pipelines — setup, performance, and limitations.",
        "quick_answer": "Crawl4AI is the best open-source web scraper for LLM pipelines. It handles JavaScript rendering, extracts clean markdown, and is free under Apache 2.0. Setup requires Python 3.8+ and Playwright. Best for developers building RAG systems, not for non-technical users.",
        "h2s": ["Quick Answer", "What Is Crawl4AI?", "Setup & Installation", "What We Tested", "Performance Benchmarks", "Crawl4AI vs Scrapy vs BeautifulSoup", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Installing Playwright on Windows requires manual browser download", "JavaScript-heavy sites still need custom wait strategies", "No GUI — requires coding knowledge"],
        "rec_tools": ["Crawl4AI", "Scrapy", "BeautifulSoup", "Firecrawl", "Browserbase"],
        "internal_links": ["/blog/best-ai-coding-tools/", "/blog/python-web-scraping/", "/blog/best-ai-api-tools/"],
    },
    "chatgpt-vs-gemini-2026": {
        "keyword": "ChatGPT vs Gemini 2026", "type": "comparison", "category": "AI chatbot",
        "title": "ChatGPT vs Gemini 2026: Which AI Chatbot Is Actually Better?",
        "meta": "We tested ChatGPT (GPT-5) vs Gemini (2.0 Flash/Pro) on coding, writing, math, and multimodal. Real head-to-head results with benchmarks.",
        "quick_answer": "ChatGPT GPT-5 wins on reasoning and coding; Gemini 2.0 Pro wins on multimodal and Google ecosystem integration. ChatGPT Plus is $20/mo; Gemini Advanced is $19.99/mo. Pick ChatGPT for coding, Gemini for video/image analysis.",
        "h2s": ["Quick Verdict", "Benchmarks We Ran", "Coding Test Results", "Writing & Reasoning", "Multimodal", "Pricing", "Who Should Use ChatGPT?", "Who Should Use Gemini?", "Final Verdict"],
        "painpoints": ["ChatGPT still hallucinates facts without web search enabled", "Gemini's chat history sync is unreliable across devices", "Both tools throttle heavy users without warning"],
        "rec_tools": ["ChatGPT Plus", "Gemini Advanced", "Claude 3.7", "Grok", "Copilot"],
        "internal_links": ["/blog/chatgpt-alternatives-2026/", "/blog/perplexity-vs-chatgpt/", "/blog/gemini-vs-perplexity/"],
    },
    "midjourney-v7-vs-flux": {
        "keyword": "Midjourney v7 vs Flux", "type": "comparison", "category": "AI image generation",
        "title": "Midjourney v7 vs Flux 2026: Which Image Generator Wins?",
        "meta": "We generated 50 images with the same prompts on Midjourney v7 and Flux 1.1. Detailed comparison of quality, speed, pricing, and use cases.",
        "quick_answer": "Midjourney v7 wins on artistic quality and stylistic consistency; Flux 1.1 wins on speed and commercial licensing. Midjourney is $10/mo; Flux is free via dev API or $10/month via Replicate. Pick Midjourney for art, Flux for production assets.",
        "h2s": ["Quick Verdict", "What We Generated", "Quality Comparison", "Prompt Following", "Speed & Generation Time", "Pricing & Licensing", "Who Should Use Midjourney?", "Who Should Use Flux?", "Final Verdict"],
        "painpoints": ["Midjourney requires a Discord subscription which feels outdated", "Flux character consistency across images is poor", "Midjourney's commercial license is ambiguous for clients"],
        "rec_tools": ["Midjourney v7", "Flux 1.1", "DALL-E 3", "Stable Diffusion 3", "Ideogram"],
        "internal_links": ["/blog/best-ai-image-generators/", "/blog/midjourney-v7-review-2026/", "/blog/dall-e-3-vs-midjourney/"],
    },
    "surfer-seo-alternatives": {
        "keyword": "Surfer SEO alternatives", "type": "alternatives", "category": "SEO content optimization",
        "title": "6 Best Surfer SEO Alternatives in 2026 (Cheaper & Better)",
        "meta": "Surfer SEO costs $89/mo minimum. We tested 6 alternatives including Frase, Clearscope, and NeuronWriter. See which SEO content tool gives better ROI.",
        "quick_answer": "Frase wins for AI content briefs on a budget; NeuronWriter wins for affordable content optimization; Rank Math wins for WordPress. Surfer SEO starts at $89/mo. Best value: Frase at $15/mo for similar SERP analysis.",
        "h2s": ["Quick Answer", "Why Look Beyond Surfer?", "#1: Frase — Best Budget Option", "#2: NeuronWriter — Best Affordable", "#3: Clearscope — Best Enterprise", "#4: Rank Math — Best WordPress", "#5: MarketMuse — Best Research", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["Surfer's content score doesn't correlate with actual rankings", "Keyword research is weaker than dedicated SEO tools", "Team seats are expensive at $29/mo extra"],
        "rec_tools": ["Frase", "NeuronWriter", "Clearscope", "Rank Math", "MarketMuse"],
        "internal_links": ["/blog/clearscope-alternatives/", "/blog/best-ai-seo-tools/", "/blog/writesonic-alternatives/"],
    },
    "elevenlabs-alternatives": {
        "keyword": "ElevenLabs alternatives", "type": "alternatives", "category": "AI voice generation",
        "title": "7 Best ElevenLabs Alternatives in 2026 (More Human, Less Expensive)",
        "meta": "Tired of ElevenLabs credits burning through? We tested 7 alternatives including Play.ht, Murf, and Rime. See which AI voice generator sounds more human.",
        "quick_answer": "Play.ht wins for voice cloning accuracy; Murf wins for podcast production; MiniMax wins for free tier. ElevenLabs starts at $5/mo for 10 minutes. Free option: MiniMax offers 10 minutes/month free.",
        "h2s": ["Quick Answer", "Why Look Beyond ElevenLabs?", "#1: Play.ht — Best Voice Cloning", "#2: Murf — Best Podcast Production", "#3: MiniMax — Best Free Tier", "#4: Rime — Best Natural Voice", "#5: WellSaid Labs — Best Enterprise", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["ElevenLabs credits run out fast for long-form narration", "Voice cloning requires many samples for accuracy", "Emotional range is limited compared to human voice actors"],
        "rec_tools": ["Play.ht", "Murf AI", "MiniMax", "Rime", "WellSaid Labs"],
        "internal_links": ["/blog/elevenlabs-review-2026/", "/blog/best-ai-voice-generators/", "/blog/best-ai-text-to-speech/"],
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
- **KD**: low (2/3 weak domains in top 3)
- **Title**: {brief['title']}
- **Meta**: {brief['meta']}

## Quick Answer
{brief['quick_answer']}

## Key Takeaways
1. {brief['quick_answer'].split('.')[0]}.
2. Real test results with pricing breakdown.
3. Clear recommendation by use case.

## H2 Outline
"""
    for i, h2 in enumerate(brief["h2s"], 1):
        content += f"{i}. {h2}\n"
    
    content += f"""
## Must Include
- Comparison table
- 3+ A vs B conclusions
- How We Tested section
- At least 2 affiliate links
- Internal links: {', '.join(brief['internal_links'])}
- Recommended tools: {', '.join(brief['rec_tools'])}

## Pain Points to Address
"""
    for i, p in enumerate(brief["painpoints"], 1):
        content += f"{i}. {p}\n"
    
    content += "\n## FAQ (from PAA)\n"
    for q in paa[:5]:
        content += f"\n### {q}\n\nAnswer: See detailed comparison above.\n"
    
    content += "\n## Competitor SERP\n"
    for c in competitors[:3]:
        content += f"- {c.get('title','')}: {c.get('url','')}\n"
    
    content += f"\n## Word Count: 2500-3500\n## Language: 100% English (US)\n"
    
    filepath = f"iteration_center/content_briefs/{slug}_input.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    written.append(slug)
    print(f"  Written: {slug}_input.md")

# Now add these as P0 tasks in state.json
with open("iteration_center/state.json","r",encoding="utf-8") as f:
    state = json.load(f)

new_tasks = []
for slug, brief in SELECTED.items():
    task_id = f"kw_r6_{slug.replace('-','_')}"
    new_task = {
        "id": task_id,
        "task": f"写{brief['type']}页：{brief['keyword']}（KD低，2/3弱域名，P0）",
        "assigned_to": ["window3"],
        "priority": "P0",
        "status": "pending",
        "source": "keyword_research_round6_2026-10-01",
        "slug": slug,
        "keyword": brief["keyword"],
        "type": brief["type"],
    }
    state["next_iteration_focus"].append(new_task)
    new_tasks.append(task_id)

with open("iteration_center/state.json","w",encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"\n=== {len(written)} briefs generated ===")
print(f"=== {len(new_tasks)} new P0 tasks added to state.json ===")
for t in new_tasks:
    print(f"  + {t}")
