import io, sys, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

posts = json.load(open('data/posts.json', encoding='utf-8'))
miss = []
total = 0
for p in posts:
    slug = p.get('slug', '')
    f = os.path.join('out', 'blog', slug, 'index.html')
    if not os.path.exists(f):
        continue
    total += 1
    c = open(f, encoding='utf-8', errors='ignore').read()
    if 'FAQPage' not in c or 'application/ld+json' not in c:
        miss.append(slug)
print('博客页:', total, '| 含FAQPage schema:', total - len(miss), '| 缺失:', len(miss))
for s in miss:
    print('  ', s)
