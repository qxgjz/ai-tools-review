import json, os, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

posts = json.load(open('data/posts.json','r',encoding='utf-8'))

EXTRAS = {
    'notion-ai-vs-notion-ai-salesforce-2026': {
        'bluf': '**Bottom line:** Notion AI wins for lightweight note-taking and docs; Salesforce Einstein wins for enterprise CRM and sales automation. Pick Notion if your team lives in docs; pick Salesforce if you need lead scoring and pipeline management.',
        'outbound': '\n\nSources: [Notion AI docs](https://www.notion.com/help/guides/notion-ai), [Salesforce Einstein](https://www.salesforce.com/artificial-intelligence/)',
        'internal': '\n\nSee also: [Notion AI alternatives](/blog/best-notion-ai-alternatives-2026), [Salesforce alternatives](/blog/salesforce-alternatives-2026)',
        'question_h2': '\n\n## Which Should Your Team Choose: Notion AI or Salesforce Einstein?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is Notion AI replacing Salesforce?** No. Notion AI handles docs and notes; Salesforce handles CRM. They solve different problems.\n\n**Can Notion AI do lead scoring?** Not natively. You need Salesforce or a dedicated CRM for that.\n\n**Is Salesforce Einstein worth the price?** For sales teams with 10+ reps, yes. For solo founders, Notion AI is cheaper.\n'
    },
    'notion-ai-vs-salesforce-2026': {
        'bluf': '**Bottom line:** Notion AI is better for docs, wikis, and project notes; Salesforce Einstein is better for CRM, sales pipelines, and enterprise data. Notion costs $10/mo; Salesforce starts at $25/user/mo.',
        'outbound': '\n\nSources: [Notion AI pricing](https://www.notion.so/pricing), [Salesforce Einstein pricing](https://www.salesforce.com/prcing/)',
        'internal': '\n\nSee also: [Best AI writing tools](/blog/best-ai-writing-tools-2026), [Notion AI review](/blog/notion-ai-review-2026)',
        'question_h2': '\n\n## Is Notion AI a Replacement for Salesforce?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Can Notion AI replace Salesforce?** No. Notion has no CRM pipeline, lead scoring, or sales forecasting.\n\n**Is Salesforce Einstein easy to use?** Steeper learning curve than Notion, but Salesforce offers Trailhead training.\n\n**Which is cheaper?** Notion AI at $10/mo vs Salesforce at $25/user/mo minimum.\n'
    },
}

for slug, ext in EXTRAS.items():
    p = next(x for x in posts if x['slug']==slug)
    c = p['content']
    if 'Bottom line' not in c:
        c = ext['bluf'] + '\n\n' + c
    c = c + ext['question_h2'] + ext['outbound'] + ext['internal'] + ext['faq']
    p['content'] = c

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

for slug in EXTRAS:
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
