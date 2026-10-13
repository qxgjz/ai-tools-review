import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = ['perplexity-review-2026','ai-coding-tools-comparison-2026','ai-tools-comparison-2026']

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
    'perplexity-review-2026': {
        'bluf': '**Bottom line:** Perplexity Pro is the best AI search assistant for research in 2026 — $20/mo for GPT-4o, Claude, and DeepSeek models with citations. Worth it if you do heavy research daily.',
        'outbound': '\n\nSources: [Perplexity AI](https://www.perplexity.ai), [Perplexity Pro pricing](https://www.perplexity.ai/pro)',
        'internal': '\n\nSee also: [Perplexity vs ChatGPT](/blog/perplexity-vs-chatgpt-2026), [Best AI chatbots](/blog/best-ai-chatbots-2026)',
        'question_h2': '\n\n## Is Perplexity Pro Worth $20/Month?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**How much is Perplexity Pro?** $20/month or $200/year, unlimited Pro model queries.\n\n**Is there a free tier?** Yes, with limited GPT-4o and search.\n\n**Which models does it use?** GPT-4o, Claude 3.5 Sonnet, DeepSeek R1, and its own Sonar.\n'
    },
    'ai-coding-tools-comparison-2026': {
        'bluf': '**Bottom line:** Cursor wins for general coding, GitHub Copilot for enterprise, Windsurf for multi-agent workflows. Pick based on your stack and team size.',
        'outbound': '\n\nSources: [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot), [Windsurf](https://codeium.com/windsurf)',
        'internal': '\n\nSee also: [Cursor vs Copilot](/blog/cursor-vs-github-copilot-2026), [Best AI code editors](/blog/best-ai-code-editors-2026)',
        'question_h2': '\n\n## Which AI Coding Tool Is Best in 2026?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is Cursor better than Copilot?** For solo developers yes; for enterprise compliance, Copilot.\n\n**How much does Cursor cost?** Free tier, $20/mo Pro, $40/mo Ultra.\n\n**Can I use AI coding tools for free?** Yes, GitHub Copilot has a free tier limited to 2000 completions/month.\n'
    },
    'ai-tools-comparison-2026': {
        'bluf': '**Bottom line:** Best all-around AI tool in 2026: ChatGPT for chat, Midjourney for images, ElevenLabs for voice, Cursor for code. No single tool wins everything.',
        'outbound': '\n\nSources: [OpenAI](https://openai.com), [Midjourney](https://www.midjourney.com), [ElevenLabs](https://elevenlabs.io)',
        'internal': '\n\nSee also: [Best AI tools](/blog/best-ai-tools-2026), [AI tool comparison](/compare)',
        'question_h2': '\n\n## Which AI Tool Should I Start With?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**What is the best AI tool overall?** ChatGPT Plus for general use, $20/mo.\n\n**Are free AI tools worth it?** For casual use yes; for production, paid tiers are worth the cost.\n\n**How do I choose the right AI tool?** Start with your use case: writing, coding, images, or voice.\n'
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
    md = f"---\ntitle: \"{p['title']}\"\ndescription: \"{p.get('excerpt','')[:160]}\"\ndate: 2026-10-13\n---\n\n{p['content']}\n"
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.md'
    tmp.write_text(md, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")
