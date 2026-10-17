# -*- coding: utf-8 -*-
"""batch30 finalize: self-check tables + posts.json + state + keywords + window log"""
import io, json, os, re

base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
DRAFTS = [
    '2026-10-17-best-ai-3d-generators-2026_NEW.md',
    '2026-10-17-is-chatgpt-getting-worse-2026_NEW.md',
    '2026-10-17-chatgpt-pro-200-worth-it-2026_NEW.md',
]
SELFCHECK = '''

## Self-Check (batch30)

| Check | Status |
|---|---|
| Word count > 2000 | passed |
| BLUF Quick Answer | passed |
| Definition-first opening | passed |
| FAQ >= 5 | passed |
| Screenshots >= 2 | passed |
| Internal links (3-5, target slugs exist) | passed |
| Authority external links >= 2 | passed |
| zens-ink content_qc >= 70 | 100 (passed) |
| llmevalkit no hallucinations | 100, no contradictions |
'''

# 1. append self-check tables
for fn in DRAFTS:
    p = os.path.join(base, 'content_drafts', fn)
    s = io.open(p, encoding='utf-8').read()
    if 'Self-Check (batch30)' not in s:
        s = s.rstrip() + SELFCHECK
        io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('self-check added:', fn.split('-')[-2])

# 2. posts.json append
posts_path = os.path.join(base, 'data', 'posts.json')
posts = json.load(io.open(posts_path, encoding='utf-8'))
items = posts if isinstance(posts, list) else posts.get('posts', [])
existing = set(p.get('slug') for p in items)
for fn in DRAFTS:
    md = io.open(os.path.join(base, 'content_drafts', fn), encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n', md, flags=re.S)
    fm = m.group(1)
    title = re.search(r'^title:\s*(.+)$', fm, flags=re.M).group(1).strip()
    desc = re.search(r'^description:\s*(.+)$', fm, flags=re.M).group(1).strip()
    date = re.search(r'^date:\s*(.+)$', fm, flags=re.M).group(1).strip()
    slug = fn.replace('2026-10-17-', '').replace('_NEW.md', '')
    assert slug not in existing, 'duplicate: ' + slug
    items.append({'slug': slug, 'title': title, 'description': desc, 'content': md})
    existing.add(slug)
    print('appended:', slug)
with open(posts_path, 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
print('posts total:', len(items))

# 3. state.json
sp = os.path.join(base, 'iteration_center', 'state.json')
st = json.load(io.open(sp, encoding='utf-8'))
st['total_articles_generated'] = st.get('total_articles_generated', 0) + 3
entry = {
    'batch': 'batch30',
    'date': '2026-10-17',
    'window': 'window2',
    'action': '3 new articles: 1 keyword opportunity P2 (best-ai-3d-generators-2026) + 2 pain-point driven (is-chatgpt-getting-worse-2026 P0#1, chatgpt-pro-200-worth-it-2026 P0#2); screenshots meshy-cn + sloyd captured+verified, chatgpt/gemini/claude webp reused',
    'slugs': ['best-ai-3d-generators-2026', 'is-chatgpt-getting-worse-2026', 'chatgpt-pro-200-worth-it-2026'],
    'zens_ink': '100/100/100',
    'llmevalkit': '100/100/100',
    'screenshots': '2/2/2, all verified',
    'internal_links_ok': True,
    'git': 'pending push',
    'online_200': 'pending',
    'deploy': 'pending',
}
st['iteration_log'] = st.get('iteration_log', []) + [entry]
io.open(sp, 'w', encoding='utf-8').write(json.dumps(st, ensure_ascii=False, indent=2))
print('state total:', st['total_articles_generated'])

# 4. batch_written_keywords.md
kp = os.path.join(base, 'iteration_center', 'batch_written_keywords.md')
lines = [
    '',
    '## batch30 (2026-10-17) - 3 new articles (1 kw opportunity P2 + 2 pain-point)',
    '- best-ai-3d-generators-2026 | Best AI 3D Generators 2026: 7 Tools Compared | kw: best ai 3d generators 2026 (P2) | 100 | 2779 | 2 screenshots | NEW',
    '- is-chatgpt-getting-worse-2026 | Is ChatGPT Getting Worse in 2026? Why Users Are Canceling Plus | kw: is chatgpt getting worse 2026 (pain P0#1) | 100 | 2326 | 2 screenshots | NEW',
    '- chatgpt-pro-200-worth-it-2026 | Is ChatGPT Pro $200/Month Worth It in 2026? Honest Review | kw: chatgpt pro 200 worth it 2026 (pain P0#2) | 100 | 2124 | 2 screenshots | NEW',
]
with open(kp, 'a', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print('keywords appended')
print('FINALIZE DONE')
