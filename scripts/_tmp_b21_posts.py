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
    'devin-ai-review': {
        'title': 'Devin AI Review 2026: Pricing, Features, and Is It Worth It?',
        'wordCount': 2128, 'screenshotCount': 2,
        'internalLinks': ['cursor_ai_review', 'cursor-vs-github-copilot-2026', 'best-ai-coding-tools-beginners', 'best-ai-agents-2026', 'how-to-build-an-ai-agent'],
        'affiliateLinks': ['https://devin.ai', 'https://devin.ai/pricing'],
        'keyTakeaways': ['Devin is the strongest autonomous software engineer in 2026 — the homepage says it "runs in the cloud or on your machine, tests in its own browser, and won\'t stop until the PR is ready to merge"', 'Pricing: Free at $0 (light quota, limited models), Pro at $20/month (Popular, frontier models), Max at $200/month (significantly higher quotas); SWE-2 is the current model', 'Devin completes task-to-PR loops autonomously — explore, implement, verify in-browser, deliver the PR with evidence', 'Trial Free on real tasks and graduate to Pro when the agent finishes work consistently — the keep-vs-cut rule from r/SaaS founders'],
    },
    'claude-opus-4-vs-gpt-5-2026': {
        'title': 'Claude Opus 4 vs GPT-5: Which LLM Wins 2026?',
        'wordCount': 2131, 'screenshotCount': 2,
        'internalLinks': ['claude-alternatives-2026', 'chatgpt-alternatives-2026', 'claude-vs-gemini-2026-comparison', 'gemini-vs-chatgpt-2026', 'chatgpt-vs-claude-2026-comparison'],
        'affiliateLinks': ['https://claude.com/pricing', 'https://chatgpt.com/pricing'],
        'keyTakeaways': ['Claude and ChatGPT are both frontier reasoning platforms; the winner depends on workload — coding and long-context favor Claude, multi-modality favors ChatGPT', 'Claude pricing: Free $0, Pro $18/month billed annually ($22 monthly), Max from $110/month with 5x or 20x usage', 'ChatGPT pricing: Free (unlimited GPT-6 text chats), Go, Plus (advanced reasoning, Projects, Codex), Pro (3 usage tiers, GPT-6 Astra, Dot agent)', 'Pick the subscription that matches your dominant workload and cut the rest — the keep-vs-cut rule for frontier models'],
    },
    'perplexity-vs-chatgpt-2026': {
        'title': 'Perplexity AI vs ChatGPT 2026: Which Wins?',
        'wordCount': 2161, 'screenshotCount': 2,
        'internalLinks': ['chatgpt-alternatives-2026', 'chatgpt-vs-claude-2026-comparison', 'best-ai-comparison-tools-2026', 'best-ai-tools-for-beginners-2026', 'ai-agent-vs-chatbot-2026'],
        'affiliateLinks': ['https://www.perplexity.ai', 'https://www.perplexity.ai/hub/pricing', 'https://chatgpt.com/pricing'],
        'keyTakeaways': ['Perplexity is the sharper research tool — citations in every answer, deep research, model selection; ChatGPT is the broader assistant with GPT-6, Codex, image and voice', 'Perplexity pricing: Free $0, Pro $17/month billed annually (Popular, 4,000 bonus credits), Max $167/month billed annually', 'ChatGPT pricing: Free (unlimited GPT-6 text chats), Go, Plus, Pro (3 usage tiers, GPT-6 Astra, Dot agent)', 'Keep both free tiers — Perplexity for verification, ChatGPT for generation — until the workload proves which one earns a subscription'],
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
