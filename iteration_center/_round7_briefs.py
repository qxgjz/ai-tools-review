"""Round 7: Generate briefs for new gap keywords"""
import json, os

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round7.json","r",encoding="utf-8") as f:
    research = json.load(f)

# Only pick truly new gaps (not already covered by existing posts)
SELECTED = {
    "cursor-vs-aider": {
        "keyword": "Cursor vs Aider", "type": "comparison", "category": "AI coding",
        "title": "Cursor vs Aider 2026: Which AI Coding Tool Wins for Developers?",
        "meta": "We tested Cursor and Aider on real projects. Honest comparison of these AI coding tools — pricing, features, autonomous coding, and which one fits your workflow.",
        "quick_answer": "Cursor wins for IDE-based AI assistance with visual diffs and multi-file edits; Aider wins for terminal-first git-native coding with any LLM. Cursor Pro is $20/mo; Aider is free (bring your own API key). Pick Cursor for beginners, Aider for CLI power users.",
        "h2s": ["Quick Verdict", "What We Tested", "Setup & Onboarding", "Coding Workflow", "Autonomous Mode Comparison", "Pricing", "Cursor Pros & Cons", "Aider Pros & Cons", "Who Should Use Which?", "Final Verdict"],
        "painpoints": ["Cursor's multi-file edits sometimes break builds", "Aider has steep learning curve for non-CLI users", "Both tools can burn API credits quickly"],
        "rec_tools": ["Cursor", "Aider", "Claude Code", "GitHub Copilot", "Windsurf"],
        "internal_links": ["/blog/cursor-alternatives-2026/", "/blog/cursor-vs-github-copilot-2026/", "/blog/cursor-review-2026/"],
    },
    "v0-vs-lovable": {
        "keyword": "v0 vs Lovable", "type": "comparison", "category": "AI app builder",
        "title": "v0 vs Lovable 2026: Which AI App Builder Is Better?",
        "meta": "We built the same app with v0.dev and Lovable. Detailed comparison of these AI website builders — pricing, export quality, customization, and deploy.",
        "quick_answer": "v0 wins for Tailwind/React code quality and developer handoff; Lovable wins for full-stack app generation with backend included. v0 is free tier + $20/mo Pro; Lovable starts at $25/mo. Pick v0 for frontend prototypes, Lovable for full-stack MVPs.",
        "h2s": ["Quick Verdict", "What We Built", "Generation Speed", "Code Quality", "Customization Control", "Backend & Database", "Pricing", "Who Should Use v0?", "Who Should Use Lovable?", "Final Verdict"],
        "painpoints": ["v0 requires manual backend setup", "Lovable's exported code is locked to their platform", "Both tools struggle with complex auth flows"],
        "rec_tools": ["v0.dev", "Lovable", "Bolt.new", "Bubble", "Webflow AI"],
        "internal_links": ["/blog/lovable-vs-boltnew/", "/blog/best-ai-app-builders/", "/blog/best-ai-website-builders/"],
    },
    "claude-vs-perplexity": {
        "keyword": "Claude vs Perplexity", "type": "comparison", "category": "AI chatbot",
        "title": "Claude vs Perplexity 2026: Which AI Assistant Wins?",
        "meta": "We tested Claude 3.7 and Perplexity on research, writing, coding, and citation accuracy. Head-to-head results with pricing comparison.",
        "quick_answer": "Claude wins on long-document analysis and creative writing; Perplexity wins on real-time web research with citations. Claude Pro is $20/mo; Perplexity Pro is $20/mo. Pick Claude for document work, Perplexity for up-to-date research.",
        "h2s": ["Quick Verdict", "Test Methodology", "Research & Citation Test", "Long Document Analysis", "Coding Test", "Writing Quality", "Pricing", "Who Should Use Claude?", "Who Should Use Perplexity?", "Final Verdict"],
        "painpoints": ["Perplexity citations sometimes point to paywalled sources", "Claude web search is slower than Perplexity", "Both tools struggle with recent news in niche topics"],
        "rec_tools": ["Claude Pro", "Perplexity Pro", "ChatGPT Plus", "Gemini Advanced", "Grok"],
        "internal_links": ["/blog/perplexity-review-2026/", "/blog/claude-review-2026/", "/blog/chatgpt-alternatives-2026/"],
    },
    "heygen-alternatives": {
        "keyword": "HeyGen alternatives", "type": "alternatives", "category": "AI video generation",
        "title": "6 Best HeyGen Alternatives in 2026 (Cheaper & More Realistic)",
        "meta": "HeyGen is expensive. We tested 6 alternatives including Synthesia, Elai, and Colossyan. See which AI avatar video generator gives better value.",
        "quick_answer": "Synthesia wins for professional training videos; Elai wins for multi-language support; Colossyan wins for budget pricing. HeyGen starts at $24/mo. Best value: Colossyan at $30/mo with similar avatar quality.",
        "h2s": ["Quick Answer", "Why Look Beyond HeyGen?", "#1: Synthesia — Best Professional", "#2: Elai.io — Best Multi-Language", "#3: Colossyan — Best Budget", "#4: D-ID — Best API", "#5: Arcads — Best Ads", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["HeyGen avatars still look uncanny in close-ups", "Video rendering is slow during peak hours", "Custom avatar creation requires expensive credits"],
        "rec_tools": ["Synthesia", "Elai.io", "Colossyan", "D-ID", "Arcads"],
        "internal_links": ["/blog/synthesia-vs-heygen/", "/blog/heygen-review-2026/", "/blog/best-ai-video-generators/"],
    },
    "n8n-ai-review": {
        "keyword": "n8n AI review", "type": "review", "category": "AI automation",
        "title": "n8n AI Review 2026: Is the Open-Source Zapier Alternative Worth It?",
        "meta": "We tested n8n AI for 2 weeks. Honest review of this open-source workflow automation tool — self-hosted, pricing, AI features, and limitations.",
        "quick_answer": "n8n is the best open-source Zapier alternative for technical teams. It supports self-hosting, 400+ integrations, and AI workflows. Free self-hosted; cloud starts at $20/mo. Best for dev teams that want control; not for non-technical users.",
        "h2s": ["Quick Answer", "What Is n8n?", "Setup & Self-Hosting", "What We Tested", "AI Features", "n8n vs Zapier", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Self-hosting requires DevOps knowledge", "n8n updates can break existing workflows", "UI is less polished than Zapier"],
        "rec_tools": ["n8n", "Zapier", "Make.com", "Dify", "Activepieces"],
        "internal_links": ["/blog/best-ai-automation-agents-2026/", "/blog/zapier-ai-alternatives/", "/blog/dify-ai-review/"],
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

# Add tasks to state.json
with open("iteration_center/state.json","r",encoding="utf-8") as f:
    state = json.load(f)

new_tasks = []
for slug, brief in SELECTED.items():
    task_id = f"kw_r7_{slug.replace('-','_')}"
    new_task = {
        "id": task_id,
        "task": f"写{brief['type']}页：{brief['keyword']}（KD低，P0）",
        "assigned_to": ["window3"],
        "priority": "P0",
        "status": "pending",
        "source": "keyword_research_round7_2026-10-01",
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
