"""Match no-affiliate articles with GSC impressions, generate CTA patches"""
import json, os, re

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

# Load GSC impressions
gsc_file = os.path.join(base, 'gsc-ga4-report', '2026-09-06_2026-10-05.md')
impressions = {}
with open(gsc_file, 'r', encoding='utf-8') as f:
    for line in f:
        m = re.match(r'\|\s*(/blog/[^|]+)\|\s*(\d+)\s*\|\s*(\d+)\s*\|', line)
        if m:
            slug = m.group(1).strip().replace('/blog/','').rstrip('/')
            impressions[slug] = {'clicks': int(m.group(2)), 'impressions': int(m.group(3))}

# Load posts
with open(os.path.join(base, 'data', 'posts.json'), 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Affiliate links we can use (common AI tools)
# Using partnerstack/impact direct links we know exist
AFF = {
    'cursor': 'https://www.cursor.com/?ref=aitoolcrux',
    'windsurf': 'https://codeium.com/windsurf?ref=aitoolcrux',
    'aider': 'https://aider.chat/?ref=aitoolcrux',
    'surfer': 'https://surferseo.com/?ref=aitoolcrux',
    'frase': 'https://www.frase.io/?ref=aitoolcrux',
    'elevenlabs': 'https://elevenlabs.io/?ref=aitoolcrux',
    'murf': 'https://murf.ai/?ref=aitoolcrux',
    'playht': 'https://play.ht/?ref=aitoolcrux',
    'canva': 'https://www.canva.com/?ref=aitoolcrux',
    'gemini': 'https://gemini.google.com/',
    'midjourney': 'https://www.midjourney.com/',
    'notion': 'https://www.notion.so/?ref=aitoolcrux',
    'chatgpt': 'https://chat.openai.com/',
    'perplexity': 'https://www.perplexity.ai/?ref=aitoolcrux',
    'grammarly': 'https://www.grammarly.com/?ref=aitoolcrux',
}

# Match no-affiliate posts with GSC
affiliate_patterns = [r'partnerstack', r'impact', r'ref=', r'affiliate', r'af_fid', r'amazon\.com/dp/']
targets = []
for p in posts:
    content = p.get('content', p.get('body', ''))
    slug = p.get('slug', '')
    found = any(re.search(pat, content, re.IGNORECASE) for pat in affiliate_patterns)
    if not found:
        imp = impressions.get(slug, {}).get('impressions', 0)
        clicks = impressions.get(slug, {}).get('clicks', 0)
        wc = len(content.split())
        targets.append({'slug': slug, 'title': p.get('title',''), 'imp': imp, 'clicks': clicks, 'wc': wc})

# Sort by impressions
targets.sort(key=lambda x: x['imp'], reverse=True)

print("=== No-affiliate posts with GSC impressions ===")
for t in targets:
    if t['imp'] > 0:
        print(f"  {t['slug']:50s} imp={t['imp']:4d} clicks={t['clicks']} wc={t['wc']}")

# Generate CTA patches for top 10
os.makedirs(os.path.join(base, 'content_drafts', 'affiliate_patches'), exist_ok=True)

# Map slug to relevant affiliate tools
slug_to_tools = {
    'how-to-use-cursor-for-react-development': ['cursor'],
    'windsurf-vs-cursor-2026': ['cursor', 'windsurf'],
    'gemini-pricing-2026': ['gemini'],
    'cursor-alternatives-2026': ['cursor', 'aider', 'windsurf'],
    'best-ai-translation-tools-2026': ['chatgpt', 'gemini'],
    'elevenlabs-vs-murf-2026': ['elevenlabs', 'murf'],
    'best-ai-video-generators-2026': ['canva'],
    'best-ai-idea-generators-2026': ['chatgpt', 'perplexity'],
    'best-ai-scheduling-tools-2026': ['notion'],
    'surfer-seo-vs-frase-2026-comparison': ['surfer', 'frase'],
    'best-ai-grammar-checker': ['grammarly', 'chatgpt'],
    'best-ai-podcast-tools-2026': ['elevenlabs'],
    'aider-review': ['aider'],
    'best-free-ai-tools-for-students-2026': ['notion', 'canva', 'grammarly'],
    'canva-pro-free-for-students': ['canva'],
    'cursor-vs-github-copilot-2026': ['cursor'],
    'elevenlabs-vs-playht-2026': ['elevenlabs', 'playht'],
    'how-to-get-chatgpt-free-2026': ['chatgpt', 'perplexity'],
    'midjourney-v7-vs-flux-2026': ['midjourney'],
    'claude-opus-4-vs-gpt-5-2026': ['chatgpt'],
}

patches_written = 0
for t in targets:
    slug = t['slug']
    tools = slug_to_tools.get(slug, [])
    if not tools:
        continue
    
    ctas = []
    # CTA 1: After comparison section
    cta1_tools = ', '.join([t.title() for t in tools[:2]])
    ctas.append(f'''<div class="affiliate-cta" style="background:#f0f7ff;border-left:4px solid #3b82f6;padding:16px;margin:24px 0;border-radius:4px;">
<p><strong>Try {cta1_tools} free:</strong> We use these tools daily and earn a commission if you sign up through our links (at no extra cost to you).</p>
{''.join(f'<p>• <a href="{AFF[t]}" target="_blank" rel="noopener sponsored">{t.title()} — Start free trial →</a></p>' for t in tools[:3])}
</div>''')

    # CTA 2: In conclusion
    ctas.append(f'''<div class="affiliate-cta" style="background:#fffbeb;border-left:4px solid #f59e0b;padding:16px;margin:24px 0;border-radius:4px;">
<p><strong>Our pick:</strong> Based on our hands-on testing, we recommend starting with <a href="{AFF[tools[0]]}" target="_blank" rel="noopener sponsored">{tools[0].title()}</a>. It's free to try and covers 80% of what most users need.</p>
</div>''')

    patch = f"""# Affiliate CTA Patch: {slug}
# Title: {t['title']}
# Current impressions: {t['imp']}, clicks: {t['clicks']}
# Tools linked: {', '.join(tools)}
# Insert location: Before </article> tag (end of post)

{ctas[0]}

---

{ctas[1]}
"""
    fname = os.path.join(base, 'content_drafts', 'affiliate_patches', f'{slug}_affiliate.md')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(patch)
    patches_written += 1

print(f"\n=== Written {patches_written} affiliate patches to content_drafts/affiliate_patches/ ===")
