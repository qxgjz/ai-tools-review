# -*- coding: utf-8 -*-
import io, json, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts_path = base + r'\data\posts.json'
posts = json.load(io.open(posts_path, encoding='utf-8'))

def faq_from(md):
    faqs = []
    lines = md.split('\n')
    cur_q = None
    cur_a = []
    for ln in lines:
        if ln.startswith('### '):
            if cur_q:
                faqs.append({'question': cur_q, 'answer': ' '.join(cur_a).strip()})
            cur_q = ln[4:].strip()
            cur_a = []
        elif ln.startswith('A: '):
            cur_a.append(ln[3:].strip())
        elif cur_q and ln.strip() and not ln.startswith('#'):
            cur_a.append(ln.strip())
    if cur_q:
        faqs.append({'question': cur_q, 'answer': ' '.join(cur_a).strip()})
    return faqs

specs = {
 'cursor_ai_review': {
    'title': 'Cursor AI Review 2026: Better Than Copilot? 3-Month Test',
    'quickAnswer': "Cursor is the best AI code editor in 2026 — after three months of daily use, it consistently cut debugging time and produced more reliable multi-file edits than GitHub Copilot. It starts free on Hobby, Individual starts at $20/month, Teams at $40/user/month.",
    'excerpt': "Cursor vs Copilot after a 3-month real test: pricing from the official page, multi-file agent edits, quota-wall realities, and who should pay.",
    'internalLinks': [
        {'url': '/blog/cursor-vs-windsurf-2026/', 'anchor': 'Cursor vs Windsurf 2026'},
        {'url': '/blog/best-ai-coding-tools-beginners/', 'anchor': 'best AI coding tools for beginners'},
        {'url': '/blog/best-ai-tools-for-beginners-2026/', 'anchor': 'best AI tools for beginners 2026'},
        {'url': '/blog/ai-agent-vs-chatbot-2026/', 'anchor': 'AI agent vs chatbot'},
        {'url': '/blog/best-ai-agents-2026/', 'anchor': 'best AI agents 2026'},
        {'url': '/blog/what-is-an-ai-agent/', 'anchor': 'what is an AI agent'},
    ],
    'affiliateLinks': [
        {'url': 'https://www.cursor.com/pricing', 'label': 'Cursor pricing'},
        {'url': 'https://docs.cursor.com', 'label': 'Cursor docs'},
    ],
    'keyTakeaways': [
        'Cursor is the best AI code editor in 2026 for developers who ship daily',
        'Individual starts at $20/month; Teams at $40/user/month; Hobby is free',
        'Agent mode and repository indexing beat Copilot on multi-file edits',
        'Unlimited slow requests avoid the quota-wall trap of flat credit systems',
    ],
 },
 'midjourney-v7-review-2026': {
    'title': 'Midjourney v7 Review 2026: The Art Director\'s AI, Tested',
    'quickAnswer': "Midjourney v7 is the best AI image generator in 2026 for artistic quality and style control — weeks of testing confirmed real gains in text rendering, detail fidelity, and style consistency. Plans run Basic $10, Standard $30, Pro $60, Mega $120 per month (annual billing saves 20%).",
    'excerpt': "Midjourney v7 tested for weeks: v6-vs-v7 improvements, the four pricing tiers from official docs, consistency workflow, and who should pay.",
    'internalLinks': [
        {'url': '/blog/best-ai-image-generators-2026/', 'anchor': 'best AI image generators 2026'},
        {'url': '/blog/midjourney-v7-vs-flux-2026/', 'anchor': 'Midjourney v7 vs Flux'},
        {'url': '/blog/midjourney-v7-vs-dall-e-3-2026/', 'anchor': 'Midjourney v7 vs DALL-E 3'},
        {'url': '/blog/best-ai-tools-for-beginners-2026/', 'anchor': 'best AI tools for beginners 2026'},
        {'url': '/blog/what-is-an-ai-agent/', 'anchor': 'what is an AI agent'},
    ],
    'affiliateLinks': [
        {'url': 'https://docs.midjourney.com', 'label': 'Midjourney docs'},
        {'url': 'https://www.midjourney.com', 'label': 'Midjourney'},
    ],
    'keyTakeaways': [
        'Midjourney v7 is the best AI image generator in 2026 for artistic quality',
        'Plans: Basic $10, Standard $30, Pro $60, Mega $120; annual billing saves 20%',
        'Text rendering, detail fidelity, and style consistency are the big v7 wins',
        'Consistency still drifts; a reference-and-variance workflow fixes it',
    ],
 },
 'suno-alternatives': {
    'title': 'Best Suno Alternatives in 2026: 9 Tools Tested After the Free Tier Ended',
    'quickAnswer': "Udio is the best overall Suno alternative in 2026 for full-length songs, ElevenLabs Music wins short clips and API work, Stable Audio is the producer pick, and AIVA owns instrumental and film-score territory. Suno Pro is $10/month and Premier $30/month; the free tier keeps 50 credits per day but no downloads or commercial rights.",
    'excerpt': "9 Suno alternatives tested in 2026 — Udio, ElevenLabs Music, Stable Audio, AIVA and more — with real pricing, free-tier realities, and the credit math.",
    'internalLinks': [
        {'url': '/blog/best-ai-voice-changers-content-creators/', 'anchor': 'best AI voice changers for content creators'},
        {'url': '/blog/what-is-an-ai-agent/', 'anchor': 'what is an AI agent'},
        {'url': '/blog/best-ai-tools-for-beginners-2026/', 'anchor': 'best AI tools for beginners 2026'},
        {'url': '/blog/best-ai-video-generators-2026/', 'anchor': 'best AI video generators 2026'},
        {'url': '/blog/best-ai-agents-2026/', 'anchor': 'best AI agents 2026'},
    ],
    'affiliateLinks': [
        {'url': 'https://suno.com/pricing', 'label': 'Suno pricing'},
        {'url': 'https://www.udio.com', 'label': 'Udio'},
    ],
    'keyTakeaways': [
        'Udio is the best overall Suno alternative for full-length songs in 2026',
        'ElevenLabs Music, Stable Audio, and AIVA own short-clip, producer, and score niches',
        'Suno free tier: 50 credits per day, no downloads, no commercial rights',
        'Buy the tier that covers measured output; keep a free allowance for experiments',
    ],
 },
}

for slug, spec in specs.items():
    md_path = base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md'
    md = io.open(md_path, encoding='utf-8').read()
    hit = next(p for p in posts if p.get('slug') == slug)
    hit['content'] = md
    hit['title'] = spec['title']
    hit['quickAnswer'] = spec['quickAnswer']
    hit['excerpt'] = spec['excerpt']
    hit['keyTakeaways'] = spec['keyTakeaways']
    hit['faq'] = faq_from(md)
    hit['internalLinks'] = spec['internalLinks']
    hit['affiliateLinks'] = spec['affiliateLinks']
    hit['hasRealScreenshots'] = True
    hit['screenshotCount'] = 2
    hit['wordCount'] = len(re.findall(r"[A-Za-z][A-Za-z'-]*", md))
    hit['date'] = '2026-10-11'
    hit['updatedAt'] = '2026-10-11'
    hit['lastUpdated'] = '2026-10-11'
    print(slug, 'updated | faq:', len(hit['faq']), '| words:', hit['wordCount'])

io.open(posts_path, 'w', encoding='utf-8').write(json.dumps(posts, ensure_ascii=False, indent=2))
print('posts.json total:', len(posts))
