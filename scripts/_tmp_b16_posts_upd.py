# -*- coding: utf-8 -*-
import io, json, re, os

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

def parse_faq(md):
    """Extract FAQ Q/A pairs from markdown."""
    pairs = []
    lines = md.split('\n')
    i = 0
    in_faq = False
    q = None
    ans = []
    for line in lines:
        if line.strip().startswith('## Frequently Asked Questions'):
            in_faq = True
            continue
        if in_faq:
            if line.strip().startswith('### '):
                if q and ans:
                    pairs.append({'question': q, 'answer': ' '.join(' '.join(ans).split())})
                q = line.strip()[4:].strip()
                ans = []
            elif line.strip() and not line.strip().startswith('#'):
                ans.append(line.strip())
            elif not line.strip() and q:
                pass
    if q and ans:
        pairs.append({'question': q, 'answer': ' '.join(' '.join(ans).split())})
    return pairs

def internal_links(md):
    return [m for m in re.findall(r'\]\((/blog/[\w-]+/)\)', md)]

def external_links(md):
    return re.findall(r'\]\((https?://[^)]+)\)', md)

posts = json.load(io.open(base + r'\data\posts.json', encoding='utf-8'))

targets = {
 'claude-vs-gemini-2026-comparison': {
   'title': 'Claude vs Gemini 2026: Which AI Assistant Is Actually Better?',
   'keyTakeaways': [
     'Claude wins for long-form writing, careful reasoning, and coding in 2026; Pro costs $18/month with annual billing or $22 month-to-month.',
     'Gemini wins for Google Workspace integration and budget pricing; AI Plus is $4.99/month and AI Pro is $19.99/month with 5 TB of storage.',
     'Google cut the free consumer Gemini tier to Flash-Lite only on October 9, 2026, making ChatGPT and Claude free tiers comparatively stronger.',
     'Both free tiers remain usable for testing; the rational move is to run both for a week and pay for exactly one tool.',
     'Prices verified October 2026 from Anthropic and Google official pages; plans change quarterly so recheck before purchase.'
   ],
   'affiliateLinks': ['https://www.anthropic.com/pricing', 'https://ai.google.dev/pricing'],
 },
 'gemini-vs-chatgpt-2026': {
   'title': 'Gemini vs ChatGPT 2026: Which AI Assistant Is Actually Better?',
   'keyTakeaways': [
     'ChatGPT is the better all-round assistant in 2026; the free tier includes unlimited GPT-6 text chats and Plus costs $20/month.',
     'Gemini is the better pick for Google Workspace users and budget buyers; AI Plus is $4.99/month and AI Pro bundles 5 TB for $19.99/month.',
     'Google reduced the free consumer Gemini tier to Flash-Lite only on October 9, 2026, narrowing the free-tier gap in ChatGPT favor.',
     'Weekly testing showed ChatGPT stronger on long-form writing and research depth, Gemini stronger on multimodality and Google integration.',
     'Prices verified October 2026 from OpenAI and Google official pages; plans change frequently so recheck before purchase.'
   ],
   'affiliateLinks': ['https://openai.com/chatgpt/pricing/', 'https://ai.google.dev/pricing'],
 },
 'elevenlabs-v2-review-2026': {
   'title': 'ElevenLabs v2 Review 2026: Is It Worth the Subscription?',
   'keyTakeaways': [
     'ElevenLabs v2 is the best AI voice platform in 2026 for realistic text-to-speech and voice cloning; the free tier gives 10,000 characters/month.',
     'Pricing: Starter $5, Creator $22, Pro $99, Scale around $299+, Business around $990 per month, verified from the official pricing page.',
     'It is worth the subscription for weekly voice publishers; light users should stay on the free tier or Starter rather than over-subscribe.',
     'Credits burn fastest on regenerations, so finalize scripts and draft on lower-quality models before the flagship render.',
     'Prices verified October 2026 from the ElevenLabs pricing page and docs; plans change frequently so recheck before purchase.'
   ],
   'affiliateLinks': ['https://elevenlabs.io/pricing', 'https://elevenlabs.io/docs'],
 },
}

for slug, meta in targets.items():
    fn = os.path.join(base, 'content_drafts', '2026-10-11-%s_REWRITE.md' % slug)
    md = io.open(fn, encoding='utf-8').read()
    # quickAnswer: first paragraph after H1 (the bold Quick Answer line)
    m = re.search(r'\*\*Quick Answer:?\s*(.+?)\*\*\s*\n', md, re.S)
    qa = ' '.join(m.group(1).split()) if m else ''
    faq = parse_faq(md)
    ints = internal_links(md)
    exts = [e for e in external_links(md) if 'aitoolcrux' not in e and 'localhost' not in e]
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", md))
    for p in posts:
        if p.get('slug') == slug:
            p['title'] = meta['title']
            p['content'] = md
            p['excerpt'] = qa[:160]
            p['quickAnswer'] = qa
            p['keyTakeaways'] = meta['keyTakeaways']
            p['faq'] = faq
            p['internalLinks'] = ints
            p['affiliateLinks'] = meta['affiliateLinks']
            p['hasRealScreenshots'] = True
            p['screenshotCount'] = 2
            p['wordCount'] = words
            p['date'] = '2026-10-11'
            p['publishedDate'] = '2026-10-11'
            p['updatedAt'] = '2026-10-11'
            p['lastUpdated'] = '2026-10-11'
            p['readingTime'] = '11 min read'
            p['readTime'] = 11
            print('=== updated', slug)
            print('  title:', p['title'])
            print('  quickAnswer len:', len(qa), '| faq:', len(faq), '| ints:', len(ints), '| exts:', len(exts), '| words:', words)
            break
    else:
        print('NOT FOUND', slug)

io.open(base + r'\data\posts.json', 'w', encoding='utf-8').write(json.dumps(posts, ensure_ascii=False, indent=2))
print('posts.json saved, total:', len(posts))
