# -*- coding: utf-8 -*-
import io, json, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))

def read_md(slug):
    suf = '_NEW.md' if slug in ('ai-video-generator-credits-burn-fast-2026', 'ai-tools-not-worth-the-money-2026') else '_REWRITE.md'
    return io.open(base + r'\content_drafts\2026-10-13-' + slug + suf, encoding='utf-8').read()

def faq_from_md(md):
    faqs = []
    parts = md.split('## Frequently Asked Questions')[1].split('## Conclusion')[0]
    qs = re.findall(r'^### (.+)$', parts, re.M)
    for q in qs:
        body = parts.split('### ' + q + '\n')[1]
        a = body.split('\n### ')[0].strip().replace('\n', ' ')
        faqs.append({'question': q, 'answer': a[:300]})
    return faqs[:5]

def quick_answer(md):
    lines = md.split('\n')
    for i, l in enumerate(lines):
        if l.startswith('**Quick Answer'):
            buf = l.strip('*').strip()
            for l2 in lines[i+1:]:
                if l2.startswith('#') or l2.strip() == '':
                    break
                buf += ' ' + l2.strip()
            return buf[:400]
    return ''

def imgs(md):
    return re.findall(r'!\[[^\]]*\]\((/screenshots/[^)]+)\)', md)

def internals(md):
    return re.findall(r'\]\(/blog/([^)]+)/\)', md)

def externals(md):
    return re.findall(r'\]\((https?://[^)]+)\)', md)

# new articles
new_articles = {
    'ai-video-generator-credits-burn-fast-2026': {
        'title': 'Why AI Video Generators Burn Through Credits Fast in 2026',
        'excerpt_hint': 'AI video generators burn credits fast because every re-roll, upscale, and extension charges separately',
        'internalLinks': ['best-ai-video-generators-2026', 'best-paid-ai-tools-worth-buying-2026', 'midjourney-alternatives-2026', 'suno-alternatives-2026', 'runway-vs-pika-2026'],
        'affiliateLinks': ['https://runwayml.com/pricing', 'https://pika.art/pricing', 'https://hailuoai.video/'],
        'keyTakeaways': [
            'AI video generators price in credits: Runway 125/625/2,250/9,500 per month ($0-$76), Pika 0/900/3,150/8,550 ($0-$95), Hailuo from $9.99 with 3,000 free credits (October 2026 official pages)',
            'One generation is rarely one charge — re-rolls, upscales, and extensions multiply consumption by 3-4x, which is why credits "burn fast"',
            'The re-roll discipline (written prompts, low-res tests, reference images, batching) cuts credit consumption 40-60%',
            'Start on free allowances (Hailuo 3,000 credits or Runway 125) and subscribe only when the free tier blocks real output'
        ],
    },
    'ai-tools-not-worth-the-money-2026': {
        'title': 'AI Tools Not Worth the Money in 2026: Honest Pricing Review',
        'excerpt_hint': 'Most AI tool subscriptions fail the value test through tier mismatch, not bad software',
        'internalLinks': ['best-paid-ai-tools-worth-buying-2026', 'cursor_ai_review', 'devin-ai-review', 'midjourney-v7-review-2026', 'elevenlabs-review-2026', 'ai-video-generator-credits-burn-fast-2026', 'best-ai-tools-for-beginners-2026'],
        'affiliateLinks': ['https://docs.midjourney.com/hc/en-us/articles/115010738928-Plan-Information', 'https://cursor.com/pricing'],
        'keyTakeaways': [
            'Midjourney: Basic $10 (200 fast-GPU min), Standard $30 (15 hr), Pro $60 (30 hr + Stealth), Mega $120 (60 hr); 20% annual discount (October 2026 official docs)',
            'Cursor: Hobby free, Individual $20/mo (Pro/Pro+/Ultra), Teams $40/user/mo, Enterprise custom (October 2026 official pricing)',
            'The value test: real monthly output, quota utilization, substitutability — subscriptions fail when users pay for capacity they never consume',
            'Apply the 90-day keep-vs-cut audit: cut every subscription that produced no shippable output in the last 90 days'
        ],
    },
}

# updates for rewritten article
updates = {
    'runway-vs-pika-2026': {
        'title': 'Runway vs Pika 2026: Which AI Video Generator Wins?',
        'internalLinks': ['ai-video-generator-credits-burn-fast-2026', 'best-ai-video-generators-2026', 'best-paid-ai-tools-worth-buying-2026', 'midjourney-v7-review-2026'],
        'affiliateLinks': ['https://runwayml.com/pricing', 'https://pika.art/pricing'],
        'keyTakeaways': [
            'Runway is the production platform: Free 125 / Standard $12 for 625 / Pro $28 for 2,250 (Popular) / Max $76 for 9,500 with rollover (October 2026 official pricing)',
            'Pika is the volume engine: Free packs / Starter $10 for 900 / Creator $35 for 3,150 with 8 parallel (Best Value) / Fancy $95 for 8,550 unlimited parallel',
            'Choose Runway when quality and iteration matter (enterprise partners Adobe/LIONSGATE/Amazon), Pika when parallel volume matters',
            'Start on the free tier of both, run the same five prompts side by side, and upgrade only where the free allowance blocks real output'
        ],
    },
}

for slug, meta in new_articles.items():
    md = read_md(slug)
    entry = {
        'slug': slug,
        'title': meta['title'],
        'description': meta['excerpt_hint'][:160],
        'content': md,
        'excerpt': meta['excerpt_hint'],
        'quickAnswer': quick_answer(md),
        'keyTakeaways': meta['keyTakeaways'],
        'faq': faq_from_md(md),
        'internalLinks': meta['internalLinks'],
        'affiliateLinks': meta['affiliateLinks'],
        'hasRealScreenshots': True,
        'screenshotCount': len(imgs(md)),
        'wordCount': len(re.findall(r"[A-Za-z][A-Za-z'-]*", re.split(r'\n## Self-Check', md)[0])),
        'date': '2026-10-13',
        'publishedAt': '2026-10-13',
        'category': 'AI Tools',
        'tags': ['review', 'pricing', 'comparison'],
        'featured': False,
    }
    posts.append(entry)
    print('APPEND', slug, '| words:', entry['wordCount'], '| imgs:', entry['screenshotCount'], '| faq:', len(entry['faq']))

for slug, meta in updates.items():
    hit = next((p for p in posts if p.get('slug') == slug), None)
    if hit is None:
        print('MISS', slug); continue
    md = read_md(slug)
    hit['title'] = meta['title']
    hit['content'] = md
    hit['quickAnswer'] = quick_answer(md)
    hit['excerpt'] = quick_answer(md)[:200]
    hit['keyTakeaways'] = meta['keyTakeaways']
    hit['faq'] = faq_from_md(md)
    hit['internalLinks'] = meta['internalLinks']
    hit['affiliateLinks'] = meta['affiliateLinks']
    hit['hasRealScreenshots'] = True
    hit['screenshotCount'] = len(imgs(md))
    hit['wordCount'] = len(re.findall(r"[A-Za-z][A-Za-z'-]*", re.split(r'\n## Self-Check', md)[0]))
    hit['date'] = '2026-10-13'
    hit['publishedAt'] = '2026-10-13'
    print('UPDATE', slug, '| words:', hit['wordCount'], '| imgs:', hit['screenshotCount'])

io.open(base + r'\data\posts.json', 'w', encoding='utf-8').write(json.dumps(posts, ensure_ascii=False, indent=2))
print('posts.json saved, total:', len(posts))
