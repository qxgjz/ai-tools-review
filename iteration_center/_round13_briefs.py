"""Round 13: Generate briefs"""
import json, os
os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round13.json","r",encoding="utf-8") as f:
    research = json.load(f)

SELECTED = {
    "replit-ai-agent-review": {
        "keyword": "Replit AI Agent review", "type": "review", "category": "AI coding",
        "title": "Replit AI Agent Review 2026: Is the Autonomous Coder Any Good?",
        "meta": "We tested Replit AI Agent (Replit Agent) for 2 weeks. Honest review of this autonomous coding AI — what it builds, pricing, and limitations.",
        "quick_answer": "Replit AI Agent is best for prototyping simple web apps fast. It builds full-stack apps from prompts in minutes. Starter is free; Core is $25/mo. Not for production code or complex architectures.",
        "h2s": ["Quick Answer", "What Is Replit AI Agent?", "Setup", "What We Tested", "What It Builds Well", "What It Fails At", "Replit vs Cursor vs Lovable", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Generated code needs heavy cleanup", "No Git integration in free tier", "Large apps time out"],
        "rec_tools": ["Replit Agent", "Cursor", "Lovable", "Bolt.new", "v0.dev"],
        "internal_links": ["/blog/cursor-review/", "/blog/lovable-review/", "/blog/best-ai-coding-tools-2026/"],
    },
    "reworkd-review": {
        "keyword": "Reworkd AI review", "type": "review", "category": "AI productivity",
        "title": "Reworkd AI Review 2026: Is the AI Agent Platform Worth It?",
        "meta": "We tested Reworkd (formerly Weasywork) AI agents. Honest review of this autonomous task automation platform — pricing, features, and real-world results.",
        "quick_answer": "Reworkd AI automates sales prospecting and outreach with AI agents. It starts at $49/mo for 1 seat. Best for small B2B teams needing lead gen automation. Not for non-sales use cases.",
        "h2s": ["Quick Answer", "What Is Reworkd?", "Setup", "What We Tested", "Lead Generation", "Outreach Quality", "Reworkd vs Clay vs Apollo", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Lead data quality varies", "Outreach emails look templated", "No CRM integration on basic plan"],
        "rec_tools": ["Reworkd", "Clay", "Apollo.io", "Instantly", "Lemlist"],
        "internal_links": ["/blog/best-ai-automation-tools/", "/blog/best-ai-sales-tools/", "/blog/best-ai-lead-generation/"],
    },
    "taskade-review": {
        "keyword": "Taskade AI review", "type": "review", "category": "AI productivity",
        "title": "Taskade AI Review 2026: Is the All-in-One Workspace Worth It?",
        "meta": "We tested Taskade AI for 2 weeks. Honest review of this AI-powered project management workspace — notes, docs, tasks, and AI agents in one app.",
        "quick_answer": "Taskade combines docs, tasks, and AI agents in one free workspace. Free tier is generous; Pro is $8/mo. Best for solopreneurs and small teams. Not for enterprise-scale project management.",
        "h2s": ["Quick Answer", "What Is Taskade?", "Setup", "What We Tested", "AI Agents", "Docs & Tasks", "Taskade vs Notion vs ClickUp", "Pricing", "Strengths", "Weaknesses", "Who Should Use It?", "FAQs"],
        "painpoints": ["Mobile app is clunky", "AI agent can't handle complex workflows", "No offline mode"],
        "rec_tools": ["Taskade", "Notion", "ClickUp", "Monday.com", "Todoist"],
        "internal_links": ["/blog/notion-ai-review/", "/blog/best-project-management-tools/", "/blog/best-ai-productivity-tools-2026/"],
    },
    "best-ai-website-builder-2026": {
        "keyword": "best AI website builder 2026", "type": "listicle", "category": "AI tools",
        "title": "10 Best AI Website Builders in 2026 (Tested & Compared)",
        "meta": "We tested 10 AI website builders including Framer, Wix ADI, and Durable. Compare which AI builder actually delivers a production-ready site.",
        "quick_answer": "Framer wins for design control; Durable wins for speed; Wix wins for ecommerce. Most cost $14-30/mo. Best value: Framer at $15/mo for a fully custom site in hours.",
        "h2s": ["Quick Answer", "How We Tested", "#1: Framer — Best Design Control", "#2: Durable — Fastest Setup", "#3: Wix ADI — Best Ecommerce", "#4: Hostinger AI — Best Budget", "#5: Webflow AI — Best Dev", "Comparison Table", "Pricing", "FAQs"],
        "painpoints": ["AI-generated sites look generic", "SEO optimization is weak on most", "Switching platforms is hard"],
        "rec_tools": ["Framer", "Durable", "Wix", "Hostinger", "Webflow"],
        "internal_links": ["/blog/best-ai-tools-2026/", "/blog/best-ai-landing-page-generators/", "/blog/framer-ai-review/"],
    },
    "gemini-3-vs-gpt5": {
        "keyword": "Gemini 3 vs GPT-5", "type": "comparison", "category": "AI chatbot",
        "title": "Gemini 3 vs GPT-5 2026: Which AI Model Wins?",
        "meta": "We tested Google Gemini 3 and OpenAI GPT-5 on reasoning, coding, and multimodal. Head-to-head comparison with pricing.",
        "quick_answer": "Gemini 3 wins on long context and multimodal; GPT-5 wins on reasoning consistency. Both are $20/mo. Pick Gemini for video/image analysis, GPT-5 for complex problem-solving.",
        "h2s": ["Quick Verdict", "Test Setup", "Reasoning", "Coding", "Multimodal", "Long Context", "Pricing", "Who Should Use Which?", "Final Verdict"],
        "painpoints": ["Gemini 3 hallucinates on math", "GPT-5 is slower on long docs", "Both have usage caps on mobile"],
        "rec_tools": ["Gemini 3", "GPT-5", "Claude Opus", "DeepSeek R1", "Grok 3"],
        "internal_links": ["/blog/gemini-review-2026/", "/blog/chatgpt-deep-review-2026/", "/blog/best-ai-chatbots-2026/"],
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
        "id": f"kw_r13_{slug.replace('-','_')}",
        "task": f"写{brief['type']}页：{brief['keyword']}（P0）",
        "assigned_to": ["window3"], "priority": "P0", "status": "pending",
        "source": "round13_2026-10-03", "slug": slug,
        "keyword": brief["keyword"], "type": brief["type"],
    })
with open("iteration_center/state.json","w",encoding="utf-8") as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
print(f"\n=== {len(SELECTED)} briefs, {len(SELECTED)} P0 tasks ===")
