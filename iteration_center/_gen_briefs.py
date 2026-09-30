"""Generate 11 content briefs from SERP research data"""
import json, os

os.chdir(r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review")

with open("iteration_center/keyword_research_round5.json", "r", encoding="utf-8") as f:
    research = json.load(f)

os.makedirs("iteration_center/content_briefs", exist_ok=True)

# Brief templates per keyword
BRIEFS = {
    "lovable-vs-boltnew": {
        "slug": "lovable-vs-boltnew",
        "keyword": "Lovable vs Bolt.new",
        "type": "comparison",
        "category": "AI app builders",
        "title": "Lovable vs Bolt.new 2026: We Built the Same App on Both",
        "meta": "We built the same SaaS app on Lovable and Bolt.new. Honest comparison of pricing, AI code quality, deployment, and who should use which.",
        "quick_answer": "Bolt.new wins for production-grade code and Vercel deployment; Lovable wins for rapid prototyping and UI polish. If you need a production MVP, pick Bolt.new. If you need a demo in 10 minutes, pick Lovable. Bolt.new starts at $20/mo; Lovable starts at $25/mo.",
        "h2s": [
            "Quick Verdict: Which Should You Pick?",
            "What Are Lovable and Bolt.new?",
            "Side-by-Side Comparison Table",
            "AI Code Quality: Same Prompt, Different Results",
            "Pricing Breakdown (Real Monthly Cost)",
            "Deployment & Hosting",
            "Who Should Use Lovable?",
            "Who Should Use Bolt.new?",
            "Common Pain Points & Fixes",
            "Final Verdict",
        ],
        "painpoints": [
            "AI-generated code has hardcoded values that break after deployment",
            "Free tier has strict daily limits that kill productivity mid-project",
            "Exported code requires heavy refactoring before it's production-ready",
        ],
        "rec_tools": ["Lovable", "Bolt.new", "v0.dev", "Cursor", "Replit"],
        "internal_links": ["/blog/cursor-alternatives-2026/", "/blog/best-ai-code-generators/", "/blog/windsurf-vs-cursor/"],
    },
    "claude-37-vs-gpt4o": {
        "slug": "claude-37-vs-gpt4o",
        "keyword": "Claude 3.7 vs GPT-4o",
        "type": "comparison",
        "category": "LLM comparison",
        "title": "Claude 3.7 Sonnet vs GPT-4o 2026: Side-by-Side Benchmarks",
        "meta": "We benchmarked Claude 3.7 Sonnet vs GPT-4o on coding, reasoning, writing, and speed. See which LLM wins for your use case in 2026.",
        "quick_answer": "Claude 3.7 Sonnet leads on long-context coding (200K tokens) and nuanced writing; GPT-4o wins on real-time multimodal and speed. For coding agents, Claude 3.7; for vision-heavy tasks, GPT-4o. Both cost ~$3 per million input tokens.",
        "h2s": [
            "Quick Verdict Table",
            "Benchmarks We Ran",
            "Coding: Claude 3.7 vs GPT-4o",
            "Long Context & Document Analysis",
            "Speed & Latency",
            "Multimodal (Images, Audio, Video)",
            "Pricing Comparison",
            "Who Should Use Claude 3.7?",
            "Who Should Use GPT-4o?",
            "Final Verdict",
        ],
        "painpoints": [
            "Long context windows silently truncate documents past advertised limits",
            "Coding benchmarks don't reflect real-world debugging on legacy codebases",
            "API rate limits cause pipeline failures under production load",
        ],
        "rec_tools": ["Claude 3.7 Sonnet", "GPT-4o", "Claude 3.5", "GPT-4o mini", "Gemini 2.0"],
        "internal_links": ["/blog/chatgpt-alternatives-2026/", "/blog/claude-alternatives-2026/", "/blog/best-ai-chatbots/"],
    },
    "synthesia-vs-heygen": {
        "slug": "synthesia-vs-heygen",
        "keyword": "Synthesia vs HeyGen",
        "type": "comparison",
        "category": "AI video generation",
        "title": "Synthesia vs HeyGen 2026: We Tested Both on the Same Script",
        "meta": "Synthesia vs HeyGen compared on avatars, voice quality, pricing, and enterprise features. We used the exact same script on both platforms.",
        "quick_answer": "Synthesia wins for enterprise training videos and multilingual support (120+ languages); HeyGen wins for consumer-facing social videos and lip-sync accuracy. Synthesia starts at $22/mo; HeyGen starts at $24/mo. Pick Synthesia for L&D, HeyGen for marketing.",
        "h2s": [
            "Quick Verdict",
            "What We Tested",
            "Avatar Quality & Realism",
            "Voice & Multilingual Support",
            "Pricing Breakdown",
            "Enterprise Features (SSO, GDPR, custom avatars)",
            "Who Should Use Synthesia?",
            "Who Should Use HeyGen?",
            "Pain Points & Limitations",
            "Final Verdict",
        ],
        "painpoints": [
            "AI avatars have unnatural hand gestures and blinking cadence",
            "Custom avatar upload requires 10+ minutes of footage and still looks robotic",
            "Pronunciation of brand names and technical terms is consistently wrong",
        ],
        "rec_tools": ["Synthesia", "HeyGen", "Runway ML", "D-ID", "Elai.io"],
        "internal_links": ["/blog/runway-vs-pika-2026/", "/blog/best-ai-video-generators/", "/blog/best-ai-avatar-generators/"],
    },
    "runway-alternatives": {
        "slug": "runway-alternatives",
        "keyword": "Runway ML alternatives",
        "type": "alternatives",
        "category": "AI video editing",
        "title": "8 Best Runway ML Alternatives in 2026 (Tested & Ranked)",
        "meta": "Tired of Runway ML credits burning through? We tested 8 alternatives for text-to-video, image-to-video, and AI editing. See which fits your budget.",
        "quick_answer": "Pika 2.0 wins for text-to-video quality; Kling AI wins for motion smoothness; Canva AI wins for integrated editing. Runway Gen-3 is still the most polished editor but costs $28/mo. Free option: Pika offers 30 credits/day free.",
        "h2s": [
            "Quick Answer: Best Runway Alternatives",
            "Why Look for a Runway Alternative?",
            "#1: Pika 2.0 — Best Text-to-Video",
            "#2: Kling AI — Best Motion Smoothness",
            "#3: Canva AI Video — Best Integrated Editor",
            "#4: Stable Video Diffusion — Best Open-Source",
            "#5: Luma Dream Machine — Best Camera Control",
            "Comparison Table",
            "Who Should Use Which?",
            "FAQs",
        ],
        "painpoints": [
            "Runway credit system is confusing — short clips eat 5+ credits instantly",
            "Generated videos have watermarks on the free tier",
            "Consistency across shots is nearly impossible",
        ],
        "rec_tools": ["Pika 2.0", "Kling AI", "Canva AI", "Luma Dream Machine", "Stable Video Diffusion"],
        "internal_links": ["/blog/runway-vs-pika-2026/", "/blog/best-ai-video-generators/", "/blog/midjourney-v7-vs-dall-e-3-ecommerce/"],
    },
    "gemini-vs-perplexity": {
        "slug": "gemini-vs-perplexity",
        "keyword": "Gemini vs Perplexity",
        "type": "comparison",
        "category": "AI search",
        "title": "Gemini vs Perplexity 2026: Which AI Search Is Actually Better?",
        "meta": "We tested Gemini Advanced vs Perplexity Pro on research, coding, and fact-checking. Real head-to-head results with sources cited.",
        "quick_answer": "Perplexity Pro wins for cited research and real-time web grounding; Gemini Advanced wins for multimodal analysis and Google Workspace integration. Perplexity starts at $20/mo; Gemini Advanced is $19.99/mo. Pick Perplexity for research, Gemini for daily use.",
        "h2s": [
            "Quick Verdict",
            "What We Tested",
            "Research & Citation Quality",
            "Real-Time Web Access",
            "Multimodal & File Analysis",
            "Speed & Response Quality",
            "Pricing",
            "Who Should Use Perplexity?",
            "Who Should Use Gemini?",
            "Final Verdict",
        ],
        "painpoints": [
            "Perplexity fabricates citations that look real but don't exist",
            "Gemini misses recent news that Google Search would surface",
            "Both tools hallucinate technical specifications",
        ],
        "rec_tools": ["Perplexity Pro", "Gemini Advanced", "ChatGPT Search", "Copilot", "You.com"],
        "internal_links": ["/blog/perplexity-vs-chatgpt/", "/blog/chatgpt-alternatives-2026/", "/blog/best-ai-search-tools/"],
    },
    "beautiful-ai-alternatives": {
        "slug": "beautiful-ai-alternatives",
        "keyword": "Beautiful.ai alternatives",
        "type": "alternatives",
        "category": "AI presentation",
        "title": "7 Best Beautiful.ai Alternatives in 2026 (Free & Paid)",
        "meta": "Tired of Beautiful.ai's rigid templates? We tested 7 alternatives including Canva, Tome, and Gamma. See which AI presentation tool fits your workflow.",
        "quick_answer": "Gamma wins for quick deck generation from text prompts; Canva AI wins for design flexibility; Tome wins for storytelling. Beautiful.ai starts at $12/mo. Free option: Gamma offers 400 credits/month free.",
        "h2s": [
            "Quick Answer",
            "Why Look Beyond Beautiful.ai?",
            "#1: Gamma — Best Prompt-to-Deck",
            "#2: Canva AI — Best Design Flexibility",
            "#3: Tome — Best Storytelling",
            "#4: Presentations.AI — Best PowerPoint Import",
            "#5: Decktopus — Best for Business Proposals",
            "Comparison Table",
            "Pricing",
            "FAQs",
        ],
        "painpoints": [
            "Beautiful.ai templates look the same on every deck",
            "Custom animations are nearly impossible",
            "Export to PowerPoint loses all AI formatting",
        ],
        "rec_tools": ["Gamma", "Canva AI", "Tome", "Presentations.AI", "Decktopus"],
        "internal_links": ["/blog/canva-ai-alternatives-2026/", "/blog/best-ai-presentation-makers/", "/blog/canva-pro-free-for-students/"],
    },
    "devin-ai-review": {
        "slug": "devin-ai-review",
        "keyword": "Devin AI review",
        "type": "review",
        "category": "AI software engineer",
        "title": "Devin AI Review 2026: Is the AI Software Engineer Worth $500/mo?",
        "meta": "We tested Devin AI on real bug fixes, feature builds, and code reviews. Honest review of Cognition's AI software engineer — what works, what doesn't.",
        "quick_answer": "Devin AI handles well-scoped bug fixes and boilerplate features impressively, but fails on complex architecture and legacy codebases. At $500/mo (200 compute units), it's expensive. Better for junior-level tasks than senior engineering. Cursor + Claude Code is more capable for the price.",
        "h2s": [
            "Quick Answer",
            "What Is Devin AI?",
            "What We Tested",
            "Real Test Results: Bug Fixes",
            "Real Test Results: Feature Builds",
            "Strengths",
            "Weaknesses & Limitations",
            "Pricing Breakdown",
            "Devin vs Cursor vs Claude Code",
            "Who Should Buy Devin?",
        ],
        "painpoints": [
            "Devin goes silent for 20+ minutes with no progress visibility",
            "Complex multi-file changes often fail and need human handoff",
            "Pricing credits vanish faster than advertised",
        ],
        "rec_tools": ["Devin AI", "Cursor", "Claude Code", "GitHub Copilot", "Windsurf"],
        "internal_links": ["/blog/cursor-vs-github-copilot-2026/", "/blog/cursor-alternatives-2026/", "/blog/windsurf-vs-cursor/"],
    },
    "writesonic-alternatives": {
        "slug": "writesonic-alternatives",
        "keyword": "Writesonic alternatives",
        "type": "alternatives",
        "category": "AI writing",
        "title": "8 Best Writesonic Alternatives in 2026 (Ranked by Use Case)",
        "meta": "Tired of Writesonic? We tested 8 alternatives for blog writing, SEO content, and marketing copy. See which AI writer beats Writesonic in 2026.",
        "quick_answer": "Jasper wins for brand voice marketing copy; ChatGPT Plus wins for raw writing quality; Surfer SEO wins for content optimization. Writesonic starts at $13/mo. Free option: ChatGPT free tier handles most writing tasks better.",
        "h2s": [
            "Quick Answer",
            "Why Look Beyond Writesonic?",
            "#1: Jasper — Best Brand Voice",
            "#2: ChatGPT Plus — Best Writing Quality",
            "#3: Surfer SEO — Best Content Optimization",
            "#4: Claude — Best Long-Form",
            "#5: Copymatic — Best Affordable Option",
            "Comparison Table",
            "Pricing",
            "FAQs",
        ],
        "painpoints": [
            "Writesonic outputs read like generic AI content",
            "SEO optimization tools are weaker than dedicated SEO platforms",
            "Team collaboration features are limited",
        ],
        "rec_tools": ["Jasper", "ChatGPT Plus", "Surfer SEO", "Claude", "Copymatic"],
        "internal_links": ["/blog/jasper-vs-copy-ai/", "/blog/best-ai-writing-tools/", "/blog/quillbot-alternatives/"],
    },
    "motion-ai-alternatives": {
        "slug": "motion-ai-alternatives",
        "keyword": "Motion AI alternatives",
        "type": "alternatives",
        "category": "AI calendar scheduling",
        "title": "7 Best Motion AI Alternatives in 2026 (Free & Paid)",
        "meta": "Motion AI is great but expensive. We tested 7 alternatives including Reclaim, Clockwise, and Trevor. See which AI calendar saves you time without the $34/mo price tag.",
        "quick_answer": "Reclaim.ai wins for Google Calendar integration and free tier; Clockwise wins for team focus time; Trevor wins for visual planning. Motion starts at $34/mo. Free option: Reclaim offers 14-day free trial with full features.",
        "h2s": [
            "Quick Answer",
            "Why Look for a Motion Alternative?",
            "#1: Reclaim.ai — Best Free Option",
            "#2: Clockwise — Best for Teams",
            "#3: Trevor — Best Visual Planning",
            "#4: Akiflow — Best All-in-One",
            "#5: Sunsama — Best Time Blocking",
            "Comparison Table",
            "Pricing",
            "FAQs",
        ],
        "painpoints": [
            "Motion's AI reschedules meetings without asking",
            "Calendar conflicts cause double-booking",
            "No free tier makes it hard to test before committing",
        ],
        "rec_tools": ["Reclaim.ai", "Clockwise", "Trevor", "Akiflow", "Sunsama"],
        "internal_links": ["/blog/best-ai-productivity-tools/", "/blog/notion-ai-vs-obsidian-ai/", "/blog/best-ai-calendar-tools/"],
    },
    "clearscope-alternatives": {
        "slug": "clearscope-alternatives",
        "keyword": "Clearscope alternatives",
        "type": "alternatives",
        "category": "SEO content optimization",
        "title": "6 Best Clearscope Alternatives in 2026 (Cheaper & Better)",
        "meta": "Clearscope costs $189/mo minimum. We tested 6 alternatives including Surfer SEO, Frase, and RankMath. See which SEO content tool gives better ROI.",
        "quick_answer": "Surfer SEO wins for comprehensive SERP analysis; Frase wins for AI content briefs on a budget; Rank Math wins for WordPress integration. Clearscope starts at $189/mo. Best value: Frase at $15/mo for similar features.",
        "h2s": [
            "Quick Answer",
            "Why Look Beyond Clearscope?",
            "#1: Surfer SEO — Best SERP Analysis",
            "#2: Frase — Best Budget Option",
            "#3: Rank Math — Best WordPress Integration",
            "#4: MarketMuse — Best Enterprise",
            "#5: NeuronWriter — Best AI Writing",
            "Comparison Table",
            "Pricing",
            "FAQs",
        ],
        "painpoints": [
            "Clearscope minimum $189/mo is out of reach for solo creators",
            "Content grading scores don't correlate with actual rankings",
            "No built-in AI writing — you still need ChatGPT",
        ],
        "rec_tools": ["Surfer SEO", "Frase", "Rank Math", "MarketMuse", "NeuronWriter"],
        "internal_links": ["/blog/best-ai-seo-tools/", "/blog/writesonic-alternatives/", "/blog/best-ai-content-creation-tools/"],
    },
    "quillbot-alternatives": {
        "slug": "quillbot-alternatives",
        "keyword": "QuillBot alternatives",
        "type": "alternatives",
        "category": "AI paraphrasing",
        "title": "7 Best QuillBot Alternatives in 2026 (Paraphrasing & Rewriting)",
        "meta": "QuillBot is great but limited. We tested 7 alternatives for paraphrasing, grammar checking, and AI rewriting. See which tool beats QuillBot in 2026.",
        "quick_answer": "GrammarlyGO wins for grammar + rewriting combined; Undetectable AI wins for humanizing AI text; Wordtune wins for tone adjustment. QuillBot Premium is $8/mo. Free option: Grammarly free tier handles basic paraphrasing.",
        "h2s": [
            "Quick Answer",
            "Why Look Beyond QuillBot?",
            "#1: GrammarlyGO — Best All-in-One",
            "#2: Undetectable AI — Best Humanizer",
            "#3: Wordtune — Best Tone Control",
            "#4: Paraphraser.io — Best Free",
            "#5: SpinBot — Best Basic Spinning",
            "Comparison Table",
            "Pricing",
            "FAQs",
        ],
        "painpoints": [
            "QuillBot changes meaning during paraphrasing",
            "Free tier has strict word limits",
            "Grammar checking is weaker than Grammarly",
        ],
        "rec_tools": ["GrammarlyGO", "Undetectable AI", "Wordtune", "Paraphraser.io", "SpinBot"],
        "internal_links": ["/blog/best-ai-grammar-checkers/", "/blog/writesonic-alternatives/", "/blog/best-ai-writing-tools/"],
    },
}

written = []
for slug, brief in BRIEFS.items():
    # Get PAA from research data
    paa = research.get(slug, {}).get("paa", [])
    competitors = research.get(slug, {}).get("top_competitors", [])
    
    # Build FAQ from PAA
    faq_items = []
    for q in paa[:5]:
        faq_items.append(f"### {q}\n\nBrief answer: This depends on your specific use case. See the detailed comparison above for the full breakdown.")
    
    content = f"""# Content Brief: {brief['keyword']}

- **Slug**: {brief['slug']}
- **Target Keyword**: {brief['keyword']}
- **Content Type**: {brief['type']}
- **Category**: {brief['category']}
- **KD**: 1-4 (P0, low competition)
- **Title**: {brief['title']}
- **Meta Description**: {brief['meta']}

## Quick Answer
{brief['quick_answer']}

## Key Takeaways
1. {brief['quick_answer'].split('.')[0]}.
2. Pricing comparison and who should use each tool.
3. Real test results, not marketing claims.

## H2 Outline
"""
    for i, h2 in enumerate(brief["h2s"], 1):
        content += f"{i}. {h2}\n"
    
    content += f"""
## Must Include
- Comparison table (features, pricing, pros/cons)
- At least 3 A vs B conclusions with specific use cases
- How We Tested section (scenario-based)
- Who Should Look Elsewhere section
- FAQ with 5+ questions (from PAA below)
- Real pricing calculations (monthly x 12)
- At least 2 affiliate links (rel="sponsored")
- Internal links: {', '.join(brief['internal_links'])}
- Recommended tools: {', '.join(brief['rec_tools'])}

## Must-Fix Pain Points
"""
    for i, p in enumerate(brief["painpoints"], 1):
        content += f"{i}. {p}\n"
    
    content += f"""
## FAQ (from PAA)
"""
    for faq in faq_items:
        content += f"\n{faq}\n"
    
    content += f"""
## Competitor Analysis (from SERP)
"""
    for c in competitors[:3]:
        content += f"- {c['title']}: {c['url']}\n"
    
    content += f"""
## Word Count Target: 2500-3500
## Language: 100% English (US audience)
"""
    
    filepath = f"iteration_center/content_briefs/{slug}_input.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    written.append(slug)
    print(f"  Written: {filepath}")

print(f"\n=== {len(written)} briefs generated ===")
for s in written:
    print(f"  - {s}")
