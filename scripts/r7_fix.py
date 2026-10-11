import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = ['beautiful-ai-alternatives','claude_fable_51_review','clearscope-alternatives']

def html_to_md(html):
    s = html
    s = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', s, flags=re.S|re.I)
    s = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', s, flags=re.S|re.I)
    s = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', s, flags=re.S|re.I)
    s = re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', r'**\1**', s, flags=re.S|re.I)
    s = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', s, flags=re.S|re.I)
    s = re.sub(r'</?[uo]l[^>]*>', '', s, flags=re.I)
    s = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', s, flags=re.S|re.I)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

# Per-slug extra content
EXTRAS = {
    'beautiful-ai-alternatives': {
        'bluf': '**Bottom line:** Beautiful.ai is great for branded decks but expensive ($12/user/mo). The best alternatives are Canva (free tier), Gamma (AI slides), and Pitch (collaborative decks).',
        'outbound': '\n\nSources: [Beautiful.ai pricing](https://www.beautiful.ai/pricing), [Canva](https://www.canva.com), [Gamma](https://gamma.app)',
        'internal': '\n\nSee also: [Best AI presentation tools](/blog/best-ai-presentation-tools-2026), [Canva vs Beautiful.ai](/blog/canva-vs-beautiful-ai-2026)',
        'question_h2': '\n\n## Is There a Free Beautiful.ai Alternative?\n\nYes. Canva offers a free tier with solid templates. Gamma gives 400 credits/month free. Pitch has a free plan for up to 5 users.\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is Beautiful.ai worth the money?** For teams that ship branded decks weekly, yes. For occasional users, Canva free is enough.\n\n**What is the best Beautiful.ai alternative?** Canva for value, Gamma for AI speed, Pitch for collaboration.\n\n**Can I use Beautiful.ai for free?** They offer a 14-day trial, no permanent free plan.\n'
    },
    'claude_fable_51_review': {
        'bluf': '**Bottom line:** Claude Fable 5.1 shines on long-context fiction writing and code explanation, but lags behind GPT-5 on speed and multimodal. Best for novelists and devs, not for real-time chat.',
        'outbound': '\n\nSources: [Anthropic Claude Fable](https://www.anthropic.com/news), [Claude pricing](https://www.anthropic.com/pricing)',
        'question_h2': '\n\n## Is Claude Fable 5.1 Better Than GPT-5?\n\nFor long-form writing, yes. For speed and multimodal, no. Pick based on your primary task.\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**How much does Claude Fable 5.1 cost?** $3/M input, $15/M output via API. Console pricing starts at $20/mo.\n\n**Is Claude Fable 5.1 good for coding?** Yes, especially on long files and refactors. It handles 200K context windows.\n\n**Does Claude Fable have web search?** Yes, via Claude.ai web search toggle.\n'
    },
    'clearscope-alternatives': {
        'bluf': '**Bottom line:** Clearscope is the gold standard for SEO content briefs but costs $189/mo. Cheaper alternatives: SurferSEO ($89/mo), Frase ($15/mo), and Clearscope alternatives like NeuronWriter.',
        'outbound': '\n\nSources: [Clearscope pricing](https://www.clearscope.io/pricing), [SurferSEO](https://surferseo.com), [Frase](https://frase.io)',
        'internal': '\n\nSee also: [Best AI SEO tools](/blog/best-ai-seo-tools-2026), [SurferSEO vs Clearscope](/blog/surferseo-vs-clearscope-2026)',
        'question_h2': '\n\n## Is There a Free Clearscope Alternative?\n\nFrase offers a 7-day trial. For permanent free, use Google Keyword Planner plus manual SERP analysis.\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**What is the cheapest Clearscope alternative?** Frase at $15/mo entry, or NeuronWriter at $19/mo.\n\n**Is SurferSEO better than Clearscope?** Surfer is better for on-page content scoring; Clearscope is better for briefs.\n\n**Can I use Clearscope for free?** No free tier, only a 14-day trial.\n'
    },
}

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in TARGETS:
    p = next(x for x in posts if x['slug']==slug)
    c = html_to_md(p['content'])
    ext = EXTRAS[slug]
    if 'Bottom line' not in c:
        c = ext['bluf'] + '\n\n' + c
    c = c + ext['question_h2'] + ext['outbound'] + ext.get('internal','') + ext['faq']
    p['content'] = c

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

for slug in TARGETS:
    p = next(x for x in posts if x['slug']==slug)
    md = f"""---
title: "{p['title']}"
description: "{p.get('excerpt','')[:160]}"
date: 2026-10-11
---

{p['content']}
"""
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.md'
    tmp.write_text(md, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")
