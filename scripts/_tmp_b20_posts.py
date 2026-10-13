# -*- coding: utf-8 -*-
import io, json, re
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))
def read_md(slug):
    return io.open(base + r'\content_drafts\2026-10-12-' + slug + '_REWRITE.md', encoding='utf-8').read()

def faq_from_md(md):
    faqs = []
    parts = md.split('## Frequently Asked Questions')[1].split('## Conclusion')[0]
    qs = re.findall(r'^### (.+)$', parts, re.M)
    for q in qs:
        body = parts.split('### ' + q + '\n')[1]
        a = body.split('\n### ')[0].strip().replace('\n', ' ')
        faqs.append({'question': q, 'answer': a[:300]})
    return faqs[:5]

def first_para_after_quick(md):
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

updates = {
    'suno-review-2026': {
        'title': 'Suno AI Review 2026: Pricing, Features, and Is It Worth It?',
        'wordCount': 2159, 'screenshotCount': 2,
        'internalLinks': ['suno-alternatives', 'suno-alternatives-2026', 'best-ai-video-generators-2026', 'best-ai-voice-changers-content-creators', 'best-ai-tools-for-beginners-2026'],
        'affiliateLinks': ['https://suno.com', 'https://suno.com/pricing'],
        'keyTakeaways': ['Suno Free is $0/month with 50 daily credits, standard features, and uploads up to 8 minutes — no downloads or commercial rights', 'Pro is $8/month billed yearly (Most Popular) with 2,500 monthly credits, 20 downloads, and commercial use rights', 'Premier is $24/month billed yearly (Best Value) with 10,000 credits, 60 downloads, and Suno Studio with MIDI, effects, and automation', 'The Annual toggle saves 20%; subscribe when your output ships and stay free until it does, per the r/SaaS keep-vs-cut rule'],
    },
    'elevenlabs-review-2026': {
        'title': 'ElevenLabs Review 2026: Best AI Voice Generator & Cloning?',
        'wordCount': 2125, 'screenshotCount': 2,
        'internalLinks': ['elevenlabs-v2-review-2026', 'elevenlabs-vs-playht-2026', 'best-ai-voice-changers-content-creators', 'best-ai-tools-for-beginners-2026'],
        'affiliateLinks': ['https://elevenlabs.io', 'https://elevenlabs.io/pricing'],
        'keyTakeaways': ['ElevenLabs is the best AI voice generator in 2026 for production-grade speech; the AI Voice Changer page demonstrates transformation "while preserving your style"', 'Pricing runs from a free tier through Starter (30k credits), Creator (121k credits), Pro (600k credits with 44.1kHz PCM API output), to Scale at $299/month and Business at $990/month', 'The v4 banner promotes "our most emotive model yet" with 3x credits on Creator+ until October 12', 'Trial the free tier, measure your monthly burn, and pick the tier that covers it — the keep-vs-cut discipline from r/SaaS founders'],
    },
    'dify_ai_review': {
        'title': 'Dify AI Review 2026: Best Open-Source LLMOps?',
        'wordCount': 2143, 'screenshotCount': 2,
        'internalLinks': ['dify-vs-langchain-2026', 'dify-vs-coze-2026-comparison', 'what-is-an-ai-agent', 'how-to-build-an-ai-agent', 'best-ai-agents-2026'],
        'affiliateLinks': ['https://dify.ai', 'https://dify.ai/pricing'],
        'keyTakeaways': ['Dify is the best open-source AI app builder in 2026 for production-ready agentic workflows — the homepage calls it "the platform for production-ready agentic workflows"', 'Deploy on cloud, VPC, or self-hosted; the open-source self-hosted version is free, with cloud tiers Professional, Team, and Enterprise and 17% off annual billing', 'Dify owns the orchestration layer, so teams ship chatbots, RAG pipelines, and agents without building the stack', 'The HN warning applies: the visual canvas accelerates shipping but can hide pipeline logic, so keep agent graphs small and readable'],
    },
}
for slug, u in updates.items():
    hit = next((p for p in posts if p.get('slug') == slug), None)
    if hit is None:
        print(slug, 'NOT FOUND'); continue
    md = read_md(slug)
    hit['title'] = u['title']
    hit['content'] = md
    hit['quickAnswer'] = first_para_after_quick(md)
    hit['keyTakeaways'] = u['keyTakeaways']
    hit['faq'] = faq_from_md(md)
    hit['internalLinks'] = u['internalLinks']
    hit['affiliateLinks'] = u['affiliateLinks']
    hit['hasRealScreenshots'] = True
    hit['screenshotCount'] = u['screenshotCount']
    hit['wordCount'] = u['wordCount']
    hit['date'] = '2026-10-12'
    hit['publishedAt'] = '2026-10-12'
    hit['excerpt'] = hit['quickAnswer'][:200]
    print(slug, 'updated | len(content):', len(md))
io.open(base + r'\data\posts.json', 'w', encoding='utf-8').write(json.dumps(posts, ensure_ascii=False, indent=2))
print('posts.json saved, total:', len(posts))
