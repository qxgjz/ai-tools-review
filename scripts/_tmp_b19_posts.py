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
            # gather the rest of that line plus following lines until blank/heading
            buf = l.strip('*').strip()
            for l2 in lines[i+1:]:
                if l2.startswith('#') or l2.strip() == '':
                    break
                buf += ' ' + l2.strip()
            return buf[:400]
    return ''

updates = {
    'clearscope-alternatives': {
        'title': '6 Best Clearscope Alternatives in 2026 (Cheaper & Better)',
        'wordCount': 2098, 'screenshotCount': 2,
        'internalLinks': ['best-ai-tools-for-beginners-2026', 'what-is-an-ai-agent', 'best-ai-agents-2026', 'quillbot-alternatives'],
        'affiliateLinks': ['https://www.clearscope.io/pricing', 'https://ahrefs.com/pricing', 'https://surferseo.com/pricing/', 'https://www.frase.io/pricing/'],
        'keyTakeaways': ['Clearscope costs $129/month (Essentials, 50 queries) and $399/month (Business, 300 queries) per the official pricing page captured October 2026', 'Ahrefs is the best Clearscope alternative when its suite is already in the stack — the Content Optimizer covers briefs without a second subscription', 'Surfer SEO is the data-first option, MarketMuse covers site-level modeling, and Frase or RankIQ are the budget picks', 'The r/SaaS keep-vs-cut rule applies: trial one tool for a month and keep it only if the briefs change what you write'],
    },
    'gemini_38_flash_review': {
        'title': 'Gemini 3.8 Flash Review 2026: Speed, Pricing, and Is It Worth It?',
        'wordCount': 2088, 'screenshotCount': 2,
        'internalLinks': ['best-ai-agents-2026', 'claude-vs-gemini-2026-comparison', 'gemini-vs-chatgpt-2026', 'chatgpt-vs-claude-2026-comparison', 'best-ai-tools-for-beginners-2026'],
        'affiliateLinks': ['https://ai.google.dev', 'https://ai.google.dev/pricing'],
        'keyTakeaways': ['Gemini 3.8 Flash is Google\'s speed-and-scale frontier model, promoted on the official developer homepage as "frontier intelligence built for speed and scale"', 'The official pricing page confirms a free tier plus a paid tier with the banner "Gemini 3.8 Flash is now available" (captured October 2026)', 'Flash wins high-volume, latency-sensitive workloads: coding assistance, RAG, summarization, and agent tool calls', 'Teams should route routine work to Flash and reserve Pro for deep reasoning, per the keep-vs-cut discipline from r/SaaS founders'],
    },
    'dify-vs-langchain-2026': {
        'title': 'Dify vs LangChain 2026: Which AI App Builder Should You Choose?',
        'wordCount': 2061, 'screenshotCount': 2,
        'internalLinks': ['what-is-an-ai-agent', 'how-to-build-an-ai-agent', 'best-ai-agents-2026', 'ai-agent-vs-chatbot-2026', 'best-ai-coding-tools-beginners'],
        'affiliateLinks': ['https://dify.ai', 'https://www.langchain.com'],
        'keyTakeaways': ['Dify is the platform for production-ready agentic workflows — visual builder, built-in RAG, deploy on cloud, VPC, or self-hosted', 'LangChain is the developer framework with LangSmith Engine observability — full code control plus production tracing', 'Product teams and non-engineers ship faster on Dify; engineering teams that need code ownership choose LangChain', 'Prototype in Dify and graduate to LangChain is the strongest practical pattern in 2026'],
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
