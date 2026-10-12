import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = ['adobe-firefly-review-2026','canva-pro-free-for-students','elevenlabs-vs-playht-2026']

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
    'adobe-firefly-review-2026': {
        'bluf': '**Bottom line:** Adobe Firefly is best for commercial-safe images with clean training data, but trails Midjourney on artistic quality. Free tier available, paid starts at $4.99/mo.',
        'outbound': '\n\nSources: [Adobe Firefly](https://www.adobe.com/products/firefly.html), [Firefly pricing](https://www.adobe.com/products/firefly/plans-pricing.html)',
        'internal': '\n\nSee also: [Midjourney vs DALL-E 3](/blog/midjourney-v7-vs-dall-e-3-2026), [Best AI image generators](/blog/best-ai-image-generators-2026)',
        'question_h2': '\n\n## Is Adobe Firefly Good for Commercial Work?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**Is Adobe Firefly free?** Yes, with a free tier (25 generations/mo).\n\n**Can I use Firefly images commercially?** Yes, they are trained on licensed Adobe stock.\n\n**How does Firefly compare to Midjourney?** Firefly is safer for commercial; Midjourney is more artistic.\n'
    },
    'canva-pro-free-for-students': {
        'bluf': '**Bottom line:** Canva Pro is free for verified students via the Canva for Education program. No credit card needed — just a .edu email and school verification.',
        'outbound': '\n\nSources: [Canva for Education](https://www.canva.com/education/), [Canva Pro pricing](https://www.canva.com/pricing/)',
        'internal': '\n\nSee also: [Canva vs Beautiful.ai](/blog/canva-vs-beautiful-ai-2026), [Best AI design tools](/blog/best-ai-design-tools-2026)',
        'question_h2': '\n\n## How Do Students Get Canva Pro for Free?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**How long is Canva Pro free for students?** 1 year, renewable while enrolled.\n\n**Do I need a .edu email?** Yes, or teacher verification through your school.\n\n**Can I use Canva Pro commercial rights?** Yes, for student work and classroom projects.\n'
    },
    'elevenlabs-vs-playht-2026': {
        'bluf': '**Bottom line:** ElevenLabs wins on voice quality and emotional range; PlayHT wins on pricing and multilingual support. Pick ElevenLabs for English narration, PlayHT for global content.',
        'outbound': '\n\nSources: [ElevenLabs](https://elevenlabs.io), [PlayHT](https://play.ht)',
        'internal': '\n\nSee also: [Best AI voice generators](/blog/best-ai-voice-generators-2026), [ElevenLabs alternatives](/blog/elevenlabs-alternatives-2026)',
        'question_h2': '\n\n## Which AI Voice Generator Is More Natural?\n\n',
        'faq': '\n\n## Frequently Asked Questions\n\n**How much does ElevenLabs cost?** Free tier, then $5/mo Starter, $22/mo Creator.\n\n**Is PlayHT cheaper?** Yes, $31/mo for 600k characters vs ElevenLabs $22/mo for 100k.\n\n**Which sounds more human?** ElevenLabs, especially on emotional intonation.\n'
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
    md = f"---\ntitle: \"{p['title']}\"\ndescription: \"{p.get('excerpt','')[:160]}\"\ndate: 2026-10-12\n---\n\n{p['content']}\n"
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.md'
    tmp.write_text(md, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")
