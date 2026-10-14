import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = [
    'best-free-ai-tools-2026',
    'best-free-ai-tools-for-youtube-creators',
    'best-paid-ai-tools-worth-buying-2026',
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
    'best-free-ai-tools-2026': {
        'bluf': '**Bottom line:** Best free AI tools in 2026: ChatGPT Free for chat, Google Gemini Free for images, ElevenLabs Free for voice. All production-ready with no credit card required.',
        'outbound': '\n\nSources: [OpenAI Free](https://chat.openai.com), [Google Gemini](https://gemini.google.com), [ElevenLabs Free](https://elevenlabs.io)',
        'internal': '\n\nSee also: [Best AI tools 2026](/blog/best-ai-tools-2026), [AI tools comparison](/compare)',
        'question_h2': '\n\n## What Are the Best Free AI Tools in 2026?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Are free AI tools actually good?** Yes, for most personal and small-business use cases.\n\n**Do free AI tools have limits?** Yes, on usage quotas and model tiers.\n\n**Which free AI tool is best overall?** ChatGPT Free — no credit card, no install.\n'
    },
    'best-free-ai-tools-for-youtube-creators': {
        'bluf': '**Bottom line:** Best free AI tools for YouTube creators: CapCut for editing, ElevenLabs for voiceover, ChatGPT for scripts, Canva for thumbnails. All free tiers cover 10-minute videos.',
        'outbound': '\n\nSources: [CapCut](https://www.capcut.com), [ElevenLabs](https://elevenlabs.io), [Canva Free](https://www.canva.com)',
        'internal': '\n\nSee also: [Best AI voice tools](/blog/best-ai-voice-changers-2026), [Best free AI tools](/blog/best-free-ai-tools-2026)',
        'question_h2': '\n\n## Which Free AI Tools Do YouTube Creators Need?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Can I use AI voiceovers on YouTube?** Yes, but disclose AI use per YouTube policy.\n\n**Is CapCut really free?** Yes, with no watermark on exports.\n\n**What AI tool is best for YouTube thumbnails?** Canva Free, with AI background remover.\n'
    },
    'best-paid-ai-tools-worth-buying-2026': {
        'bluf': '**Bottom line:** Worth paying for in 2026: ChatGPT Plus ($20/mo), Cursor Pro ($20/mo), ElevenLabs Pro ($22/mo). Skip generic "all-in-one" AI suites; pay for tools that save you hours weekly.',
        'outbound': '\n\nSources: [ChatGPT Plus](https://openai.com/chatgpt/pricing), [Cursor Pricing](https://cursor.com/pricing), [ElevenLabs Pricing](https://elevenlabs.io/pricing)',
        'internal': '\n\nSee also: [Best AI tools 2026](/blog/best-ai-tools-2026), [AI tools comparison](/compare)',
        'question_h2': '\n\n## Which Paid AI Tools Are Actually Worth the Money?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**How much should I spend on AI tools?** $50-100/mo per role is the sweet spot.\n\n**Is ChatGPT Plus worth it?** Yes, if you use AI daily for work.\n\n**Should I buy an all-in-one AI suite?** No, specialized tools are better value.\n'
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
    md = f"---\ntitle: \"{p['title']}\"\ndescription: \"{p.get('excerpt','')[:160]}\"\ndate: 2026-10-14\n---\n\n{p['content']}\n"
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.md'
    tmp.write_text(md, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")
