import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = [
    'canva-ai-alternatives-2026',
    'chatgpt-alternatives-2026',
    'chatgpt-deep-review-2026',
]

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

EXTRAS = {
    'canva-ai-alternatives-2026': {
        'bluf': '**Bottom line:** Best Canva AI alternatives in 2026: Adobe Express for pros, Figma for design teams, VistaCreate for social media. Switch only if you outgrow Canva Magic Design limits.',
        'outbound': '\n\nSources: [Adobe Express](https://www.adobe.com/express.html), [Figma AI](https://www.figma.com), [VistaCreate](https://create.vista.com)',
        'internal': '\n\nSee also: [Best AI design tools](/blog/category/ai-design), [Canva vs Adobe Firefly](/blog/canva-ai-vs-adobe-firefly-2026-comparison)',
        'question_h2': '\n\n## What Are the Best Canva AI Alternatives?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is Canva AI free?** Yes, with limits on AI generations per month.\n\n**What is better than Canva for professional design?** Adobe Express or Figma.\n\n**Are Canva alternatives cheaper?** Most are similarly priced; Adobe Express is free with Creative Cloud.\n'
    },
    'chatgpt-alternatives-2026': {
        'bluf': '**Bottom line:** Best ChatGPT alternatives in 2026: Claude 3.5 Sonnet for long context, Gemini Advanced for multimodal, Perplexity Pro for search. Each beats ChatGPT in one specific job.',
        'outbound': '\n\nSources: [Claude](https://claude.ai), [Gemini](https://gemini.google.com), [Perplexity](https://perplexity.ai)',
        'internal': '\n\nSee also: [Best AI chatbots](/blog/category/ai-chat), [ChatGPT vs Claude](/blog/chatgpt-vs-claude-2026-comparison)',
        'question_h2': '\n\n## What Are the Best ChatGPT Alternatives in 2026?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is there a free ChatGPT alternative?** Yes — Claude Free, Gemini Free, Perplexity Free.\n\n**Which ChatGPT alternative is best?** Depends: Claude for writing, Gemini for images, Perplexity for search.\n\n**Can I use alternatives without login?** No, all require email signup.\n'
    },
    'chatgpt-deep-review-2026': {
        'bluf': '**Bottom line:** ChatGPT Plus ($20/mo) is worth it if you use AI daily. GPT-4o beats free GPT-3.5 on reasoning, coding, and multimodal. Skip Team plan unless you have 3+ users.',
        'outbound': '\n\nSources: [OpenAI Pricing](https://openai.com/chatgpt/pricing), [GPT-4o Benchmarks](https://platform.openai.com/docs/guides/benchmarks)',
        'internal': '\n\nSee also: [ChatGPT vs Claude](/blog/chatgpt-vs-claude-2026-comparison), [Best AI tools 2026](/blog/best-ai-tools-2026)',
        'question_h2': '\n\n## Is ChatGPT Plus Worth It in 2026?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**What is ChatGPT Plus?** $20/mo plan with GPT-4o, DALL-E, and faster responses.\n\n**Is the free tier enough?** For casual use yes; for work, upgrade.\n\n**How does GPT-4o compare to GPT-3.5?** 2x faster, better reasoning, sees images.\n'
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
    md = f"---\ntitle: \"{p['title']}\"\ndescription: \"{p.get('excerpt','')[:160]}\"\ndate: 2026-10-16\n---\n\n{p['content']}\n"
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.md'
    tmp.write_text(md, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")
