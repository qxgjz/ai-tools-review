# -*- coding: utf-8 -*-
import io, json, re, datetime
base = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'

def load(p):
    return json.load(io.open(base + p, encoding='utf-8'))
def save(p, d):
    io.open(base + p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2))

def parse_md(slug):
    s = io.open(base + r'\content_drafts\2026-10-11-' + slug + '_REWRITE.md', encoding='utf-8').read()
    s = s.split('## Self-Check Report')[0]
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", s))
    title = s.split('\n', 1)[0].lstrip('# ').strip()
    # quick answer: first **Quick Answer: ...** block
    qa = re.search(r'\*\*Quick Answer: (.+?)\*\*', s, re.S)
    quickAnswer = re.sub(r'\s+', ' ', qa.group(1)).strip() if qa else ''
    excerpt = quickAnswer[:150]
    # key takeaways: pull first sentence of each H2 body is complex; craft from quickAnswer + pricing facts
    il = sorted(set(re.findall(r'\[[^\]]+\]\(/blog/([^/]+)/\)', s)))
    ext = [x for x in re.findall(r'\]\((https?://[^)]+)\)', s) if '/blog/' not in x]
    imgs = re.findall(r'!\[[^\]]*\]\((/screenshots/real/webp/[^)]+)\)', s)
    # FAQ: from '## Frequently Asked Questions' onward, capture ### Question \n answer
    faq = []
    fsec = s.split('## Frequently Asked Questions')
    if len(fsec) > 1:
        parts = re.split(r'\n### ', fsec[1])
        for part in parts[1:]:
            lines = part.strip().split('\n', 1)
            q = lines[0].strip()
            a = re.sub(r'\s+', ' ', lines[1].strip()) if len(lines) > 1 else ''
            faq.append({'question': q, 'answer': a})
    return {'title': title, 'content': s, 'quickAnswer': quickAnswer, 'excerpt': excerpt,
            'keyTakeaways': None, 'faq': faq, 'internalLinks': il, 'affiliateLinks': ext,
            'screenshotCount': len(imgs), 'wordCount': words, 'date': '2026-10-11'}

info = {}
for slug in ['lovable-vs-boltnew', 'beautiful-ai-alternatives', 'sudowrite-alternatives']:
    info[slug] = parse_md(slug)
    print(slug, '| words:', info[slug]['wordCount'], '| faq:', len(info[slug]['faq']), '| il:', info[slug]['internalLinks'], '| imgs:', info[slug]['screenshotCount'])

# keyTakeaways per slug
kt = {
 'lovable-vs-boltnew': [
   'Lovable and Bolt.new both cost $25/month at Pro; Lovable grants 100 credits, Bolt grants 10M tokens with rollover',
   'Lovable wins for non-developers: auth, database, and hosting ship with the generated app',
   'Bolt.new wins for developers: real editable code in a browser IDE with GitHub export',
   'Bolt free tier caps at 300K daily tokens; Lovable free tier includes 5 lovable.app domains',
 ],
 'beautiful-ai-alternatives': [
   'Beautiful.ai Pro is $14.50/month annual billing; Teams is $40/month including 3 users',
   'Gamma is the best free-tier alternative; Canva is the best overall for non-designers',
   'Beautiful.ai keeps users via auto-aligning Smart Slides and native PowerPoint round-tripping',
   'Pick by three questions: who builds, where decks live, and what the budget is',
 ],
 'sudowrite-alternatives': [
   'Sudowrite costs $10/$22/$44 per month with 225K/1M/2M credits, yearly up to 50% off',
   'Claude is the best overall alternative at $18/month with long-context prose consistency',
   'ChatGPT free tier covers outlining; NovelAI adds image-assisted worldbuilding',
   'Draft a chapter in each free tier before subscribing — measure output before you pay',
 ],
}
for slug, arr in kt.items():
    info[slug]['keyTakeaways'] = arr

posts = load(r'\data\posts.json')
for slug, d in info.items():
    for p in posts:
        if p.get('slug') == slug:
            p['title'] = d['title']
            p['content'] = d['content']
            p['quickAnswer'] = d['quickAnswer']
            p['excerpt'] = d['excerpt']
            p['keyTakeaways'] = d['keyTakeaways']
            p['faq'] = d['faq']
            p['internalLinks'] = d['internalLinks']
            p['affiliateLinks'] = d['affiliateLinks']
            p['hasRealScreenshots'] = True
            p['screenshotCount'] = d['screenshotCount']
            p['wordCount'] = d['wordCount']
            p['date'] = d['date']
            p['publishedAt'] = '2026-10-11'
            print('updated posts:', slug)
save(r'\data\posts.json', posts)

# state.json
st = load(r'\iteration_center\state.json')
st['total_articles_generated'] = 47
log_entry = {
 'batch': 'batch18', 'date': '2026-10-11', 'window': 'window2/creator',
 'action': 'rewrite 3 low-score articles', 'slugs': ['lovable-vs-boltnew', 'beautiful-ai-alternatives', 'sudowrite-alternatives'],
 'zens_ink': [73, 73, 73], 'llmevalkit': [100, 100, 100],
 'screenshots': 8, 'internal_links_ok': True, 'git': None, 'online_200': False,
}
st.setdefault('iteration_log', []).append(log_entry)
save(r'\iteration_center\state.json', st)
print('state saved, total:', st['total_articles_generated'])

# keywords
kw_path = base + r'\iteration_center\batch_written_keywords.md'
with io.open(kw_path, 'a', encoding='utf-8') as f:
    f.write('\n## batch18 (2026-10-11) - rewrite\n')
    f.write('- lovable-vs-boltnew | Lovable vs Bolt.new 2026: We Built the Same App on Both | kw: lovable vs bolt.new\n')
    f.write('- beautiful-ai-alternatives | 7 Best Beautiful.ai Alternatives in 2026 (Free & Paid) | kw: beautiful.ai alternatives\n')
    f.write('- sudowrite-alternatives | 7 Best Sudowrite Alternatives in 2026 (For Novel Writers) | kw: sudowrite alternatives\n')
print('keywords appended')
