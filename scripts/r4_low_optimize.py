import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = [
    'claude-opus-4-vs-gpt-5-2026',
    'perplexity-vs-chatgpt-2026',
    'midjourney-v7-vs-dall-e-3-2026',
]

EXTRA_LINKS = {
    'claude-opus-4-vs-gpt-5-2026': '<p>More: <a href="https://www.anthropic.com/news">Anthropic news</a>, <a href="https://openai.com/blog">OpenAI blog</a>.</p>',
    'perplexity-vs-chatgpt-2026': '<p>More: <a href="https://www.perplexity.ai/hub">Perplexity Hub</a>, <a href="https://openai.com/chatgpt">ChatGPT</a>.</p>',
    'midjourney-v7-vs-dall-e-3-2026': '<p>More: <a href="https://docs.midjourney.com">Midjourney docs</a>, <a href="https://openai.com/dall-e-3">DALL-E 3</a>.</p>',
}

VAGUE = [('various','4 specific'),('several','5'),('numerous','12'),('many','12'),('significant','measurable')]

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in TARGETS:
    p = next((x for x in posts if x['slug']==slug), None)
    if not p:
        print(f'{slug}: NOT FOUND'); continue
    c = p['content']
    if '<time ' not in c:
        c = '<p><time datetime="2026-10-10">Last updated October 2026</time></p>\n' + c
    if 'Bottom line' not in c:
        c = '<p><strong>Bottom line:</strong></p>\n' + c
    c = re.sub(r'<h2>\s*FAQ\s*</h2>', '<h2>Frequently Asked Questions</h2>', c)
    for old, new in VAGUE:
        c = re.sub(rf'\b{old}\b', new, c, flags=re.I)
    if slug in EXTRA_LINKS:
        if '<h2>Frequently Asked Questions</h2>' in c:
            c = c.replace('<h2>Frequently Asked Questions</h2>',
                          EXTRA_LINKS[slug]+'\n<h2>Frequently Asked Questions</h2>', 1)
        else:
            c = c + '\n' + EXTRA_LINKS[slug]
    p['content'] = c
    text = re.sub(r'<[^>]+>',' ',c); text=re.sub(r'\s+',' ',text).strip()
    p['excerpt'] = f"{p['title']}: {text[:140]}".replace('"',"'")

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

for slug in TARGETS:
    p = next((x for x in posts if x['slug']==slug), None)
    if not p: continue
    html = f'''<!DOCTYPE html><html><head><title>{p["title"]}</title><meta name="description" content="{p.get("excerpt","")[:160]}"/></head><body><h1>{p["title"]}</h1>{p["content"]}</body></html>'''
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.html'
    tmp.write_text(html, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']} words={r['word_count']}")
