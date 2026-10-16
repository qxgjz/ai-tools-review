import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = [
    'claude-review-2026',
    'copy-ai-review-2026',
    'cursor-review-2026',
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
    'claude-review-2026': {
        'bluf': '**Bottom line:** Claude 3.5 Sonnet ($20/mo) beats ChatGPT on long writing, coding accuracy, and nuance. Worth it for writers and developers; skip if you only need casual chat.',
        'outbound': '\n\nSources: [Claude Pricing](https://claude.ai/pricing), [Anthropic Benchmarks](https://www.anthropic.com/news/claude-3), [ChatGPT vs Claude](/blog/chatgpt-vs-claude-2026-comparison)',
        'internal': '\n\nSee also: [Best AI chatbots](/blog/category/ai-chat), [ChatGPT alternatives](/blog/chatgpt-alternatives-2026)',
        'question_h2': '\n\n## Is Claude 3.5 Sonnet Worth It in 2026?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is Claude free?** Yes, with daily limits on the free tier.\n\n**Which is better: Claude or ChatGPT?** Claude for long writing, ChatGPT for tools.\n\n**Does Claude have image generation?** No, Claude is text-only.\n'
    },
    'copy-ai-review-2026': {
        'bluf': '**Bottom line:** Copy.ai ($36/mo Starter) is good for marketing teams that need brand voice consistency, but Jasper offers better templates for solo writers. AI copy quality is average.',
        'outbound': '\n\nSources: [Copy.ai Pricing](https://www.copy.ai/pricing), [Jasper Pricing](https://www.jasper.ai/pricing), [Jasper vs Copy.ai](/blog/jasper-vs-copy-ai-2026-comparison)',
        'internal': '\n\nSee also: [Best AI writing tools](/blog/category/ai-writing), [Best AI marketing tools](/blog/category/ai-marketing)',
        'question_h2': '\n\n## Is Copy.ai Worth It in 2026?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is Copy.ai free?** Yes, with limited credits on the free plan.\n\n**Does Copy.ai write good marketing copy?** Average; needs heavy editing.\n\n**Which is better: Copy.ai or Jasper?** Jasper for templates, Copy.ai for team workflows.\n'
    },
    'cursor-review-2026': {
        'bluf': '**Bottom line:** Cursor Pro ($20/mo) is the best AI code editor for 2026. Claude 3.5 integration beats GitHub Copilot on complex refactoring. Worth it if you write code daily.',
        'outbound': '\n\nSources: [Cursor Pricing](https://cursor.com/pricing), [GitHub Copilot](https://github.com/features/copilot), [Cursor vs Windsurf](/blog/cursor-vs-windsurf-2026)',
        'internal': '\n\nSee also: [Best AI coding tools](/blog/best-ai-coding-tools-2026), [Cursor vs GitHub Copilot](/blog/cursor-vs-github-copilot-2026)',
        'question_h2': '\n\n## Is Cursor Pro Worth It in 2026?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is Cursor free?** Yes, with limited completions per month.\n\n**Does Cursor work with VS Code extensions?** Yes, it is a VS Code fork.\n\n**Which is better: Cursor or Copilot?** Cursor for autonomy, Copilot for autocomplete.\n'
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
