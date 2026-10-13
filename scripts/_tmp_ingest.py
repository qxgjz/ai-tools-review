# -*- coding: utf-8 -*-
import io, json, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts_path = base + r'\data\posts.json'
posts = json.load(io.open(posts_path, encoding='utf-8'))
drafts = base + r'\content_drafts'

def read(fn):
    return io.open(drafts + '\\' + fn, encoding='utf-8').read()

b = read('2026-10-10-best-ai-tools-for-beginners-2026_DRAFT.md')
a = read('2026-10-10-agenta-ai-review-2026_DRAFT.md')
c = read('2026-10-10-cursor-vs-windsurf-2026_REWRITE.md')

def wc(md):
    return len(re.findall(r"[A-Za-z0-9']+", md))

new_b = {
    "id": "best-ai-tools-for-beginners-2026-153",
    "slug": "best-ai-tools-for-beginners-2026",
    "title": "Best AI Tools for Beginners 2026 (Without a Tech Background)",
    "category": "AI Tools",
    "date": "2026-10-10",
    "tags": ["best AI tools", "AI tools for beginners", "ChatGPT free", "Claude free", "Gemini free"],
    "description": "Best AI tools for beginners 2026: ChatGPT free (unlimited GPT-6 chats), Claude for writing, Canva for design, Notion and Grammarly — plus a 30-day plan and what to pay for.",
    "content": b,
    "wordCount": wc(b),
    "screenshotCount": 2,
    "hasRealScreenshots": True,
    "status": "draft",
    "meta": {"title": "Best AI Tools for Beginners 2026 (Without a Tech Background)", "description": "Best AI tools for beginners 2026: ChatGPT free (unlimited GPT-6 chats), Claude for writing, Canva for design, Notion and Grammarly — plus a 30-day plan and what to pay for.", "wordCount": wc(b), "screenshotCount": 2, "hasRealScreenshots": True}
}
new_a = {
    "id": "agenta-ai-review-2026-154",
    "slug": "agenta-ai-review-2026",
    "title": "Agenta AI Review 2026: Is This the Best Open-Source Agent Builder?",
    "category": "AI Agents",
    "date": "2026-10-10",
    "tags": ["Agenta", "open-source AI agent builder", "AI agents", "self-hosted AI", "LLM observability"],
    "description": "Agenta AI review 2026: MIT-licensed open-source agent workspace, self-hosted free forever, cloud from $0 (Hobby) to $29 Pro and $299 Business — who it fits and who it doesn't.",
    "content": a,
    "wordCount": wc(a),
    "screenshotCount": 2,
    "hasRealScreenshots": True,
    "status": "draft",
    "meta": {"title": "Agenta AI Review 2026: Is This the Best Open-Source Agent Builder?", "description": "Agenta AI review 2026: MIT-licensed open-source agent workspace, self-hosted free forever, cloud from $0 (Hobby) to $29 Pro and $299 Business — who it fits and who it doesn't.", "wordCount": wc(a), "screenshotCount": 2, "hasRealScreenshots": True}
}
posts.append(new_b)
posts.append(new_a)

# update cursor-vs-windsurf entry
updated = False
for p in posts:
    if p.get('slug') == 'cursor-vs-windsurf-2026':
        p['title'] = 'Cursor vs Windsurf 2026: Which AI Code Editor Is Better?'
        p['excerpt'] = 'We tested Cursor and Windsurf head-to-head in 2026, captured both official pricing pages, and compared free tiers, agent modes, quotas, and costs — here is which AI code editor to pick and why.'
        p['content'] = c
        p['wordCount'] = wc(c)
        p['hasRealScreenshots'] = True
        p['screenshotCount'] = 2
        p['quickAnswer'] = 'Cursor is the better AI code editor for most developers in 2026 (stable $20 pricing, VS Code familiarity, deep multi-model AI). Windsurf (now under the Devin brand) is better for agent-first coding with free SWE-2 agent use and unlimited Tab on Pro. Start free on both; upgrade the one that earns $20.'
        p['keyTakeaways'] = ['Cursor = safer default: VS Code fork, $20/mo Individual, large ecosystem', 'Windsurf = more agentic: free SWE-2 on Pro, unlimited Tab, Teams from $80', 'Both have usable free tiers; set usage guardrails to avoid cost creep']
        p['faq'] = ['Q: Is Cursor or Windsurf free in 2026? A: Both. Cursor Hobby is $0; Windsurf Free is $0 with light quota and limited models.',
                    'Q: How much does Cursor cost? A: Free (Hobby), $20/mo Individual, $40/user Teams, custom Enterprise.',
                    'Q: How much does Windsurf cost in 2026? A: Free $0, Pro $20/mo, Max $200/mo, Teams from $80/seat, per the official (Devin-branded) pricing page.',
                    'Q: Did Windsurf merge with Devin? A: Yes — in 2026 Windsurf pricing and docs now carry the Devin brand.',
                    'Q: Which is better for beginners? A: Cursor — VS Code fork, huge tutorial ecosystem, free Hobby plan.']
        updated = True
        break
assert updated

io.open(posts_path, 'w', encoding='utf-8').write(json.dumps(posts, ensure_ascii=False, indent=1))
print('posts total now:', len(posts))
for p in posts:
    if p.get('id','').endswith(('153','154')) or p.get('slug')=='cursor-vs-windsurf-2026':
        print('  in:', p['slug'], '| wc:', p['wordCount'])
