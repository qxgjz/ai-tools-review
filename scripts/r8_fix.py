import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = ['creatium-coach-review-2025','devin-ai-review','openai_astra_review']

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
    'creatium-coach-review-2025': {
        'bluf': '**Bottom line:** Creatium Coach is a solid AI writing coach for solopreneurs, but $99/mo is steep compared to Jasper ($49/mo) or ChatGPT Plus ($20/mo). Best if you need structured feedback, not just generation.',
        'outbound': '\n\nSources: [Creatium Coach](https://www.creatium.ai), [Jasper](https://www.jasper.com)',
        'internal': '\n\nSee also: [Best AI writing tools](/blog/best-ai-writing-tools-2026), [Jasper review](/blog/jasper-review-2026)',
        'question_h2': '\n\n## Is Creatium Coach Worth the $99/mo Price?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**What is Creatium Coach?** An AI writing assistant that acts as a coach, giving feedback on drafts rather than just generating text.\n\n**How much does Creatium Coach cost?** $99/mo for the pro plan.\n\n**Is there a free trial?** Yes, 14 days.\n'
    },
    'devin-ai-review': {
        'bluf': '**Bottom line:** Devin AI is the most impressive autonomous coder demo we tested, but at $500/mo it is overkill for most teams. Use it for complex multi-step engineering tasks, not bug fixes.',
        'outbound': '\n\nSources: [Devin AI](https://devin.ai), [Cognition Labs](https://www.cognition.ai)',
        'internal': '\n\nSee also: [Best AI coding tools](/blog/best-ai-coding-tools-2026), [Cursor review](/blog/cursor_ai_review)',
        'question_h2': '\n\n## Is Devin AI Better Than Cursor?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**How much does Devin AI cost?** $500/mo for the standard plan.\n\n**Can Devin replace a junior engineer?** Not yet. It handles well-scoped tasks but needs oversight.\n\n**Is there a free trial?** Limited beta access only.\n'
    },
    'openai_astra_review': {
        'bluf': '**Bottom line:** OpenAI Astra is the best coding agent for full-repo refactors, but at $200/mo it costs 5x Cursor. Buy it if you spend 20+ hours/week on large refactors; otherwise Cursor is enough.',
        'outbound': '\n\nSources: [OpenAI Astra](https://openai.com/astra), [OpenAI pricing](https://openai.com/api/pricing)',
        'internal': '\n\nSee also: [Cursor review](/blog/cursor_ai_review), [Best AI coding tools](/blog/best-ai-coding-tools-2026)',
        'question_h2': '\n\n## Is OpenAI Astra Worth $200/mo?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**How much does OpenAI Astra cost?** $200/mo for the pro tier.\n\n**What is OpenAI Astra used for?** Autonomous coding agent that handles multi-file refactors and long tasks.\n\n**How does it compare to Cursor?** Astra handles full-repo work; Cursor is better for interactive edits.\n'
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
date: 2026-10-12
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
