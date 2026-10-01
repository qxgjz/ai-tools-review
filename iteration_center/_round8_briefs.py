"""Round 8: Generate briefs for new gap keywords"""
import json, os

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round8.json","r",encoding="utf-8") as f:
    research = json.load(f)

SELECTED = {
    "copilot-vs-gemini": {
        "keyword": "Microsoft Copilot vs Gemini", "type": "comparison", "category": "AI chatbot",
        "title": "Microsoft Copilot vs Gemini 2026: Which AI Assistant Wins?",
        "meta": "We tested Microsoft Copilot and Gemini on coding, writing, multimodal, and pricing. Head-to-head results with free vs paid tier comparison.",
        "quick_answer": "Gemini wins on multimodal and Google ecosystem integration; Copilot wins on Microsoft 365 integration and free tier. Copilot free tier is generous; Gemini Advanced is $19.99/mo. Pick Gemini for research, Copilot for Office work.",
        "h2s": ["Quick Verdict", "Test Methodology", "Free Tier Comparison", "Multimodal Test", "Office/Productivity", "Coding Test", "Pricing", "Who Should Use Copilot?", "Who Should Use Gemini?", "Final Verdict"],
        "painpoints": ["Copilot still routes to Bing with ads in free tier", "Gemini free tier has usage limits", "Both tools struggle with enterprise data privacy"],
        "rec_tools": ["Microsoft Copilot", "Gemini", "ChatGPT Plus", "Claude", "Perplexity"],
        "internal_links": ["/blog/gemini-review-2026/", "/blog/chatgpt-alternatives-2026/", "/blog/microsoft-365-copilot-review-2026/"],
    },
    "perplexity-vs-grok": {
        "keyword": "Perplexity vs Grok", "type": "comparison", "category": "AI chatbot",
        "title": "Perplexity vs Grok 2026: Which AI Search Tool Is Better?",
        "meta": "We tested Perplexity Pro and Grok 3 on real-time search, coding, and personality. Honest comparison of these two AI search assistants.",
        "quick_answer": "Perplexity wins on citation accuracy and research workflow; Grok wins on real-time X (Twitter) data and personality. Perplexity Pro is $20/mo; Grok Premium is $30/mo. Pick Perplexity for research, Grok for social media monitoring.",
        "h2s": ["Quick Verdict", "What We Tested", "Search & Citation Test", "Real-Time Data", "Coding Test", "Pricing", "Who Should Use Perplexity?", "Who Should Use Grok?", "Final Verdict"],
        "painpoints": ["Perplexity citations sometimes point to low-quality sources", "Grok's real-time data has a 15-minute delay", "Both tools hallucinate on niche topics"],
        "rec_tools": ["Perplexity Pro", "Grok 3", "ChatGPT Plus", "Gemini Advanced", "Claude"],
        "internal_links": ["/blog/perplexity-review-2026/", "/blog/claude-vs-perplexity/", "/blog/chatgpt-alternatives-2026/"],
    },
    "aider-review": {
        "keyword": "Aider AI review", "type": "review", "category": "AI coding",
        "title": "Aider AI Review 2026: Is the Open-Source Coding Agent Worth It?",
        "meta": "We tested Aider for 2 weeks on real projects. Honest review of this open-source terminal-based AI coding assistant — setup, LLM support, and limitations.",
        "quick_answer": "Aider is the best open-source terminal-based AI coding assistant. It works with any LLM (Claude/GPT/DeepSeek), tracks git commits automatically, and is free under Apache 2.0. Requires Python and CLI comfort. Best for devs who live in the terminal; not for beginners.",
        "h2s": ["Quick Answer", "What Is Aider?", "Setup & Installation", "What We Tested", "Git Integration", "LLM Support", "Aider vs Cursor", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["No GUI — terminal only", "Requires manual model configuration", "Diff resolution can be confusing"],
        "rec_tools": ["Aider", "Cursor", "Claude Code", "GitHub Copilot", "Roo Code"],
        "internal_links": ["/blog/cursor-vs-aider/", "/blog/best-ai-coding-tools-2026/", "/blog/cursor-alternatives-2026/"],
    },
    "fireflies-ai-alternatives": {
        "keyword": "Fireflies.ai alternatives", "type": "alternatives", "category": "AI meeting notes",
        "title": "6 Best Fireflies.ai Alternatives in 2026 (Cheaper & More Accurate)",
        "meta": "Fireflies.ai is expensive. We tested 6 alternatives including Otter.ai, Granola, and Fathom. See which AI meeting note taker gives better value.",
        "quick_answer": "Granola wins for macOS-native speed; Fathom wins for free Zoom recording; Otter.ai wins for established brand. Fireflies.ai starts at $18/mo. Best free option: Fathom for Zoom users.",
        "h2s": ["Quick Answer", "Why Look Beyond Fireflies?", "#1: Granola — Best macOS", "#2: Fathom — Best Free", "#3: Otter.ai — Best Established", "#4: Read.ai — Best AI Summaries", "#5: tl;dv — Best Multi-Platform", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["Fireflies.ai transcript accuracy drops with accents", "Video playback can be laggy", "Team seats are expensive"],
        "rec_tools": ["Granola", "Fathom", "Otter.ai", "Read.ai", "tl;dv"],
        "internal_links": ["/blog/otter-ai-alternatives/", "/blog/best-ai-meeting-assistants-2026/", "/blog/best-ai-transcription-tools-2026/"],
    },
    "boltnew-review": {
        "keyword": "Bolt.new review", "type": "review", "category": "AI app builder",
        "title": "Bolt.new Review 2026: Is StackBlitz's AI Builder Worth It?",
        "meta": "We tested Bolt.new (StackBlitz) on real projects. Honest review of this AI full-stack web app builder — pricing, code quality, and limitations.",
        "quick_answer": "Bolt.new is the fastest AI full-stack app builder for prototypes. It runs in-browser, generates React + Tailwind + Supabase, and exports clean code. Free tier available; Pro is $20/mo. Best for MVPs; not for production.",
        "h2s": ["Quick Answer", "What Is Bolt.new?", "Setup", "What We Built", "Code Quality", "Bolt.new vs Lovable vs v0", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Exported code still needs manual cleanup", "Supabase integration is limited", "Mobile responsiveness is inconsistent"],
        "rec_tools": ["Bolt.new", "Lovable", "v0.dev", "Bubble", "Webflow AI"],
        "internal_links": ["/blog/lovable-vs-boltnew/", "/blog/v0-vs-lovable/", "/blog/best-ai-app-builders/"],
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
- **KD**: low/medium (see research data)
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

# Add tasks to state.json
with open("iteration_center/state.json","r",encoding="utf-8") as f:
    state = json.load(f)

new_tasks = []
for slug, brief in SELECTED.items():
    task_id = f"kw_r8_{slug.replace('-','_')}"
    new_task = {
        "id": task_id,
        "task": f"写{brief['type']}页：{brief['keyword']}（P0）",
        "assigned_to": ["window3"],
        "priority": "P0",
        "status": "pending",
        "source": "keyword_research_round8_2026-10-01",
        "slug": slug,
        "keyword": brief["keyword"],
        "type": brief["type"],
    }
    state["next_iteration_focus"].append(new_task)
    new_tasks.append(task_id)

with open("iteration_center/state.json","w",encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

print(f"\n=== {len(written)} briefs generated ===")
print(f"=== {len(new_tasks)} new P0 tasks added ===")
for t in new_tasks:
    print(f"  + {t}")
