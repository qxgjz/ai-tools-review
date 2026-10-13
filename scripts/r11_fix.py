import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = [
    'ai-tools-for-beginners-2026',
    'ai-tools-review-guide-2026',
    'ai-tools-selection-guide-2026',
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
    'ai-tools-for-beginners-2026': {
        'bluf': '**Bottom line:** Start with ChatGPT Free for chat, Google Images for AI images, and ElevenLabs Free for voice. No need to pay for tools until you know your workflow.',
        'outbound': '\n\nSources: [OpenAI](https://chat.openai.com), [Google AI Studio](https://aistudio.google.com), [ElevenLabs](https://elevenlabs.io)',
        'internal': '\n\nSee also: [Best free AI tools](/blog/best-free-ai-tools-2026), [Best AI tools 2026](/blog/best-ai-tools-2026)',
        'question_h2': '\n\n## What AI Tools Should a Beginner Start With?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**What is the easiest AI tool to learn first?** ChatGPT Free — no setup, just type a prompt.\n\n**Are free AI tools good enough?** Yes for learning; upgrade to paid only when you hit limits.\n\n**Do I need coding skills?** No, most modern AI tools are no-code.\n'
    },
    'ai-tools-review-guide-2026': {
        'bluf': '**Bottom line:** Review AI tools on real tasks, not demos. Test 3-5 alternatives side by side, check pricing tiers, and verify outputs match your use case before paying.',
        'outbound': '\n\nSources: [GPT-4o benchmark](https://platform.openai.com/docs/guides/benchmarks), [MMLU leaderboard](https://github.com/hendrycks/test)',
        'internal': '\n\nSee also: [AI tool comparison](/compare), [Best AI tools 2026](/blog/best-ai-tools-2026)',
        'question_h2': '\n\n## How Do You Review an AI Tool?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**What makes a good AI tool review?** Real task testing, not marketing screenshots.\n\n**How many tools should I compare?** 3-5 minimum; 7-10 for buying decisions.\n\n**How long should a review be?** 2000+ words with screenshots and pricing.\n'
    },
    'ai-tools-selection-guide-2026': {
        'bluf': '**Bottom line:** Choose AI tools by use case (writing, coding, images, voice), team size, and budget. Start free, upgrade when you hit limits. Avoid "all-in-one" tools until you know your needs.',
        'outbound': '\n\nSources: [G2 AI tools category](https://www.g2.com/categories/artificial-intelligence), [Capterra AI tools](https://www.capterra.com/artificial-intelligence-software/)',
        'internal': '\n\nSee also: [AI tools comparison](/compare), [Best AI tools 2026](/blog/best-ai-tools-2026)',
        'question_h2': '\n\n## How Do I Choose the Right AI Tool?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**What is the #1 AI tool in 2026?** ChatGPT Plus for general use, $20/mo.\n\n**Should I use one all-in-one AI tool?** No — specialized tools beat suites for quality.\n\n**How much should I budget?** Start $0, then $20-50/mo per role.\n'
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
