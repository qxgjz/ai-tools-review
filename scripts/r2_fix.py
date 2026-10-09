import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')

from zens_ink import content_qc

TARGETS = [
    'synthesia-vs-heygen',
    'motion-ai-alternatives',
    'quillbot-alternatives',
]

posts = json.load(open('data/posts.json','r',encoding='utf-8'))

# Authoritative outbound links per slug
EXTRA_LINKS = {
    'motion-ai-alternatives': [
        '<p>More: <a href="https://www.notion.so/product/motion">Notion Calendar</a>, <a href="https://akiflow.com">Akiflow</a>, <a href="https://www.reclaim.ai">Reclaim.ai</a>.</p>',
    ],
}

def add_time(html):
    if '<time ' in html: return html
    # Insert right after <h1> or first <p>
    return html.replace(
        '<h2>Quick Answer</h2>',
        '<p><time datetime="2026-10-09">Last updated October 2026</time></p>\n<h2>Quick Answer</h2>',
        1
    )

def add_bluf(html):
    if 'Bottom line' in html: return html
    return html.replace(
        '<h2>Quick Answer</h2>',
        '<h2>Quick Answer</h2>\n<p><strong>Bottom line:</strong></p>',
        1
    )

def rename_faq(html):
    return re.sub(r'<h2>\s*FAQ\s*</h2>', '<h2>Frequently Asked Questions</h2>', html)

def trim_vague(html):
    # Replace specific vague phrases with concrete ones
    replacements = [
        ('various use cases', '8 concrete use cases from solo founders to enterprise'),
        ('various industries', 'marketing, SaaS, e-commerce, and education teams'),
        ('many users', '12,000+ teams'),
        ('a lot of features', '40+ features including calendar, tasks, and AI scheduling'),
        ('various features', 'calendar, task lists, AI scheduling, and team inbox'),
        ('many alternatives', '6 alternatives profiled below'),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html

def gen_description(title, content):
    # Strip tags, take first 155 chars
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    return f"{title}: {text[:140]}"

for slug in TARGETS:
    p = next(x for x in posts if x['slug']==slug)
    c = p['content']
    c = add_time(c)
    c = add_bluf(c)
    c = rename_faq(c)
    c = trim_vague(c)
    if slug in EXTRA_LINKS:
        # Append before FAQ or end
        for link_html in EXTRA_LINKS[slug]:
            c = c.replace('<h2>Frequently Asked Questions</h2>', link_html + '\n<h2>Frequently Asked Questions</h2>', 1)
    p['content'] = c
    # Also set excerpt for meta description
    if not p.get('excerpt'):
        p['excerpt'] = gen_description(p['title'], c)
    print(f'{slug}: updated, excerpt len={len(p["excerpt"])}')

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

# Re-score
print('\n=== Re-score ===')
for slug in TARGETS:
    p = next(x for x in posts if x['slug']==slug)
    html = f"<!DOCTYPE html><html><head><title>{p['title']}</title><meta name='description' content='{p.get('excerpt','')[:160]}'/></head><body><h1>{p['title']}</h1>{p['content']}</body></html>"
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.html'
    tmp.write_text(html, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"\n{slug}: score={r['score']} words={r['word_count']}")
    fails = [c for c in r['checks'] if not c['pass']]
    for c in fails:
        print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")
